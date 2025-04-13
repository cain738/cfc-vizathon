# capability_page.py (in app/pages)
import streamlit as st
from analysis.data_loader import load_capability_data
from feature_engineering.data_wrangler import load_capability_recovery_merged_data
from analysis.advanced_analysis import compute_movement_recovery_correlations
from charts.capability_charts import (
    plot_avg_benchmark_by_movement,
    plot_movement_trend,
    plot_movement_boxplot,
    plot_movement_heatmap,
    plot_expression_box,
    plot_player_expression_bar,
    plot_expression_trend,
    plot_quality_heatmap,
    plot_quality_scatter,
    plot_quality_trend,
    plot_player_rankings,
    plot_capability_vs_recovery,
    plot_combined_heatmap,
    plot_movement_recovery_correlation_heatmap
)
from utils.ui_styling import load_local_css
load_local_css()

def show_capability_page():
    # st.set_page_config(layout="wide")
    st.sidebar.image("app/static/chelsea_logo.png", width=120)
    st.title("🏋️ Physical Capability Dashboard")

    # 1) Load + filter data
    df = load_capability_data()
    players = sorted(df["player"].unique())
    selected_players = st.sidebar.multiselect("Select Player(s)", players, default=players)
    df = df[df["player"].isin(selected_players)]

    # 2) Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏃 Movement Overview",
        "⚖️ Expression Analysis",
        "⚙️ Quality Insights",
        "🔗 Merged Analysis",
        "📊 Player Ranking"
    ])

    # --- MOVEMENT OVERVIEW TAB ---
    with tab1:
        st.subheader("Movement-Based Performance (2×2 layout)")
        col1, col2 = st.columns(2)
        with col1:
            plot_avg_benchmark_by_movement(df)
        with col2:
            plot_movement_trend(df)

        col3, col4 = st.columns(2)
        with col3:
            plot_movement_boxplot(df)
        with col4:
            plot_movement_heatmap(df)

    # --- EXPRESSION ANALYSIS TAB ---
    with tab2:
        st.subheader("Expression Analysis (2×2 layout)")
        col1, col2 = st.columns(2)
        with col1:
            plot_expression_box(df)
        with col2:
            plot_player_expression_bar(df)

        col3, col4 = st.columns(2)
        with col3:
            plot_expression_trend(df)
        with col4:
            # If you want a 4th chart, e.g. a radar or other advanced chart:
            st.info("Add a 4th expression chart here if desired.")

    # --- QUALITY INSIGHTS TAB ---
    with tab3:
        st.subheader("Quality Insights (2×2 layout)")
        col1, col2 = st.columns(2)
        with col1:
            plot_quality_heatmap(df)
        with col2:
            plot_quality_scatter(df)

        col3, col4 = st.columns(2)
        with col3:
            plot_quality_trend(df)
        with col4:
            st.info("Add an optional 4th chart or summary table here.")
    
    # --- TAB 4: Merged Analysis (Capability + Recovery) ---
    with tab4:
        st.subheader("Merged Capability and Recovery Analysis")
        
        df_merged, output_path = load_capability_recovery_merged_data()

        if df_merged is not None and not df_merged.empty:
            st.markdown("#### Capability vs Recovery Scatter")
            plot_capability_vs_recovery(df_merged)
            st.markdown("#### Combined Heatmap (Capability) Based on Merged Data")
            plot_combined_heatmap(df_merged)
        else:
            st.warning("Merged data is not available or empty.")
        
        st.subheader("Advanced Movement-Recovery Analysis")
        corr_df = compute_movement_recovery_correlations()
        plot_movement_recovery_correlation_heatmap(corr_df)
    
    # --- TAB 5: Player Ranking (filters for movement, quality, and expression)
    with tab5:
        st.subheader("Rank Players on Movement Metrics")
        # In-page filters: Movement, Quality, Expression
        all_movements = sorted(df["movement"].unique())
        all_movements.insert(0, "All")
        selected_movement = st.selectbox("Select Movement", all_movements, key="rank_movement")
        all_qualities = sorted(df["quality"].unique())
        all_qualities.insert(0, "All")
        selected_quality = st.selectbox("Select Quality", all_qualities, key="rank_quality")
        all_expressions = sorted(df["expression"].unique())
        all_expressions.insert(0, "All")
        selected_expression = st.selectbox("Select Expression", all_expressions, key="rank_expression")
        
        plot_player_rankings(df, selected_movement, selected_quality, selected_expression)

if __name__ == "__main__":
    show_capability_page()
