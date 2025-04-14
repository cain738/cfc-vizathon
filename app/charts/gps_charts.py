# app/charts/gps_charts.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

# ===================== DISTANCE =========================

def plot_distance_stacked_bar(df: pd.DataFrame):
    st.markdown("##### Distance Ratios per Player")
    df["over_21_ratio"] = df["distance_over_21"] / df["distance"]
    df["over_24_ratio"] = df["distance_over_24"] / df["distance"]
    df["over_27_ratio"] = df["distance_over_27"] / df["distance"]
    
    bar_df = df.groupby("player")[["over_21_ratio", "over_24_ratio", "over_27_ratio"]].mean().reset_index()
    fig = px.bar(bar_df, x="player", y=["over_21_ratio", "over_24_ratio", "over_27_ratio"],
                 title="High-Speed Distance Proportions", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

def plot_distance_regression(df: pd.DataFrame):
    st.markdown("##### Regression: Distance Ratios vs. Training Load")
    for ratio, label in zip(["distance_over_21", "distance_over_24", "distance_over_27"],
                            ["Over 21", "Over 24", "Over 27"]):
        df[f"{label}_ratio"] = df[ratio] / df["distance"]
        fig = px.scatter(df, x=f"{label}_ratio", y="training_load",
                         trendline="ols", title=f"{label} Ratio vs. Training Load")
        st.plotly_chart(fig, use_container_width=True)

def plot_distance_radar(df: pd.DataFrame):
    st.markdown("##### Radar: Distance Metrics Feature Importance")
    X = df[["distance_over_21", "distance_over_24", "distance_over_27"]].fillna(0)
    y = df["training_load"]
    
    model = RandomForestRegressor()
    model.fit(X, y)
    importances = model.feature_importances_

    fig = go.Figure(go.Scatterpolar(
        r=importances,
        theta=X.columns,
        fill='toself',
        name='Feature Importance'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ================== ACCELERATION ========================

def plot_acceleration_stacked_bar(df: pd.DataFrame):
    print(df.columns)
    st.markdown("##### Acceleration Ratios per Player")
    df["accel_decel_total"] = df["accel_decel_over_2_5"] + df["accel_decel_over_3_5"] + df["accel_decel_over_4_5"]
    df["accel_2_5_ratio"] = df["accel_decel_over_2_5"] / df["accel_decel_total"]
    df["accel_3_5_ratio"] = df["accel_decel_over_3_5"] / df["accel_decel_total"]
    df["accel_4_5_ratio"] = df["accel_decel_over_4_5"] / df["accel_decel_total"]

    bar_df = df.groupby("player")[["accel_2_5_ratio", "accel_3_5_ratio", "accel_4_5_ratio"]].mean().reset_index()
    fig = px.bar(bar_df, x="player", y=["accel_2_5_ratio", "accel_3_5_ratio", "accel_4_5_ratio"],
                 title="Acceleration Ratios", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

def plot_acceleration_regression(df: pd.DataFrame):
    st.markdown("##### Regression: Acceleration Ratios vs. Training Load")
    for col, label in zip(["accel_2_5_ratio", "accel_3_5_ratio", "accel_4_5_ratio"],
                          [">2.5", ">3.5", ">4.5"]):
        fig = px.scatter(df, x=col, y="training_load",
                         trendline="ols", title=f"{label} Ratio vs. Training Load")
        st.plotly_chart(fig, use_container_width=True)

def plot_acceleration_radar(df: pd.DataFrame):
    st.markdown("##### Radar: Acceleration Feature Importance")
    X = df[["accel_decel_over_2_5", "accel_decel_over_3_5", "accel_decel_over_4_5"]].fillna(0)
    y = df["training_load"]
    model = RandomForestRegressor()
    model.fit(X, y)
    importances = model.feature_importances_

    fig = go.Figure(go.Scatterpolar(
        r=importances,
        theta=X.columns,
        fill='toself',
        name='Feature Importance'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ================== HEART RATE ========================

def plot_heart_rate_stacked_bar(df: pd.DataFrame):
    st.markdown("##### Heart Rate Zone Ratios")
    zones = [f"hr_zone_{i}_hms" for i in range(1, 6)]
    for z in zones:
        df[f"{z}_ratio"] = df[z] / df["day_duration"]
    bar_df = df.groupby("player")[[f"{z}_ratio" for z in zones]].mean().reset_index()
    fig = px.bar(bar_df, x="player", y=[f"{z}_ratio" for z in zones],
                 title="Heart Rate Zone Distribution", barmode="stack")
    st.plotly_chart(fig, use_container_width=True)

def plot_heart_rate_regression(df: pd.DataFrame):
    st.markdown("##### Regression: Heart Rate Zones vs. Training Load")
    for i in range(1, 6):
        col = f"hr_zone_{i}_hms"
        df[f"{col}_ratio"] = df[col] / df["day_duration"]
        fig = px.scatter(df, x=f"{col}_ratio", y="training_load",
                         trendline="ols", title=f"Zone {i} Ratio vs. Training Load")
        st.plotly_chart(fig, use_container_width=True)

def plot_heart_rate_radar(df: pd.DataFrame):
    st.markdown("##### Radar: Heart Rate Feature Importance")
    X = df[[f"hr_zone_{i}_hms" for i in range(1, 6)]].fillna(0)
    y = df["training_load"]
    model = RandomForestRegressor()
    model.fit(X, y)
    importances = model.feature_importances_
    fig = go.Figure(go.Scatterpolar(
        r=importances,
        theta=X.columns,
        fill='toself',
        name='Feature Importance'
    ))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# ============= PLAYER COMPARISON ======================

def plot_gps_player_comparison(df: pd.DataFrame):
    st.markdown("### Compare Two Players Over Time")
    player_list = sorted(df["player"].unique())
    player1 = st.selectbox("Player 1", player_list, key="gps_comp_1")
    player2 = st.selectbox("Player 2", player_list, key="gps_comp_2")
    
    compare_df = df[df["player"].isin([player1, player2])]
    compare_df = compare_df.sort_values("date")
    
    metrics = ["distance", "accel_decel_total", "day_duration", "training_load"]
    for metric in metrics:
        fig = px.line(compare_df, x="date", y=metric, color="player", title=f"{metric} over Time")
        st.plotly_chart(fig, use_container_width=True)
