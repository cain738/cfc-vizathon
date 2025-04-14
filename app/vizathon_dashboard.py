"""
# ⚽ Chelsea FC Dashboard
"""
import streamlit as st
import os
from utils.ui_styling import load_local_css

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "app", "static")

def show_home():
    """
    Home page content.
    """
    st.title("Chelsea FC Vizathon - Home")
    # Adjust the image path according to your working directory:
    st.image(os.path.join(STATIC_DIR, "chelsea_logo.png"), width=150)
    st.markdown("""
    ### Welcome to the Chelsea FC Performance Dashboard

    Use the navigation below to switch between pages:
    - Home
    - GPS
    - Recovery
    - Capability
    - IPA
    - Combined
    - Advanced Analysis
    - Calendar
    """)

def main():
    print(STATIC_DIR)
    load_local_css()
    show_home()


if __name__ == "__main__":
    main()
