
import streamlit as st

def render_progress_bar(value):
    st.progress(min(value / 10, 1.0))
