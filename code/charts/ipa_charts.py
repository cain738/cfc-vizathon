# code/charts/ipa_charts.py
import plotly.express as px
import streamlit as st

def show_priority_category(ipa_df):
    cat_count = ipa_df["priority_category"].value_counts().reset_index()
    cat_count.columns = ["priority_category", "count"]
    fig = px.bar(cat_count, x="priority_category", y="count", title="Priority Goals by Category")
    st.plotly_chart(fig)

def show_tracking_status(ipa_df):
    status_count = ipa_df["tracking_status"].value_counts().reset_index()
    status_count.columns = ["tracking_status", "count"]
    fig = px.bar(status_count, x="tracking_status", y="count", title="Tracking Status Distribution")
    st.plotly_chart(fig)

def show_type_distribution(ipa_df):
    type_count = ipa_df["type"].value_counts().reset_index()
    type_count.columns = ["type", "count"]
    fig = px.bar(type_count, x="type", y="count", title="Habit vs Outcome Goals")
    st.plotly_chart(fig)
