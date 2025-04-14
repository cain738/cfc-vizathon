import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder

# ============ 1. Performance Tracking Charts ============

def plot_performance_stacked_charts(df: pd.DataFrame):
    st.markdown("##### Tracking Distribution for Performance Areas")

    performance_df = df[df["priority_category"].str.lower() == "performance"]

    if performance_df.empty:
        st.warning("No performance IPA data available.")
        return

    for area in performance_df["area"].unique():
        area_df = performance_df[performance_df["area"] == area]
        plot = area_df.groupby(["player", "tracking_status"]).size().unstack().fillna(0)
        fig = px.bar(plot, title=f"{area} Tracking Status", barmode="stack")
        st.plotly_chart(fig, use_container_width=True)

# ============ 2. Performance Radar ============

def plot_performance_importance_radar(df: pd.DataFrame):
    st.markdown("##### Feature Importance Radar (Performance IPAs → Target Performance)")

    filtered = df[df["priority_category"].str.lower() == "performance"].copy()

    if filtered.empty:
        st.warning("No performance IPAs found.")
        return

    categorical_features = ["area", "type"]
    encoded = pd.get_dummies(filtered[categorical_features], drop_first=False)

    y = filtered["tracking_status"].astype("category").cat.codes

    model = RandomForestClassifier()
    model.fit(encoded, y)

    fig = go.Figure(go.Scatterpolar(
        r=model.feature_importances_,
        theta=encoded.columns,
        fill='toself'
    ))
    fig.update_layout(title="Performance IPA Importance", polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig, use_container_width=True)

# ============ 3. Recovery Tracking Charts ============

def plot_recovery_stacked_charts(df: pd.DataFrame):
    st.markdown("##### Tracking Distribution for Recovery Areas")

    recovery_df = df[df["priority_category"].str.lower() == "recovery"]

    if recovery_df.empty:
        st.warning("No recovery IPA data available.")
        return

    for area in recovery_df["area"].unique():
        area_df = recovery_df[recovery_df["area"] == area]
        plot = area_df.groupby(["player", "tracking_status"]).size().unstack().fillna(0)
        fig = px.bar(plot, title=f"{area} Tracking Status", barmode="stack")
        st.plotly_chart(fig, use_container_width=True)

# ============ 4. Recovery Radar ============

def plot_recovery_importance_radar(df: pd.DataFrame):
    st.markdown("##### Feature Importance Radar (Recovery IPAs → Target Performance)")

    filtered = df[df["priority_category"].str.lower() == "recovery"].copy()

    if filtered.empty:
        st.warning("No recovery IPAs found.")
        return

    categorical_features = ["area", "type"]
    encoded = pd.get_dummies(filtered[categorical_features], drop_first=False)

    y = filtered["tracking_status"].astype("category").cat.codes

    model = RandomForestClassifier()
    model.fit(encoded, y)

    fig = go.Figure(go.Scatterpolar(
        r=model.feature_importances_,
        theta=encoded.columns,
        fill='toself'
    ))
    fig.update_layout(title="Recovery IPA Importance", polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig, use_container_width=True)

# ============ 5. Player Rankings ============

def plot_ipa_player_rankings(df: pd.DataFrame):
    st.markdown("##### Player Rankings by IPA Achievement Rate")
    
    print(df.columns)

    achievement_rates = (
        df.groupby("player")["tracking_status"]
        .apply(lambda x: (x == "Achieved").sum() / len(x))
        .reset_index(name="achievement_rate")
        .sort_values(by="achievement_rate", ascending=False)
    )

    fig = px.bar(achievement_rates, x="player", y="achievement_rate", title="Goal Achievement Rate by Player")
    st.plotly_chart(fig, use_container_width=True)

# ============ 6. Player Comparison ============

def plot_ipa_comparison_view(df: pd.DataFrame):
    st.markdown("##### Compare Two Players on IPA Goal Achievements")
    
    print(df.columns)

    players = sorted(df["player"].unique())
    p1 = st.selectbox("Player 1", players, key="ipa_p1")
    p2 = st.selectbox("Player 2", players, key="ipa_p2")

    goals = df["area"].unique()

    p1_data = df[(df["player"] == p1) & (df["tracking_status"] == "Achieved")]["area"].value_counts()
    p2_data = df[(df["player"] == p2) & (df["tracking_status"] == "Achieved")]["area"].value_counts()

    compare_df = pd.DataFrame({
        "area": goals,
        p1: [p1_data.get(area, 0) for area in goals],
        p2: [p2_data.get(area, 0) for area in goals]
    })

    compare_df = compare_df.melt(id_vars="area", var_name="Player", value_name="Achieved Count")
    fig = px.bar(compare_df, x="area", y="Achieved Count", color="Player", barmode="group", title="IPA Area Achievement Comparison")
    st.plotly_chart(fig, use_container_width=True)
