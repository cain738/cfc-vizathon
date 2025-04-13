import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Distance Charts
def distance_bar_chart(df: pd.DataFrame):
    fig = px.bar(df.groupby("player")["distance"].mean().reset_index(),
                 x="player", y="distance", title="Average Distance by Player")
    st.plotly_chart(fig, use_container_width=True)

def distance_line_chart(df: pd.DataFrame):
    fig = px.line(df.groupby("date")["distance"].mean().reset_index(),
                  x="date", y="distance", title="Avg Distance Over Time")
    st.plotly_chart(fig, use_container_width=True)

def distance_box_by_session(df: pd.DataFrame):
    fig = px.box(df, x="session_type", y="distance", color="session_type",
                 title="Distance by Session Type")
    st.plotly_chart(fig, use_container_width=True)

def distance_cumulative_area(df: pd.DataFrame):
    df_grouped = df.groupby("date")["distance"].sum().cumsum().reset_index(name="cumulative_distance")
    fig = px.area(df_grouped, x="date", y="cumulative_distance", title="Cumulative Distance Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Acceleration Charts
def accel_bar(df: pd.DataFrame):
    fig = px.bar(df.groupby("player")["accel_decel_over_2_5"].mean().reset_index(),
                 x="player", y="accel_decel_over_2_5", title="Avg Accel/Decel Events by Player")
    st.plotly_chart(fig, use_container_width=True)

def accel_box_session(df: pd.DataFrame):
    fig = px.box(df, x="session_type", y="accel_decel_over_2_5", color="session_type",
                 title="Accel/Decel Events by Session Type")
    st.plotly_chart(fig, use_container_width=True)

def accel_vs_speed(df: pd.DataFrame):
    fig = px.scatter(df, x="accel_decel_over_2_5", y="peak_speed", color="player",
                     title="Accel Events vs Peak Speed")
    st.plotly_chart(fig, use_container_width=True)

def accel_over_time(df: pd.DataFrame):
    fig = px.line(df.groupby("date")["accel_decel_over_2_5"].mean().reset_index(),
                  x="date", y="accel_decel_over_2_5", title="Avg Accel Events Over Time")
    st.plotly_chart(fig, use_container_width=True)

# Heart Rate Charts
def hr_stacked_bar(df: pd.DataFrame):
    grouped = df.groupby("player")[["hr_zone_1_hms", "hr_zone_2_hms", "hr_zone_3_hms", "hr_zone_4_hms"]].sum()
    grouped = grouped.reset_index().melt(id_vars="player", var_name="HR Zone", value_name="Minutes")
    fig = px.bar(grouped, x="player", y="Minutes", color="HR Zone", title="Heart Rate Zone Time by Player")
    st.plotly_chart(fig, use_container_width=True)

def hr_violin(df: pd.DataFrame):
    fig = px.violin(df, x="player", y="hr_zone_3_hms", box=True, title="Zone 3 HR Time Distribution")
    st.plotly_chart(fig, use_container_width=True)

def hr_area_over_time(df: pd.DataFrame):
    df_grouped = df.groupby("date")[["hr_zone_1_hms", "hr_zone_2_hms", "hr_zone_3_hms", "hr_zone_4_hms"]].mean()
    df_grouped = df_grouped.reset_index()
    fig = go.Figure()
    for col in df_grouped.columns[1:]:
        fig.add_trace(go.Scatter(x=df_grouped["date"], y=df_grouped[col], stackgroup='one', name=col))
    fig.update_layout(title="Heart Rate Zones Over Time")
    st.plotly_chart(fig, use_container_width=True)

def hr_zone_ratio(df: pd.DataFrame):
    zone_totals = df[["hr_zone_1_hms", "hr_zone_2_hms", "hr_zone_3_hms", "hr_zone_4_hms"]].sum()
    zone_df = pd.DataFrame({"Zone": zone_totals.index, "Total Time": zone_totals.values})
    fig = px.pie(zone_df, names="Zone", values="Total Time", title="Total Time in Each HR Zone")
    st.plotly_chart(fig, use_container_width=True)
