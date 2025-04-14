# ⚽ Chelsea FC Dashboard

import streamlit as st
import os
import pandas as pd
import plotly.express as px
from utils.ui_styling import load_local_css
from analysis.data_loader import (
    load_gps_data,
    load_recovery_data,
    load_capability_data,
    load_ipa_data,
    load_calendar_data
)

# Setup static assets
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

def show_home():
    st.title("Chelsea FC Vizathon - Home")
    st.image(os.path.join(STATIC_DIR, "chelsea_logo.png"), width=150)

    st.markdown("""
    Welcome to the **Chelsea FC Performance Dashboard**.

    This application provides insights from GPS tracking, recovery status, physical capability benchmarks, and IPA goals.  
    Below, you’ll find visual summaries and key takeaways across all major datasets.
    """)

    # Load data
    gps_df = load_gps_data()
    recovery_df = load_recovery_data()
    capability_df = load_capability_data()
    ipa_df = load_ipa_data()
    calendar_df = load_calendar_data()

    # Merge GPS with calendar for actual training load
    gps_df["date"] = pd.to_datetime(gps_df["date"])
    calendar_df["event_date"] = pd.to_datetime(calendar_df["event_date"])
    merged_gps = pd.merge(
        gps_df,
        calendar_df[["player", "event_date", "training_load"]],
        left_on=["player", "date"],
        right_on=["player", "event_date"],
        how="left"
    )

    # Summaries
    gps_summary = merged_gps.groupby("player")["training_load"].mean().sort_values(ascending=False).head()
    recovery_summary = recovery_df.groupby("player")["emboss_baseline_score"].mean().sort_values(ascending=False).head()
    capability_summary = capability_df.groupby("player")["BenchmarkPct"].mean().sort_values(ascending=False).head()
    ipa_summary = ipa_df.groupby("player")["target_performance"].apply(
        lambda x: (x == "Achieved").sum() / len(x)
    ).sort_values(ascending=False).head()

    # Tabs for each dataset
    tab1, tab2, tab3, tab4 = st.tabs([
        "🛰️ GPS Insights", "🛌 Recovery", "🏋️ Capability", "📌 IPA Goals"
    ])

    with tab1:
        st.subheader("🛰️ Training Load Analysis")
        st.markdown("""
        - High-speed runs and HR Zone 5 minutes correlate with training load.
        - Based on calendar data, **Callum Hudson-Odoi** and **Emerson Palmieri** logged the highest average loads.
        """)
        fig = px.bar(gps_summary, x=gps_summary.index, y=gps_summary.values,
                     labels={"x": "Player", "y": "Avg. Training Load"},
                     title="Top 5 Players by Avg. Training Load")
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.subheader("🛌 Recovery & Readiness")
        st.markdown("""
        - **Sleep completeness** and **subjective wellness** are the best predictors of `emboss_baseline_score`.
        - **César Azpilicueta** consistently ranks among the top in recovery readiness.
        """)
        fig = px.bar(recovery_summary, x=recovery_summary.index, y=recovery_summary.values,
                     labels={"x": "Player", "y": "Recovery Score"},
                     title="Top 5 Players by Emboss Baseline Score")
        st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.subheader("🏋️ Physical Capability")
        st.markdown("""
        - Capability performance depends on **movement**, **quality**, **expression**, and **matchday timing**.
        - **Ben Chilwell** leads in Sprint and Upper Body benchmarks.
        """)
        fig = px.bar(capability_summary, x=capability_summary.index, y=capability_summary.values,
                     labels={"x": "Player", "y": "Benchmark %"},
                     title="Top 5 Players by Physical Capability (BenchmarkPct)")
        st.plotly_chart(fig, use_container_width=True)

    with tab4:
        st.subheader("📌 Individual Priority Areas (IPA)")
        st.markdown("""
        - Goals like **Fitness**, **Strength**, and **Speed** are frequently achieved.
        - Tactical and mindset areas show higher risk.
        - **Mason Mount** has the highest goal achievement rate overall.
        """)
        fig = px.bar(ipa_summary, x=ipa_summary.index, y=ipa_summary.values,
                     labels={"x": "Player", "y": "Achievement Rate"},
                     title="Top 5 Players by IPA Goal Achievement Rate")
        st.plotly_chart(fig, use_container_width=True)

def main():
    load_local_css()
    show_home()

if __name__ == "__main__":
    main()
