# gps_page.py (in app/pages)
import streamlit as st

from analysis.data_loader import load_gps_data
from charts.gps_charts import (
    distance_bar_chart, distance_line_chart, distance_box_by_session, distance_cumulative_area,
    accel_bar, accel_box_session, accel_vs_speed, accel_over_time,
    hr_stacked_bar, hr_violin, hr_area_over_time, hr_zone_ratio
)
from utils.ui_styling import load_local_css
load_local_css()
def show_gps_page():
    # st.set_page_config(layout="wide")
    st.sidebar.image("app/static/chelsea_logo.png", width=120)
    st.title("📍 GPS Metrics Dashboard")

    df = load_gps_data()

    # Player filter
    players = sorted(df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players)
    df = df[df["player"].isin(selected_players)]

    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📆 Distance Ran Analysis", 
        "⚡ Acceleration Analysis", 
        "❤️ Heart Rate Analysis",
        "📈 Player Comparison"
    ])

    # Distance Ran Analysis
    with tab1:
        st.subheader("Distance Metrics")
        col1, col2 = st.columns(2)
        with col1:
            distance_bar_chart(df)
        with col2:
            distance_line_chart(df)

        col3, col4 = st.columns(2)
        with col3:
            distance_box_by_session(df)
        with col4:
            distance_cumulative_area(df)

    # Acceleration Analysis
    with tab2:
        st.subheader("Acceleration Events")
        col1, col2 = st.columns(2)
        with col1:
            accel_bar(df)
        with col2:
            accel_box_session(df)

        col3, col4 = st.columns(2)
        with col3:
            accel_vs_speed(df)
        with col4:
            accel_over_time(df)

    # Heart Rate Analysis
    with tab3:
        st.subheader("Heart Rate Zones")
        col1, col2 = st.columns(2)
        with col1:
            hr_stacked_bar(df)
        with col2:
            hr_violin(df)

        col3, col4 = st.columns(2)
        with col3:
            hr_area_over_time(df)
        with col4:
            hr_zone_ratio(df)

    # Player Comparison (basic layout to be extended)
    with tab4:
        st.subheader("Player Comparison")
        st.info("This section will include player-specific comparisons with date filtering and key metrics.")

if __name__ == "__main__":
    show_gps_page()
