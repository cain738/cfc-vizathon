# ipa_page.py (in app/pages)
import streamlit as st
from analysis.data_loader import load_ipa_data
from charts.ipa_charts import (
    plot_ipa_category_distribution,
    plot_ipa_type_pie,
    plot_ipa_heatmap,
    plot_tracking_status_stacked_bar,
    plot_ipa_timeline_chart,
    plot_player_radar_chart,
    plot_player_comparison_table
)
from utils.ui_styling import load_local_css
load_local_css()
def show_ipa_page():
    # st.set_page_config(layout="wide")
    st.sidebar.image("app/static/chelsea_logo.png", width=120)
    st.title("📌 Individual Priority Areas (IPA) Dashboard")

    df = load_ipa_data()
    players = sorted(df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players)
    df = df[df["player"].isin(selected_players)]

    tab1, tab2, tab3 = st.tabs([
        "🧭 Overview",
        "📊 Tracking & Timelines",
        "👥 Player Comparisons"
    ])

    with tab1:
        st.subheader("IPA Distribution Overview")
        col1, col2 = st.columns(2)
        with col1:
            plot_ipa_category_distribution(df)
        with col2:
            plot_ipa_type_pie(df)
        st.markdown("---")
        plot_ipa_heatmap(df)

    with tab2:
        st.subheader("Goal Progress and Timelines")
        plot_tracking_status_stacked_bar(df)
        plot_ipa_timeline_chart(df)

    with tab3:
        st.subheader("Player-Level Comparison")
        plot_player_radar_chart(df, selected_players)
        plot_player_comparison_table(df, selected_players)

if __name__ == "__main__":
    show_ipa_page()
