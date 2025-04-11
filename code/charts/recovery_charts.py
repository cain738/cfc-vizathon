# code/charts/recovery_charts.py
import plotly.express as px
import streamlit as st

def show_avg_recovery_line(recovery_df):
    daily_avg = recovery_df.groupby("date")["emboss_baseline_score"].mean().reset_index()
    fig = px.line(daily_avg, x="date", y="emboss_baseline_score", title="Average Recovery Over Time")
    st.plotly_chart(fig)

def show_recovery_box(recovery_df):
    fig = px.box(recovery_df, x="player", y="emboss_baseline_score", title="Recovery Score Distribution")
    st.plotly_chart(fig)

def show_recovery_domains(recovery_df):
    domain_scores = recovery_df[[col for col in recovery_df.columns if "_composite" in col]].mean().reset_index()
    domain_scores.columns = ["Domain", "Average Score"]
    fig = px.bar(domain_scores, x="Domain", y="Average Score", title="Composite Recovery Scores by Domain")
    st.plotly_chart(fig)
