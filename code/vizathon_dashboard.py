import streamlit as st
import pandas as pd
import plotly.express as px

# Data loading and advanced analysis modules
from code.analysis.data_loader import load_all_data
from code.analysis.advanced_analysis import run_regression, cluster_players

# Chart modules
from code.charts.gps_charts import (
    show_session_type_boxplot,
    show_high_speed_zones,
    show_accel_distance_bubble
)
from code.charts.recovery_charts import (
    show_avg_recovery_line,
    show_recovery_box,
    show_recovery_domains
)
from code.charts.capability_charts import (
    show_benchmark_by_movement,
    show_benchmark_by_expression
)
from code.charts.ipa_charts import (
    show_priority_category,
    show_tracking_status,
    show_type_distribution
)
from code.charts.combined_charts import (
    show_gps_vs_recovery
)


def main():
    st.set_page_config(page_title="Chelsea FC Vizathon Dashboard", layout="wide")
    st.title("Chelsea FC Vizathon Performance Dashboard")

    # 1) Load Data from local CSVs (no file upload). Requires 'data/' folder.
    gps_df, recovery_df, capability_df, ipa_df = load_all_data()

    # 2) KPI Example
    st.markdown("## 📌 Key Performance Indicators")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg GPS Distance", f"{gps_df['distance'].mean():.1f}")
    col2.metric("Avg Recovery Score", f"{recovery_df['emboss_baseline_score'].mean():.2f}")
    col3.metric("IPA Goals", len(ipa_df))

    # 3) Setup Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "GPS", "Recovery", "Capability", "IPA", "Combined", "Advanced Analysis"
    ])

    with tab1:
        st.subheader("📊 GPS Load Metrics")
        show_session_type_boxplot(gps_df)
        show_high_speed_zones(gps_df)
        show_accel_distance_bubble(gps_df)

    with tab2:
        st.subheader("💤 Recovery Status")
        show_avg_recovery_line(recovery_df)
        show_recovery_box(recovery_df)
        show_recovery_domains(recovery_df)

    with tab3:
        st.subheader("🏋️ Physical Capability")
        show_benchmark_by_movement(capability_df)
        show_benchmark_by_expression(capability_df)

    with tab4:
        st.subheader("🧠 Individual Priority Areas")
        show_priority_category(ipa_df)
        show_tracking_status(ipa_df)
        show_type_distribution(ipa_df)

    with tab5:
        st.subheader("🔀 Combined Insights")
        show_gps_vs_recovery(gps_df, recovery_df)

    with tab6:
        st.subheader("📈 Advanced Analysis")

        # Regression
        st.markdown("### 🔁 1. Regression: Predicting Peak Speed")
        reg_df, r2 = run_regression(gps_df)
        st.write(f"R² Score: {r2:.3f}")
        fig_reg = px.scatter(reg_df, x="peak_speed", y="predicted",
                             title="Actual vs Predicted Peak Speed",
                             labels={"peak_speed": "Actual Peak Speed", "predicted": "Predicted Peak Speed"})
        # Add diagonal line
        min_val, max_val = reg_df["peak_speed"].min(), reg_df["peak_speed"].max()
        fig_reg.add_shape(type="line", x0=min_val, y0=min_val, x1=max_val, y1=max_val,
                          line=dict(dash="dash", color="red"))
        st.plotly_chart(fig_reg)

        # Clustering
        st.markdown("### 🔍 2. Clustering: Player Load Profiles (via PCA)")
        cluster_data, kmeans, pca = cluster_players(gps_df)
        fig_cluster = px.scatter(cluster_data, x="PC1", y="PC2",
                                 color=cluster_data["cluster"].astype(str),
                                 hover_name="player",
                                 title="PCA Projection of Load Clusters")
        st.plotly_chart(fig_cluster)

if __name__ == "__main__":
    main()
