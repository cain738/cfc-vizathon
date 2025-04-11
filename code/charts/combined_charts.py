# code/charts/combined_charts.py
import pandas as pd
import plotly.express as px
import streamlit as st

def show_gps_vs_recovery(gps_df, recovery_df):
    merged = pd.merge(gps_df, recovery_df, on=["player", "date"], how="inner")
    fig = px.scatter(merged, x="distance", y="emboss_baseline_score", trendline="ols", title="GPS Load vs Recovery")
    st.plotly_chart(fig)

def show_cluster_profile(clustered_df):
    """
    Example: We assume advanced_analysis provides a cluster_data with 'cluster', 'PC1', 'PC2'
    """
    fig = px.scatter(clustered_df, x="PC1", y="PC2", color=clustered_df["cluster"].astype(str),
                     hover_name="player", title="PCA Projection of Load Clusters")
    st.plotly_chart(fig)
