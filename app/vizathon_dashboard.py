import streamlit as st

from utils.ui_styling import load_local_css

def show_home():
    """
    Home page content.
    """
    st.title("Chelsea FC Vizathon - Home")
    # Adjust the image path according to your working directory:
    st.image("app/static/chelsea_logo.png", width=150)
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
    load_local_css()
    show_home()


if __name__ == "__main__":
    main()
