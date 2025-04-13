# app/analysis/advanced_analysis.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from analysis.data_loader import load_recovery_data, load_calendar_data
from feature_engineering.data_wrangler import load_advanced_capability_recovery_data


def run_regression(gps_df):
    """
    Example: Predict peak_speed from distance, distance_over_24, accel_decel_over_2_5
    """
    df = gps_df.dropna(subset=["peak_speed", "distance", "distance_over_24", "accel_decel_over_2_5"])
    X = df[["distance", "distance_over_24", "accel_decel_over_2_5"]]
    y = df["peak_speed"]
    model = LinearRegression().fit(X, y)
    df["predicted"] = model.predict(X)
    r2 = r2_score(y, df["predicted"])
    return df, r2

def cluster_players(gps_df):
    """
    Example: Use KMeans + PCA for clustering by workload metrics
    """
    cluster_data = gps_df[["player", "distance", "distance_over_24", "distance_over_27",
                           "accel_decel_over_2_5", "accel_decel_over_4_5", "peak_speed"]].dropna()

    X = cluster_data.drop("player", axis=1)
    X_scaled = StandardScaler().fit_transform(X)
    kmeans = KMeans(n_clusters=3, random_state=42).fit(X_scaled)

    pca = PCA(n_components=2)
    pcs = pca.fit_transform(X_scaled)

    cluster_data["cluster"] = kmeans.labels_
    cluster_data["PC1"] = pcs[:, 0]
    cluster_data["PC2"] = pcs[:, 1]

    return cluster_data, kmeans, pca

def compute_recovery_feature_importances():
    """
    1) Loads recovery + calendar data
    2) Merges them to identify matchdays
    3) Adds matchday ± 1 indicators
    4) Trains a RandomForest to predict 'emboss_baseline_score'
    5) Returns a DF of feature importances + correlation matrix
    """

    # 1. Load data
    recovery_df = load_recovery_data()
    calendar_df = load_calendar_data()  # For instance, 'chelsea_fc_calendar.csv'

    # 2. Identify match days in calendar
    #    We'll assume 'event_type == "Match"' means a matchday
    match_dates = calendar_df.loc[calendar_df["event_type"] == "Match", "event_date"].unique()

    # 3. Mark MD+1, MD-1 in recovery_df
    #    We'll assume date is a daily measure
    #    We do a simple approach: for each date in recovery_df, if date-1 or date+1 is a match date => True
    recovery_df["md_minus_1"] = recovery_df["date"].isin(match_dates + np.timedelta64(1, 'D'))
    recovery_df["md_plus_1"]  = recovery_df["date"].isin(match_dates - np.timedelta64(1, 'D'))
    # Some prefer the opposite sign, check your logic carefully.

    # 4. Prepare features + target
    #    We'll pick the composite columns + MD indicators as features
    #    Filter rows with non-null EMBOSS baseline
    df_model = recovery_df.dropna(subset=["emboss_baseline_score"]).copy()

    X = df_model[[
        "Bio_composite",
        "Msk_joint_range_composite",
        "Subjective_composite",
        "Sleep_composite",
        # Our new MD flags
        "md_minus_1",
        "md_plus_1"
    ]].copy()

    # Convert booleans to numeric
    X["md_minus_1"] = X["md_minus_1"].astype(int)
    X["md_plus_1"]  = X["md_plus_1"].astype(int)

    y = df_model["emboss_baseline_score"]

    # 5. Train a RandomForest Regressor
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled  = scaler.transform(X_test)

    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    # 6. Feature Importances
    fi = model.feature_importances_
    feature_names = X.columns.tolist()
    fi_df = pd.DataFrame({
        "feature": feature_names,
        "importance": fi
    }).sort_values("importance", ascending=False).reset_index(drop=True)

    # 7. Return the DF
    return fi_df, df_model

def compute_movement_recovery_correlations() -> pd.DataFrame:
    """
    Loads the merged capability and recovery dataset,
    and for each movement, computes the Pearson correlation coefficient
    between the capability metric (BenchmarkPct) and each recovery metric:
       - Sleep_composite
       - Bio_composite
       - Msk_joint_range_composite
       - Subjective_composite
       - emboss_baseline_score

    Returns:
        A DataFrame with columns: 'movement', 'Sleep_composite', 'Bio_composite',
        'Msk_joint_range_composite', 'Subjective_composite', 'emboss_baseline_score',
        where each value is the correlation coefficient.
    """
    # Load merged data using our data wrangler; it returns (merged_df, filepath)
    merged_df, _ = load_advanced_capability_recovery_data()
    
    # Define required columns (if missing, rows will be dropped)
    required_cols = [
        "BenchmarkPct", "Sleep_composite", "Bio_composite",
        "Msk_joint_range_composite", "Subjective_composite", 
        "emboss_baseline_score", "movement"
    ]
    df = merged_df.dropna(subset=required_cols).copy()
    
    # Define the recovery metrics to be compared with BenchmarkPct.
    recovery_metrics = [
        "Sleep_composite", "Bio_composite", 
        "Msk_joint_range_composite", "Subjective_composite", 
        "emboss_baseline_score"
    ]
    results = []
    # Loop through each unique movement
    for mov in df["movement"].unique():
        sub_df = df[df["movement"] == mov]
        corr_dict = {"movement": mov}
        for metric in recovery_metrics:
            # Compute the Pearson correlation (returns NaN if insufficient data)
            corr_value = sub_df["BenchmarkPct"].corr(sub_df[metric])
            corr_dict[metric] = corr_value
        results.append(corr_dict)
    corr_df = pd.DataFrame(results)
    return corr_df