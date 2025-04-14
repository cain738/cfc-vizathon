# app/pages/recovery_page.py

import streamlit as st
import pandas as pd
from utils.ui_styling import load_local_css
from analysis.data_loader import load_recovery_data
from charts.recovery_charts import (
    plot_completeness_radar, plot_completeness_heatmap, plot_completeness_scatter,
    plot_composite_radar, plot_composite_heatmap, plot_composite_scatter,
    plot_recovery_rankings, plot_recovery_player_comparison
)

# ✅ Required: first thing in the file
load_local_css()

def show_recovery_page():
    st.title("♻️ Recovery Dashboard")

    # Load and filter data
    df = load_recovery_data()
    players = sorted(df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players[:5])
    date_range = st.sidebar.date_input("Select Date Range", [df["date"].min(), df["date"].max()])
    
    df = df[df["player"].isin(selected_players)]
    df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "✅ Completeness", "🧠 Composite Metrics", "👥 Comparison & Rankings"
    ])

    with tab1:
        st.subheader("Recovery Completeness Analysis")
        col1, col2 = st.columns(2)
        with col1:
            plot_completeness_radar(df)
        with col2:
            plot_completeness_heatmap(df)
        plot_completeness_scatter(df)

    with tab2:
        st.subheader("Composite Recovery Metrics Analysis")
        col1, col2 = st.columns(2)
        with col1:
            plot_composite_radar(df)
        with col2:
            plot_composite_heatmap(df)
        plot_composite_scatter(df)

    with tab3:
        st.subheader("Player Recovery Comparison & Rankings")
        plot_recovery_rankings(df)
        plot_recovery_player_comparison(df)

if __name__ == "__main__":
    show_recovery_page()
