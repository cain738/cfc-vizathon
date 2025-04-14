# app/pages/capability_page.py

import streamlit as st
from utils.ui_styling import load_local_css
from analysis.data_loader import load_capability_data, load_recovery_data, load_calendar_data
from feature_engineering.data_wrangler import (
    merge_capability_with_calendar,
    merge_capability_with_recovery
)
from charts.capability_charts import (
    plot_feature_importance_by_movement,
    plot_player_rankings,
    plot_player_comparison,
    plot_merged_capability_recovery
)

load_local_css()

def show_capability_page():
    st.title("🏋️ Physical Capability Dashboard")

    # Load & merge data
    cap_df = load_capability_data()
    cal_df = load_calendar_data()
    recovery_df = load_recovery_data()
    cap_df = merge_capability_with_calendar(cap_df, cal_df)
    cap_recovery_df = merge_capability_with_recovery(cap_df, recovery_df)

    # Sidebar filters
    players = sorted(cap_df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players)
    cap_df = cap_df[cap_df["player"].isin(selected_players)]
    cap_recovery_df = cap_recovery_df[cap_recovery_df["player"].isin(selected_players)]

    # Tabs
    tabs = st.tabs([
        "🌀 Agility", "🚀 Sprint", "🧱 Upper Body", "🦵 Jump",
        "📊 Player Rankings", "🔗 Capability + Recovery"
    ])

    movement_types = ["Agility", "Sprint", "Upper Body", "Jump"]

    # Tab 0 to 3 — Individual Movement Tabs
    for idx, movement in enumerate(movement_types):
        with tabs[idx]:
            st.subheader(f"{movement} Capability Analysis")
            plot_feature_importance_by_movement(cap_df, movement)

    # Player Rankings
    with tabs[4]:
        st.subheader("Compare or Rank Players")
        plot_player_rankings(cap_df)
        plot_player_comparison(cap_df)

    # Merged Capability + Recovery
    with tabs[5]:
        st.subheader("Capability vs. Recovery Context")
        plot_merged_capability_recovery(cap_recovery_df)

if __name__ == "__main__":
    show_capability_page()
