# app/pages/ipa_page.py

import streamlit as st
from utils.ui_styling import load_local_css
from analysis.data_loader import load_ipa_data
from charts.ipa_charts import (
    plot_performance_stacked_charts,
    plot_recovery_stacked_charts,
    plot_performance_importance_radar,
    plot_recovery_importance_radar,
    plot_ipa_player_rankings,
    plot_ipa_comparison_view
)

load_local_css()

def show_ipa_page():
    st.title("📌 Individual Priority Areas (IPA) Dashboard")

    df = load_ipa_data()
    players = sorted(df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players)
    df = df[df["player"].isin(selected_players)]

    tab1, tab2, tab3 = st.tabs([
        "⚽ Performance Goals", "♻️ Recovery Goals", "📊 Comparison & Rankings"
    ])

    with tab1:
        st.subheader("Tracking Status Across Performance Goals")
        plot_performance_stacked_charts(df)
        plot_performance_importance_radar(df)

    with tab2:
        st.subheader("Tracking Status Across Recovery Goals")
        plot_recovery_stacked_charts(df)
        plot_recovery_importance_radar(df)

    with tab3:
        st.subheader("IPA Ranking and Comparison")
        plot_ipa_player_rankings(df)
        plot_ipa_comparison_view(df)

if __name__ == "__main__":
    show_ipa_page()
