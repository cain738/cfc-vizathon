# recovery_charts.py (in app/charts)
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# --- DAILY TRENDS ---
def show_avg_recovery_line(df: pd.DataFrame, title_suffix=""):
    fig = px.line(
        df,
        x="date",
        y=["Bio_composite", "Msk_joint_range_composite", "Subjective_composite", "Sleep_composite"],
        color_discrete_sequence=px.colors.qualitative.Set2,
        title=f"Daily Recovery Metrics by Domain {title_suffix}"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_emboss_trend(df: pd.DataFrame, title_suffix=""):
    fig = px.line(
        df,
        x="date",
        y="emboss_baseline_score",
        color="player",
        title=f"EMBOSS Baseline Score Over Time {title_suffix}"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_stacked_domain_area(df: pd.DataFrame):
    df_area = df.set_index("date")[[
        "Bio_composite", "Msk_joint_range_composite", "Subjective_composite", "Sleep_composite"
    ]].groupby("date").mean()
    fig = go.Figure()
    for col in df_area.columns:
        fig.add_trace(go.Scatter(x=df_area.index, y=df_area[col], stackgroup='one', name=col))
    fig.update_layout(title="Average Domain Scores - Stacked Area Chart")
    st.plotly_chart(fig, use_container_width=True)

def show_player_domain_line(df: pd.DataFrame):
    cols = st.columns(2)
    domain_keys = [
        "Bio_composite",
        "Msk_joint_range_composite",
        "Subjective_composite",
        "Sleep_composite"
    ]
    for i, domain in enumerate(domain_keys):
        fig = px.line(df, x="date", y=domain, color="player", title=f"{domain} Over Time")
        with cols[i % 2]:
            st.plotly_chart(fig, use_container_width=True, key=f"line_chart_{domain}_{i}")

# --- DOMAIN DISTRIBUTION ---
def show_recovery_box(df: pd.DataFrame):
    melted = df.melt(id_vars=["player"],
                     value_vars=["Bio_composite", "Msk_joint_range_composite", "Subjective_composite", "Sleep_composite"],
                     var_name="Domain", value_name="Score")
    fig = px.box(melted, x="Domain", y="Score", color="player",
                 title="Recovery Score Distribution by Domain")
    st.plotly_chart(fig, use_container_width=True)

def show_recovery_violin(df: pd.DataFrame):
    melted = df.melt(id_vars=["player"],
                     value_vars=["Bio_composite", "Msk_joint_range_composite", "Subjective_composite", "Sleep_composite"],
                     var_name="Domain", value_name="Score")
    fig = px.violin(melted, x="Domain", y="Score", color="player",
                    box=True, points="all", title="Recovery Variability by Domain")
    st.plotly_chart(fig, use_container_width=True)

def show_avg_bar_by_player(df: pd.DataFrame, chart_key: str = "avg_domain_scores_bar"):
    melted = df.melt(
        id_vars=["player"],
        value_vars=["Bio_composite", "Msk_joint_range_composite", "Subjective_composite", "Sleep_composite"],
        var_name="Domain",
        value_name="Score"
    )
    avg_scores = melted.groupby(["player", "Domain"])['Score'].mean().reset_index()
    fig = px.bar(
        avg_scores,
        x="player",
        y="Score",
        color="Domain",
        barmode="group",
        title="Average Domain Scores per Player"
    )
    # Pass the unique chart_key here
    st.plotly_chart(fig, use_container_width=True, key=chart_key)

# --- HEATMAPS ---
# def show_recovery_heatmap(df: pd.DataFrame):
#     melted = df.melt(id_vars=["player"],
#                      value_vars=["Bio_composite", "Msk_joint_range_composite", "Subjective_composite", "Sleep_composite"],
#                      var_name="Domain", value_name="Score")
#     heat_df = melted.groupby(["player", "Domain"])['Score'].mean().reset_index()
#     pivot = heat_df.pivot(index="player", columns="Domain", values="Score")
#     fig = go.Figure(data=go.Heatmap(
#         z=pivot.values,
#         x=pivot.columns,
#         y=pivot.index,
#         colorscale="Viridis",
#         colorbar=dict(title="Avg Score")
#     ))
#     fig.update_layout(title="Avg Recovery Score per Player by Domain",
#                       xaxis_title="Domain", yaxis_title="Player")
#     st.plotly_chart(fig, use_container_width=True)

def show_feature_importances(fi_df: pd.DataFrame):
    """
    Renders both a bar chart and a single-row heatmap of feature importances.
    fi_df must have columns ['feature', 'importance'].
    """

    st.subheader("Feature Importances for EMBOSS Score")

    # # 1) Bar chart
    # fig_bar = px.bar(
    #     fi_df,
    #     x="feature",
    #     y="importance",
    #     title="Feature Importances (Bar)",
    #     labels={"feature": "Feature", "importance": "Importance"},
    # )
    # st.plotly_chart(fig_bar, use_container_width=True)

    # 2) Single-row heatmap
    # We'll pivot so each feature is a column, the single row is the 'importance'.
    pivot = fi_df.set_index("feature").T  # shape => (1, #features)
    fig_heat = go.Figure(data=go.Heatmap(
        z=[pivot.loc["importance"].values],  # one row
        x=pivot.columns,
        y=["Importance"],  # single row label
        colorscale="Blues",
        colorbar=dict(title="Importance")
    ))
    fig_heat.update_layout(
        title="Feature Importances (Heatmap)",
        xaxis_title="Features",
        yaxis_title=""
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    
def show_day_by_domain_heatmap(df):
    # 1) Group by date
    daily_means = df.groupby("date")[
        ["Bio_composite", "Msk_joint_range_composite", "Subjective_composite", "Sleep_composite"]
    ].mean().reset_index()

    # 2) Melt
    melted = daily_means.melt(id_vars="date", var_name="Domain", value_name="Score")

    # 3) Pivot
    pivot = melted.pivot(index="date", columns="Domain", values="Score")

    # 4) Heatmap
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="Viridis",
        colorbar=dict(title="Avg Score")
    ))
    fig.update_layout(
        title="Mean Domain Scores by Day",
        xaxis_title="Domain",
        yaxis_title="Date"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_domain_correlation_heatmap(df):
    # Subset columns
    subset = df[[
        "Bio_composite",
        "Msk_joint_range_composite",
        "Subjective_composite",
        "Sleep_composite",
        "emboss_baseline_score"
    ]].dropna()

    corr_matrix = subset.corr(method="pearson")  # or "spearman"

    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale="RdBu",
        colorbar=dict(title="Correlation"),
        zmin=-1, zmax=1
    ))
    fig.update_layout(
        title="Domain-to-Domain Correlation Heatmap",
        xaxis_title="Variable",
        yaxis_title="Variable"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_emboss_heatmap(df: pd.DataFrame):
    pivot = df.pivot(index="date", columns="player", values="emboss_baseline_score")
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="RdBu",
        colorbar=dict(title="EMBOSS")
    ))
    fig.update_layout(title="EMBOSS Scores Over Time", xaxis_title="Player", yaxis_title="Date")
    st.plotly_chart(fig, use_container_width=True)
    
