# capability_charts.py (in app/charts)
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# --- MOVEMENT OVERVIEW ---
def plot_avg_benchmark_by_movement(df):
    """
    Bar chart:
    X = movement, Y = mean BenchmarkPct, color = player
    """
    grouped = df.groupby(["player", "movement"])["BenchmarkPct"].mean().reset_index()
    fig = px.bar(
        grouped,
        x="movement",
        y="BenchmarkPct",
        color="player",
        barmode="group",
        title="Average Benchmark % by Movement per Player"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_movement_trend(df):
    """
    Line chart:
    X = date, Y = BenchmarkPct, color = movement
    Focus on top movements or all movements.
    """
    fig = px.line(
        df,
        x="date",
        y="BenchmarkPct",
        color="movement",
        title="Benchmark % Over Time by Movement"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_movement_boxplot(df):
    """
    Box plot:
    movement on X, BenchmarkPct on Y, color = movement
    """
    fig = px.box(
        df, 
        x="movement", 
        y="BenchmarkPct", 
        color="movement",
        title="Movement Performance Distribution"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_movement_heatmap(df):
    """
    Heatmap pivot:
    Rows = player, Columns = movement, Values = avg BenchmarkPct
    """
    pivot = df.groupby(["player", "movement"])["BenchmarkPct"].mean().reset_index()
    pivot = pivot.pivot(index="player", columns="movement", values="BenchmarkPct")

    custom_scale = [[0, "#034694"], [0.5, "#D69A00"], [1, "#FAF8F0"]]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=custom_scale,
        colorbar=dict(title="Avg Benchmark %")
    ))
    fig.update_layout(title="Avg Benchmark % by Movement and Player")
    st.plotly_chart(fig, use_container_width=True)

# --- EXPRESSION ANALYSIS ---
def plot_expression_box(df):
    """
    Violin or box plot to compare Isometric vs Dynamic
    Possibly color by movement or expression
    """
    fig = px.violin(
        df, 
        x="expression", 
        y="BenchmarkPct", 
        color="movement",
        box=True, 
        points="all",
        title="Expression Distribution by Movement"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_player_expression_bar(df):
    """
    Bar chart:
    X = player, Y = avg BenchmarkPct, color = expression
    """
    grouped = df.groupby(["player", "expression"])["BenchmarkPct"].mean().reset_index()
    fig = px.bar(
        grouped,
        x="player",
        y="BenchmarkPct",
        color="expression",
        barmode="group",
        title="Avg Benchmark % by Expression per Player",
        color_discrete_sequence=["#034694", "#D69A00", "#022E6E", "#F0F2F6"]  # Customize as needed

    )
    st.plotly_chart(fig, use_container_width=True)

def plot_expression_trend(df):
    """
    Time-series line:
    X = date, Y = BenchmarkPct, color = expression
    """
    fig = px.line(
        df, 
        x="date", 
        y="BenchmarkPct", 
        color="expression",
        title="Expression Trend Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- QUALITY INSIGHTS ---
def plot_quality_heatmap(df):
    """
    Heatmap pivot:
    Rows = player, Columns = quality, Values = avg BenchmarkPct
    """
    pivot = df.groupby(["player", "quality"])["BenchmarkPct"].mean().reset_index()
    pivot = pivot.pivot(index="player", columns="quality", values="BenchmarkPct")

    custom_scale = [[0, "#034694"], [0.5, "#D69A00"], [1, "#FAF8F0"]]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=custom_scale,
        colorbar=dict(title="Avg Benchmark %")
    ))
    fig.update_layout(title="Avg Benchmark % by Quality and Player")
    st.plotly_chart(fig, use_container_width=True)

def plot_quality_scatter(df):
    """
    Scatter plot:
    X = quality, Y = BenchmarkPct, color = movement
    """
    fig = px.scatter(
        df,
        x="quality",
        y="BenchmarkPct",
        color="movement",
        size_max=60,
        title="Benchmark % vs Quality by Movement"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_quality_trend(df):
    """
    Time-series line:
    X = date, Y = BenchmarkPct, color = quality
    """
    fig = px.line(
        df,
        x="date",
        y="BenchmarkPct",
        color="quality",
        title="Quality Trend Over Time"
    )
    st.plotly_chart(fig, use_container_width=True)

# --- PLAYER RANKINGS ---
def plot_player_rankings(df: pd.DataFrame, movement_filter: str, quality_filter: str, expression_filter: str):
    """
    Filters the dataset based on selected movement, quality, and expression,
    then ranks players by their average BenchmarkPct.
    Displays a bar chart and table of rankings.
    """
    filtered = df.copy()
    if movement_filter != "All":
        filtered = filtered[filtered["movement"] == movement_filter]
    if quality_filter != "All":
        filtered = filtered[filtered["quality"] == quality_filter]
    if expression_filter != "All":
        filtered = filtered[filtered["expression"] == expression_filter]

    # Group by player and compute average BenchmarkPct
    ranking = filtered.groupby("player")["BenchmarkPct"].mean().reset_index()
    ranking = ranking.sort_values("BenchmarkPct", ascending=False)

    fig = px.bar(
        ranking,
        x="player",
        y="BenchmarkPct",
        title="Player Rankings by Selected Metrics",
        labels={"BenchmarkPct": "Average Benchmark %", "player": "Player"}
    )
    st.plotly_chart(fig, use_container_width=True, key=f"ranking_{movement_filter}_{quality_filter}_{expression_filter}")
    st.write("Ranking Table")
    st.dataframe(ranking)

def plot_capability_vs_recovery(df: pd.DataFrame):
    """
    Scatter plot: x = BenchmarkPct (capability), y = Emboss Baseline Score (recovery)
    """
    # You can choose a different recovery metric as needed.
    fig = px.scatter(
        df, 
        x="BenchmarkPct", 
        y="emboss_baseline_score", 
        color="player",
        hover_data=["movement", "expression"],
        title="Capability vs Recovery (BenchmarkPct vs Emboss Baseline Score)"
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_combined_heatmap(df: pd.DataFrame):
    """
    Heatmap: Rows = player, Columns = movement, Values = BenchmarkPct,
    with merged recovery info available for future extensions.
    """
    grouped = df.groupby(["player", "movement"])["BenchmarkPct"].mean().reset_index()
    pivot = grouped.pivot(index="player", columns="movement", values="BenchmarkPct")
    
    custom_scale = [[0, "#034694"], [0.5, "#D69A00"], [1, "#FAF8F0"]]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=custom_scale,
        colorbar=dict(title="Avg BenchmarkPct")
    ))
    fig.update_layout(title="Capability Heatmap (Merged Data)")
    st.plotly_chart(fig, use_container_width=True)

def plot_movement_recovery_correlation_heatmap(corr_df: pd.DataFrame):
    """
    Plots a heatmap of correlation coefficients between the capability metric (BenchmarkPct)
    and several recovery metrics for each movement.
    
    Args:
        corr_df: DataFrame with columns: 
            'movement', 'Sleep_composite', 'Bio_composite', 
            'Msk_joint_range_composite', 'Subjective_composite', 'emboss_baseline_score'
    """
    # We'll treat 'movement' as row index and the rest as columns
    recovery_columns = [col for col in corr_df.columns if col != "movement"]
    pivot = corr_df.set_index("movement")[recovery_columns]
    
    custom_scale = [[0, "#034694"], [0.5, "#D69A00"], [1, "#FAF8F0"]]

    fig = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns,
        y=pivot.index,
        colorscale=custom_scale,
        zmin=-1,
        zmax=1,
        colorbar=dict(title="Correlation")
    ))
    fig.update_layout(
        title="Correlation between Capability & Recovery Metrics (by Movement)",
        xaxis_title="Recovery Metric",
        yaxis_title="Movement"
    )
    st.plotly_chart(fig, use_container_width=True)