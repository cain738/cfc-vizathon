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
        st.plotly_chart(px.line(gps_df.groupby("date")["distance"].sum().reset_index(), x="date", y="distance", title="Total Team Distance Over Time"))
        st.plotly_chart(px.box(gps_df, x="session_type", y="distance", title="Distance by Session Type"))
        st.plotly_chart(px.bar(gps_df.groupby("player")["distance_over_24"].mean().sort_values(ascending=False).reset_index(), x="player", y="distance_over_24", title="High-Speed Running Zones (>24 km/h)"))
        st.plotly_chart(px.histogram(gps_df, x="peak_speed", nbins=20, title="Distribution of Peak Speeds"))

    with tab2:
        st.subheader("💤 Recovery Status")
        st.plotly_chart(px.line(recovery_df.groupby("date")["emboss_baseline_score"].mean().reset_index(), x="date", y="emboss_baseline_score", title="Average Recovery Over Time"))
        st.plotly_chart(px.box(recovery_df, x="player", y="emboss_baseline_score", title="Recovery Score Distribution"))
        domain_scores = recovery_df[[col for col in recovery_df.columns if "_composite" in col]].mean().reset_index()
        domain_scores.columns = ["Domain", "Average Score"]
        st.plotly_chart(px.bar(domain_scores, x="Domain", y="Average Score", title="Composite Recovery Scores by Domain"))
        st.plotly_chart(px.scatter(recovery_df, x="Soreness_composite", y="emboss_baseline_score", color="player", title="Soreness vs Recovery Score"))

    with tab3:
        st.subheader("🏋️ Physical Capability")
        st.plotly_chart(px.bar(capability_df.groupby("movement")["BenchmarkPct"].mean().reset_index(), x="movement", y="BenchmarkPct", title="Average Benchmark by Movement"))
        st.plotly_chart(px.bar(capability_df.groupby("expression")["BenchmarkPct"].mean().reset_index(), x="expression", y="BenchmarkPct", title="Benchmark by Expression Type"))
        st.plotly_chart(px.box(capability_df, x="movement", y="BenchmarkPct", color="expression", title="Capability Spread by Movement & Expression"))

    with tab4:
        st.subheader("🧠 Individual Priority Areas")
        priority_cat = ipa_df["priority_category"].value_counts().reset_index()
        priority_cat.columns = ["priority_category", "count"]
        st.plotly_chart(px.bar(priority_cat, x="priority_category", y="count", title="Priority Goals by Category"))

        status_count = ipa_df["tracking_status"].value_counts().reset_index()
        status_count.columns = ["tracking_status", "count"]
        st.plotly_chart(px.bar(status_count, x="tracking_status", y="count", title="Tracking Status Distribution"))

        type_count = ipa_df["type"].value_counts().reset_index()
        type_count.columns = ["type", "count"]
        st.plotly_chart(px.bar(type_count, x="type", y="count", title="Habit vs Outcome Goals"))

        st.plotly_chart(px.timeline(ipa_filtered, x_start="target_set_date", x_end="review_date", y="player", color="tracking_status", title="Goal Timeline per Player"))

    with tab5:
        st.subheader("🔀 Combined Insights")
        merged = pd.merge(gps_filtered, recovery_filtered, on=["player", "date"], how="inner")
        fig = px.scatter(merged, x="distance", y="emboss_baseline_score", trendline="ols", title="GPS Load vs Recovery")
        st.plotly_chart(fig)
        st.plotly_chart(px.density_heatmap(merged, x="distance", y="emboss_baseline_score", title="Recovery vs Load Density Heatmap"))

    with tab6:
        st.subheader("📈 Advanced Analysis")

        st.markdown("### 📉 Regression Analysis: Predicting Recovery from GPS Load")
        reg_df = pd.merge(gps_df, recovery_df, on=["player", "date"], how="inner")
        if not reg_df.empty:
            X = reg_df[["distance"]]
            y = reg_df["emboss_baseline_score"]
            model = LinearRegression().fit(X, y)
            reg_df["predicted"] = model.predict(X)
            fig = px.scatter(reg_df, x="distance", y="emboss_baseline_score", trendline="ols",
                             color_discrete_sequence=["blue"], title="Linear Fit: Recovery vs Distance")
            fig.add_traces(px.line(reg_df, x="distance", y="predicted").data)
            st.plotly_chart(fig)
            st.caption("This regression model shows the linear relationship between physical workload and next-day recovery scores.")

        st.markdown("### 🤖 Player Clustering Based on Capability")
        cap_pivot = capability_df.pivot_table(index="player", columns=["movement", "quality", "expression"],
                                              values="BenchmarkPct", aggfunc="mean").fillna(0)
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(cap_pivot)
        kmeans = KMeans(n_clusters=3, random_state=42).fit(X_scaled)
        cap_pivot["cluster"] = kmeans.labels_
        pca = PCA(n_components=2)
        pcs = pca.fit_transform(X_scaled)
        pca_df = pd.DataFrame(pcs, columns=["PC1", "PC2"])
        pca_df["cluster"] = kmeans.labels_
        pca_df["player"] = cap_pivot.index
        fig = px.scatter(pca_df, x="PC1", y="PC2", color=pca_df["cluster"].astype(str), hover_name="player",
                         title="PCA Projection of Player Clusters")
        st.plotly_chart(fig)
        st.caption("Players are grouped by similar physical profiles using KMeans and visualized via PCA.")

    # Download buttons
    st.markdown("## 📥 Export Filtered Data")
    st.download_button("Download GPS", gps_filtered.to_csv(index=False), file_name="gps_filtered.csv")
    st.download_button("Download Recovery", recovery_filtered.to_csv(index=False), file_name="recovery_filtered.csv")
    st.download_button("Download Capability", capability_filtered.to_csv(index=False), file_name="capability_filtered.csv")
    st.download_button("Download IPA", ipa_filtered.to_csv(index=False), file_name="ipa_filtered.csv")

else:
    st.info("Please upload all four datasets to view dashboard.")
