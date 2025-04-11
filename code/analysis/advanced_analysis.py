# code/analysis/advanced_analysis.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score

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
