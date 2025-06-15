
import streamlit as st

def apply_custom_styles():
    st.markdown("""
    <style>
    html, body, [data-testid="stAppViewContainer"] {
        height: 100%;
        background: linear-gradient(270deg, #f093fb, #f5576c, #4facfe, #43e97b);
        background-size: 800% 800%;
        animation: gradientBG 25s ease infinite;
        overflow-x: hidden;
        font-family: 'Segoe UI', sans-serif;
    }

    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    .main > div {
        background-color: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 20px rgba(0,0,0,0.15);
    }

    .stButton > button {
        background: linear-gradient(to right, #ff758c, #ff7eb3);
        color: white;
        font-weight: bold;
        padding: 10px 22px;
        border-radius: 30px;
        border: none;
        transition: 0.3s;
    }

    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0px 0px 12px rgba(0,0,0,0.15);
    }

    section[data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.7);
        border-right: 2px solid #ccc;
    }

    h2 {
        color: #6a11cb;
    }
    </style>
    """, unsafe_allow_html=True)
