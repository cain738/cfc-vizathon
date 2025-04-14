# app/pages/gps_page.py
import streamlit as st
import pandas as pd
from analysis.data_loader import load_gps_data, load_calendar_data
from feature_engineering.data_wrangler import merge_gps_with_calendar
from utils.ui_styling import load_local_css
from charts.gps_charts import (
    plot_distance_stacked_bar, plot_distance_regression,
    plot_distance_radar, plot_acceleration_stacked_bar,
    plot_acceleration_regression, plot_acceleration_radar,
    plot_heart_rate_stacked_bar, plot_heart_rate_regression,
    plot_heart_rate_radar, plot_gps_player_comparison
)

# Required before anything else
load_local_css()

def show_gps_page():
    st.title("🛰 GPS Metrics Dashboard")

    # Load and merge GPS + calendar data
    gps_df = load_gps_data()
    cal_df = load_calendar_data()
    df = merge_gps_with_calendar(gps_df, cal_df)

    # Sidebar filters
    players = sorted(df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players)
    date_range = st.sidebar.date_input("Select Date Range", [df["date"].min(), df["date"].max()])
    
    df = df[df["player"].isin(selected_players)]
    df = df[(df["date"] >= pd.to_datetime(date_range[0])) & (df["date"] <= pd.to_datetime(date_range[1]))]

    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📏 Distance Ran", "🚀 Acceleration Bursts", "💓 Heart Rate", "👥 Player Comparison"
    ])

    with tab1:
        st.subheader("Distance Ran Analysis")
        col1, col2 = st.columns(2)
        with col1:
            plot_distance_stacked_bar(df)
        with col2:
            plot_distance_radar(df)
        plot_distance_regression(df)

    with tab2:
        st.subheader("Acceleration Burst Analysis")
        col1, col2 = st.columns(2)
        with col1:
            plot_acceleration_stacked_bar(df)
        with col2:
            plot_acceleration_radar(df)
        plot_acceleration_regression(df)

    with tab3:
        st.subheader("Heart Rate Zone Analysis")
        col1, col2 = st.columns(2)
        with col1:
            plot_heart_rate_stacked_bar(df)
        with col2:
            plot_heart_rate_radar(df)
        plot_heart_rate_regression(df)

    with tab4:
        st.subheader("Compare Player GPS Metrics")
        plot_gps_player_comparison(df)

if __name__ == "__main__":
    show_gps_page()
