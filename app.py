import streamlit as st
from style import apply_custom_styles
from ui import show_login, show_dashboard

# ✅ Apply global background styles
apply_custom_styles()

# ✅ Initialize login session state
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# ✅ Route user based on login status
if not st.session_state["authenticated"]:
    show_login()
else:
    show_dashboard()
