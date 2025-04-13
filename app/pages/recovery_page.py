# recovery_page.py (in app/pages)
import streamlit as st
from analysis.data_loader import load_recovery_data
from analysis.advanced_analysis import compute_recovery_feature_importances
from charts.recovery_charts import (
    show_avg_recovery_line,
    show_emboss_trend,
    show_stacked_domain_area,
    show_player_domain_line,
    show_recovery_box,
    show_recovery_violin,
    show_avg_bar_by_player,
    show_day_by_domain_heatmap,
    show_domain_correlation_heatmap,
    show_player_date_heatmap,
    show_matchday_impact_heatmap,
    show_emboss_momentum_heatmap,
    show_feature_importances,
    show_player_comparison_overview
)
from utils.ui_styling import load_local_css
load_local_css()


def show_recovery_page():
    # st.set_page_config(layout="wide")
    st.sidebar.image("app/static/chelsea_logo.png", width=120)
    st.title("💪 Recovery Status Dashboard")

    df = load_recovery_data()

    # Player filter
    players = sorted(df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players)
    df = df[df["player"].isin(selected_players)]

    # Main Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 Daily Trends",
        "📊 Domain Distribution",
        "🌡️ Heatmaps",
        "👤 Player Comparison"
    ])

    with tab1:
        st.subheader("Recovery Trends Over Time")
        show_avg_recovery_line(df)
        show_emboss_trend(df)
        show_stacked_domain_area(df)
        show_player_domain_line(df)

    with tab2:
        st.subheader("Recovery Score Distribution")
        show_recovery_box(df)
        show_recovery_violin(df)
        show_avg_bar_by_player(df, chart_key="avg_bar_main_tab")

    with tab3:
        st.subheader("Heatmaps for Recovery")
        fi_df, df_model = compute_recovery_feature_importances()
        
        show_feature_importances(fi_df)
        show_day_by_domain_heatmap(df)
        show_domain_correlation_heatmap(df)
        show_player_date_heatmap(df)
        show_matchday_impact_heatmap(df_model)
        show_emboss_momentum_heatmap(df_model)
        # show_recovery_heatmap(df)
        # show_emboss_heatmap(df)

    with tab4:
        st.subheader("Compare Players")
        show_player_comparison_overview(df)

if __name__ == "__main__":
    show_recovery_page()
