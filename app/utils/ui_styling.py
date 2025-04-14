# app/utils/ui_styling.py
import streamlit as st
st.set_page_config(layout="wide")

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

def load_local_css(filename: str = "custom.css"):
    """
    Loads the custom CSS file into the Streamlit app.
    Default path assumes static files are under app/static.
    """
    full_path = os.path.join(STATIC_DIR, filename)
    try:
        with open(full_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"⚠️ Could not find CSS file at: {full_path}")
