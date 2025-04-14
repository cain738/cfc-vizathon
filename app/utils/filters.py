# app/utils/filters.py
import streamlit as st
import pandas as pd
from analysis.data_loader import load_calendar_data



def player_filter():
    """
    Displays a sidebar multiselect for player names based on the calendar CSV.
    Returns the list of selected players and stores the selection in session state.
    """
    df = load_calendar_data()
    players = sorted(df["player"].dropna().unique())
    
    # Initialize session state if not present
    if 'selected_players' not in st.session_state:
        st.session_state['selected_players'] = players

    selected = st.sidebar.multiselect(
        "Select Player(s)",
        options=players,
        default=players[:5],
        key="player_filter"
    )
    
    # Persist the selection in session state
    st.session_state['selected_players'] = selected
    return selected
