# ipa_charts.py (in app/charts)
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# --- Overview Tab Charts ---
def plot_ipa_category_distribution(df):
    fig = px.bar(
        df.groupby("priority_category").size().reset_index(name="count"),
        x="priority_category", y="count", color="priority_category",
        title="IPA Goals by Priority Category"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_ipa_type_pie(df):
    fig = px.pie(
        df, names="type", title="Habit vs Outcome Goal Distribution",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_ipa_heatmap(df):
    pivot = df.groupby(["player", "priority_category"]).size().unstack(fill_value=0)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="Viridis",
        colorbar=dict(title="Goal Count")
    ))
    fig.update_layout(
        title="IPA Distribution by Player and Category",
        xaxis_title="Priority Category",
        yaxis_title="Player"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- Tracking & Timelines Tab ---
def plot_tracking_status_stacked_bar(df):
    df_group = df.groupby(["priority_category", "tracking_status"]).size().reset_index(name="count")
    fig = px.bar(
        df_group,
        x="priority_category", y="count", color="tracking_status",
        title="Tracking Status by Category",
        barmode="stack"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_ipa_timeline_chart(df):
    if "target_set_date" in df and "review_date" in df:
        df_sorted = df.dropna(subset=["target_set_date", "review_date"]).sort_values("player")
        fig = px.timeline(
            df_sorted,
            x_start="target_set_date",
            x_end="review_date",
            y="player",
            color="priority_category",
            title="IPA Timeline by Player"
        )
        fig.update_yaxes(autorange="reversed")
        st.plotly_chart(fig, use_container_width=True)

# --- Player Comparisons Tab ---
def plot_player_radar_chart(df, selected_players):
    if not selected_players:
        st.info("Please select at least one player to display radar chart.")
        return
    radar_df = df[df["player"].isin(selected_players)]
    category_count = radar_df.groupby(["player", "priority_category"]).size().unstack(fill_value=0)
    categories = list(category_count.columns)
    fig = go.Figure()
    for player in category_count.index:
        fig.add_trace(go.Scatterpolar(
            r=category_count.loc[player].values,
            theta=categories,
            fill='toself',
            name=player
        ))
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=True)),
        title="Player IPA Category Radar Chart"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_player_comparison_table(df, selected_players):
    if not selected_players:
        return
    filtered = df[df["player"].isin(selected_players)]
    summary = filtered.groupby(["player", "tracking_status"]).size().unstack(fill_value=0)
    st.markdown("### Player IPA Status Summary")
    st.dataframe(summary)
