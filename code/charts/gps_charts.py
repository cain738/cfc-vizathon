# code/charts/gps_charts.py
import plotly.express as px
import streamlit as st

def show_session_type_boxplot(gps_df):
    fig = px.box(gps_df, x="session_type", y="distance", title="Distance by Session Type")
    st.plotly_chart(fig)
    st.caption("Match days show significantly higher workload — recovery scheduling is key.")

def show_high_speed_zones(gps_df):
    high_speed_summary = gps_df.groupby("player")[["distance_over_21", "distance_over_24", "distance_over_27"]].mean().reset_index()
    melted = high_speed_summary.melt(id_vars="player", var_name="speed_zone", value_name="distance")
    fig = px.bar(melted, x="player", y="distance", color="speed_zone",
                 barmode="group", title="High-Speed Running Zones per Player")
    st.plotly_chart(fig)
    st.caption("Highlights sprint thresholds — ideal to flag conditioning or injury risks.")

def show_accel_distance_bubble(gps_df):
    fig = px.scatter(gps_df, x="distance", y="accel_decel_over_2_5", size="accel_decel_over_4_5",
                     color="peak_speed", title="Acceleration vs Distance Bubble Chart",
                     hover_name="player")
    st.plotly_chart(fig)
    st.caption("Top-right red bubbles = sessions with high acceleration + distance → monitor for overload.")