def show_player_date_heatmap(df: pd.DataFrame, domain="Sleep_composite"):
    st.subheader(f"{domain} Score Heatmap (Player vs Date)")
    df = df.dropna(subset=[domain])
    pivot = df.pivot(index="player", columns="date", values=domain)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="Viridis",
        colorbar=dict(title="Score")
    ))
    fig.update_layout(
        title=f"{domain} Scores by Player and Date",
        xaxis_title="Date",
        yaxis_title="Player"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_matchday_impact_heatmap(df: pd.DataFrame, value_col="emboss_baseline_score"):
    st.subheader(f"Matchday Impact on {value_col}")
    df = df.copy()
    df["day_type"] = "non_matchday"
    df.loc[df["md_minus_1"] == 1, "day_type"] = "md_minus_1"
    df.loc[df["md_plus_1"] == 1, "day_type"] = "md_plus_1"
    avg = df.groupby(["player", "day_type"])[value_col].mean().reset_index()
    pivot = avg.pivot(index="player", columns="day_type", values=value_col)
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="Cividis",
        colorbar=dict(title="Avg Score")
    ))
    fig.update_layout(
        title=f"Average {value_col} by Matchday Context",
        xaxis_title="Day Type",
        yaxis_title="Player"
    )
    st.plotly_chart(fig, use_container_width=True)

def show_emboss_momentum_heatmap(df: pd.DataFrame):
    st.subheader("EMBOSS Momentum (3-day Rolling Avg)")
    df_sorted = df.sort_values(["player", "date"]).copy()
    df_sorted["rolling_emboss"] = df_sorted.groupby("player")["emboss_baseline_score"].transform(lambda x: x.rolling(3).mean())
    pivot = df_sorted.pivot(index="date", columns="player", values="rolling_emboss")
    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale="Plasma",
        colorbar=dict(title="3-Day Avg")
    ))
    fig.update_layout(
        title="Rolling 3-Day Average of EMBOSS Score",
        xaxis_title="Player",
        yaxis_title="Date"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- PLAYER COMPARISON ---
def show_player_comparison_overview(df: pd.DataFrame):
    players = sorted(df["player"].unique())
    player = st.selectbox("Select a Player", players, key="compare_player")
    date_range = st.date_input("Select Date Range", [df["date"].min(), df["date"].max()], key="compare_date")

    filtered = df[(df["player"] == player) &
                  (df["date"] >= pd.to_datetime(date_range[0])) &
                  (df["date"] <= pd.to_datetime(date_range[1]))]

    st.markdown(f"### {player} Recovery Summary")
    show_avg_recovery_line(filtered, title_suffix=f"for {player}")
    show_emboss_trend(filtered, title_suffix=f"for {player}")
