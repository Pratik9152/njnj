import streamlit as st
from style import apply_custom_styles
from ui import show_login, show_dashboard

# ✅ Apply styles
apply_custom_styles()

# ✅ Initialize login state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ✅ Route user
if not st.session_state["authenticated"]:
    show_login()
else:
    show_dashboard()
