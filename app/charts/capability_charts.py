import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# ========= 1. Feature Importance by Movement Type =========

def plot_feature_importance_by_movement(df: pd.DataFrame, movement_type: str):
    st.markdown(f"##### Feature Importance for BenchmarkPct — {movement_type}")
    
    filtered_df = df[df["movement"].str.lower() == movement_type.lower()].dropna(subset=["BenchmarkPct"])
    if filtered_df.empty:
        st.warning(f"No data available for movement: {movement_type}")
        return
    
    features = ["quality", "expression", "position", "is_md_minus_1"]
    target = "BenchmarkPct"

    # Encode categorical variables
    preprocessor = ColumnTransformer(transformers=[
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["quality", "expression", "position"])
    ], remainder="passthrough")

    model = Pipeline(steps=[
        ("pre", preprocessor),
        ("rf", RandomForestRegressor(random_state=42))
    ])

    model.fit(filtered_df[features], filtered_df[target])
    rf = model.named_steps["rf"]

    # Get feature names from transformer
    ohe = model.named_steps["pre"].named_transformers_["cat"]
    encoded_labels = ohe.get_feature_names_out(["quality", "expression", "position"])
    final_features = list(encoded_labels) + ["is_md_minus_1"]

    fig = px.bar(
        x=rf.feature_importances_,
        y=final_features,
        orientation="h",
        title=f"Random Forest Feature Importance for {movement_type}"
    )
    st.plotly_chart(fig, use_container_width=True)

# ========= 2. Player Rankings =========

def plot_player_rankings(df: pd.DataFrame):
    st.markdown("##### Player Rankings by Avg. BenchmarkPct")
    ranking_df = df.groupby("player")["BenchmarkPct"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(ranking_df, x="player", y="BenchmarkPct", title="Avg. BenchmarkPct by Player")
    st.plotly_chart(fig, use_container_width=True)

# ========= 3. Player Comparison =========

def plot_player_comparison(df: pd.DataFrame):
    st.markdown("##### Compare Two Players on BenchmarkPct Over Time")
    players = sorted(df["player"].unique())
    p1 = st.selectbox("Player 1", players, key="cap_p1")
    p2 = st.selectbox("Player 2", players, key="cap_p2")
    compare_df = df[df["player"].isin([p1, p2])].sort_values("date")
    fig = px.line(compare_df, x="date", y="BenchmarkPct", color="player", title="BenchmarkPct Timeline")
    st.plotly_chart(fig, use_container_width=True)

# ========= 4. Merged Capability + Recovery Analysis =========

def plot_merged_capability_recovery(df: pd.DataFrame):
    st.markdown("##### Capability vs Recovery Composite")

    if "Sleep_composite" not in df.columns:
        st.warning("Merged recovery metrics not found.")
        return

    # Drop rows with missing values in key metrics
    sub = df.dropna(subset=["BenchmarkPct", "Sleep_composite"])

    fig = px.scatter(
        sub,
        x="Sleep_composite",
        y="BenchmarkPct",
        color="movement",
        title="BenchmarkPct vs Sleep Composite (by Movement)"
    )
    st.plotly_chart(fig, use_container_width=True)
