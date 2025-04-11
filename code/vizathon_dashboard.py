import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Chelsea FC Vizathon Dashboard", layout="wide")
st.title("Chelsea FC Vizathon Performance Dashboard")

# --- Load Data ---
st.markdown("### Upload preprocessed CSVs for GPS, Recovery, Capability, IPA")
gps_file = st.file_uploader("Upload GPS Data", type="csv")
recovery_file = st.file_uploader("Upload Recovery Data", type="csv")
capability_file = st.file_uploader("Upload Capability Data", type="csv")
ipa_file = st.file_uploader("Upload IPA Data", type="csv")

@st.cache_data
def load_data(file):
    return pd.read_csv(file, parse_dates=["date"]) if file else None

if gps_file and recovery_file and capability_file and ipa_file:
    gps_df = pd.read_csv(gps_file, parse_dates=["date"])
    recovery_df = pd.read_csv(recovery_file, parse_dates=["date"])
    capability_df = pd.read_csv(capability_file, parse_dates=["date"])
    ipa_df = pd.read_csv(ipa_file, parse_dates=["target_set_date", "review_date"])

    # Sidebar filters
    st.sidebar.header("🔎 Filter Options")
    selected_player = st.sidebar.selectbox("Select Player", sorted(gps_df["player"].unique()))
    start_date = st.sidebar.date_input("Start Date", gps_df["date"].min().date())
    end_date = st.sidebar.date_input("End Date", gps_df["date"].max().date())

    gps_filtered = gps_df[(gps_df["player"] == selected_player) & (gps_df["date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))]
    recovery_filtered = recovery_df[(recovery_df["player"] == selected_player) & (recovery_df["date"].between(pd.to_datetime(start_date), pd.to_datetime(end_date)))]
    capability_filtered = capability_df[capability_df["player"] == selected_player]
    ipa_filtered = ipa_df[ipa_df["player"] == selected_player]

    # KPI Metrics
    st.markdown("## 📌 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg GPS Distance", f"{gps_filtered['distance'].mean():.1f} m")
    col2.metric("Avg Recovery Score", f"{recovery_filtered['emboss_baseline_score'].mean():.2f}")
    col3.metric("IPA Goals", len(ipa_filtered))

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["GPS", "Recovery", "Capability", "IPA", "Combined", "Advanced Analysis"])

    with tab1:
        st.subheader("📊 GPS Load Metrics")
        st.markdown("**📦 Chart 2: Player Load by Session Type**")
        st.plotly_chart(px.box(gps_df, x="session_type", y="distance", title="Distance by Session Type"))
        st.caption("Match days show significantly higher workload — recovery scheduling is key.")

        st.markdown("**⚡ Chart 3: High-Speed Running Zones per Player**")
        high_speed_summary = gps_df.groupby("player")[["distance_over_21", "distance_over_24", "distance_over_27"]].mean().reset_index()
        high_speed_melted = high_speed_summary.melt(id_vars="player", var_name="speed_zone", value_name="distance")
        st.plotly_chart(px.bar(high_speed_melted, x="player", y="distance", color="speed_zone", barmode="group", title="High-Speed Running Zones per Player"))
        st.caption("Highlights sprint thresholds — ideal to flag conditioning or injury risks.")

        st.markdown("**🫧 Chart 4: Acceleration vs Distance Bubble View**")
        fig = px.scatter(gps_df, x="distance", y="accel_decel_over_2_5", size="accel_decel_over_4_5", color="peak_speed",
                         title="Acceleration vs Distance Bubble Chart", hover_name="player")
        st.plotly_chart(fig)
        st.caption("Top-right red bubbles = sessions with high acceleration + distance → monitor for overload.")

    with tab6:
        st.subheader("📈 Advanced Analysis")

        st.markdown("### 🔁 1. Regression: Predicting Peak Speed")
        regression_df = gps_df.dropna(subset=["peak_speed", "distance", "distance_over_24", "accel_count_2_5"])
        X = regression_df[["distance", "distance_over_24", "accel_count_2_5"]]
        y = regression_df["peak_speed"]
        model = LinearRegression().fit(X, y)
        regression_df["predicted"] = model.predict(X)
        fig = px.scatter(regression_df, x="peak_speed", y="predicted",
                         title="Actual vs Predicted Peak Speed",
                         labels={"peak_speed": "Actual Peak Speed", "predicted": "Predicted Peak Speed"})
        fig.add_shape(type="line", x0=y.min(), y0=y.min(), x1=y.max(), y1=y.max(), line=dict(dash="dash", color="red"))
        st.plotly_chart(fig)
        st.caption("Prediction accuracy helps track player performance; try non-linear models later.")

        st.markdown("### 🔍 2. Clustering: Player Load Profiles (via PCA)")
        cluster_data = gps_df[["player", "distance", "distance_over_24", "distance_over_27", "accel_count_2_5", "accel_count_4_5", "peak_speed"]].dropna()
        cluster_data_std = StandardScaler().fit_transform(cluster_data.drop("player", axis=1))
        kmeans = KMeans(n_clusters=3, random_state=42).fit(cluster_data_std)
        pca = PCA(n_components=2)
        pca_comp = pca.fit_transform(cluster_data_std)
        cluster_plot_df = pd.DataFrame(pca_comp, columns=["PC1", "PC2"])
        cluster_plot_df["cluster"] = kmeans.labels_
        cluster_plot_df["player"] = cluster_data["player"].values
        fig = px.scatter(cluster_plot_df, x="PC1", y="PC2", color=cluster_plot_df["cluster"].astype(str), hover_name="player",
                         title="PCA Projection of Load Clusters")
        st.plotly_chart(fig)
        st.caption("Cluster 1 = match sessions, Cluster 0 = training load, Cluster 2 = recovery/split sessions")

        st.markdown("### 📊 Cluster Profile Breakdown – Average Metrics")
        cluster_data["cluster"] = kmeans.labels_
        cluster_avg = cluster_data.groupby("cluster").mean().reset_index()
        cluster_melt = cluster_avg.melt(id_vars="cluster", var_name="metric", value_name="value")
        st.plotly_chart(px.bar(cluster_melt, x="metric", y="value", color=cluster_melt["cluster"].astype(str), barmode="group",
                               title="Cluster-wise Load Metric Averages"))
        st.caption("Cluster 1 leads in most metrics → likely starters on matchdays.")

        st.markdown("### 📈 Cluster Time Trends – Sessions Per Day")
        gps_cluster_df = gps_df.merge(cluster_data[["player", "cluster"]], on="player", how="inner")
        gps_cluster_df = gps_cluster_df.groupby(["date", "cluster"]).size().reset_index(name="session_count")
        fig = px.line(gps_cluster_df, x="date", y="session_count", color=gps_cluster_df["cluster"].astype(str),
                      title="Cluster Distribution Over Time")
        st.plotly_chart(fig)
        st.caption("Helps assess training balance and load rotation through match weeks.")

    # Export Buttons
    st.markdown("## 📥 Export Filtered Data")
    st.download_button("Download GPS", gps_filtered.to_csv(index=False), file_name="gps_filtered.csv")
    st.download_button("Download Recovery", recovery_filtered.to_csv(index=False), file_name="recovery_filtered.csv")
    st.download_button("Download Capability", capability_filtered.to_csv(index=False), file_name="capability_filtered.csv")
    st.download_button("Download IPA", ipa_filtered.to_csv(index=False), file_name="ipa_filtered.csv")

else:
    st.info("Please upload all four datasets to view dashboard.")
