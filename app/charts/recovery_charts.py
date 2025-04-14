# app/charts/recovery_charts.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestRegressor

# ============ COMPLETENESS ==================

def plot_completeness_radar(df):
    st.markdown("##### Feature Importance Radar (Completeness → EMBOSS)")
    features = [
        "Bio_completeness", "Msk_joint_range_completeness", "Msk_load_tolerance_completeness",
        "Subjective_completeness", "Soreness_completeness", "Sleep_completeness"
    ]
    df = df.dropna(subset=features + ["emboss_baseline_score"])
    X = df[features]
    y = df["emboss_baseline_score"]

    model = RandomForestRegressor()
    model.fit(X, y)
    importances = model.feature_importances_

    fig = go.Figure(go.Scatterpolar(
        r=importances,
        theta=features,
        fill='toself'
    ))
    fig.update_layout(title="Completeness Metrics Importance", polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig, use_container_width=True)


def plot_completeness_heatmap(df):
    st.markdown("##### Correlation Heatmap")
    features = [
        "Bio_completeness", "Msk_joint_range_completeness", "Msk_load_tolerance_completeness",
        "Subjective_completeness", "Soreness_completeness", "Sleep_completeness",
        "emboss_baseline_score"
    ]
    subset = df[features].dropna()
    fig = px.imshow(subset.corr(), text_auto=True, title="Completeness vs. EMBOSS Correlation")
    st.plotly_chart(fig, use_container_width=True)


def plot_completeness_scatter(df):
    st.markdown("##### Subjective Completeness vs. EMBOSS")
    fig = px.scatter(df, x="Subjective_completeness", y="emboss_baseline_score", color="player")
    st.plotly_chart(fig, use_container_width=True)


# ============ COMPOSITE ==================

def plot_composite_radar(df):
    st.markdown("##### Feature Importance Radar (Composite → EMBOSS)")
    features = [
        "Bio_composite", "Msk_joint_range_composite", "Msk_load_tolerance_composite",
        "Subjective_composite", "Soreness_composite", "Sleep_composite"
    ]
    df = df.dropna(subset=features + ["emboss_baseline_score"])
    X = df[features]
    y = df["emboss_baseline_score"]

    model = RandomForestRegressor()
    model.fit(X, y)
    importances = model.feature_importances_

    fig = go.Figure(go.Scatterpolar(
        r=importances,
        theta=features,
        fill='toself'
    ))
    fig.update_layout(title="Composite Metrics Importance", polar=dict(radialaxis=dict(visible=True)))
    st.plotly_chart(fig, use_container_width=True)


def plot_composite_heatmap(df):
    st.markdown("##### Correlation Heatmap")
    features = [
        "Bio_composite", "Msk_joint_range_composite", "Msk_load_tolerance_composite",
        "Subjective_composite", "Soreness_composite", "Sleep_composite",
        "emboss_baseline_score"
    ]
    subset = df[features].dropna()
    fig = px.imshow(subset.corr(), text_auto=True, title="Composite vs. EMBOSS Correlation")
    st.plotly_chart(fig, use_container_width=True)


def plot_composite_scatter(df):
    st.markdown("##### Subjective Composite vs. EMBOSS")
    fig = px.scatter(df, x="Subjective_composite", y="emboss_baseline_score", color="player")
    st.plotly_chart(fig, use_container_width=True)

# ============ COMPARISON ==================

def plot_recovery_rankings(df):
    st.markdown("##### Player Rankings (Avg. EMBOSS)")
    ranking_df = df.groupby("player")["emboss_baseline_score"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(ranking_df, x="player", y="emboss_baseline_score", title="Player Recovery Rankings")
    st.plotly_chart(fig, use_container_width=True)

def plot_recovery_player_comparison(df):
    st.markdown("##### Compare 2 Players' Recovery")
    players = sorted(df["player"].unique())
    p1 = st.selectbox("Player 1", players, key="rec_p1")
    p2 = st.selectbox("Player 2", players, key="rec_p2")

    compare_df = df[df["player"].isin([p1, p2])].sort_values("date")
    fig = px.line(compare_df, x="date", y="emboss_baseline_score", color="player", title="EMBOSS Score Over Time")
    st.plotly_chart(fig, use_container_width=True)