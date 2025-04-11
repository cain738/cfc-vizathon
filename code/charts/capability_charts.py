# code/charts/capability_charts.py
import plotly.express as px
import streamlit as st

def show_benchmark_by_movement(capability_df):
    movement_avg = capability_df.groupby("movement")["BenchmarkPct"].mean().reset_index()
    fig = px.bar(movement_avg, x="movement", y="BenchmarkPct", title="Average Benchmark by Movement")
    st.plotly_chart(fig)

def show_benchmark_by_expression(capability_df):
    expr_avg = capability_df.groupby("expression")["BenchmarkPct"].mean().reset_index()
    fig = px.bar(expr_avg, x="expression", y="BenchmarkPct", title="Benchmark by Expression Type")
    st.plotly_chart(fig)
