
import streamlit as st
import pandas as pd
import os
from config import authenticate_user
from utils import process_file, save_processed_data, clear_data
from analytics import show_analytics
from notifications import show_reminder_popup
from filters import apply_filters
from progress import render_progress_bar

def show_login():
    st.markdown("""
    <div style='background-color: #fff0f5; padding: 30px; border-radius: 15px; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);'>
        <h2 style='color: #e63946;'>🔐 Gratuity Tracker Login</h2>
        <p style='color: #555;'>Please enter your credentials</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        user = st.text_input("👤 Username")
        pwd = st.text_input("🔑 Password", type="password")
        submitted = st.form_submit_button("🚀 Login")

        if submitted:
            if authenticate_user(user, pwd):
                st.session_state['authenticated'] = True
                st.success("✅ Login successful! Redirecting...")
                st.experimental_rerun()
            else:
                st.error("❌ Invalid credentials. Please try again.")

def show_dashboard():
    st.markdown("""
    <div style='text-align: center; padding: 20px; background-color: #ffffffbb; border-radius: 10px;'>
        <h2 style='color: #0077b6;'>🏢 Gratuity Tracker Dashboard</h2>
        <p style='color: #444;'>Monitor employee eligibility, visualize progress, and export insights.</p>
    </div>
    """, unsafe_allow_html=True)

    show_reminder_popup()

    st.markdown("### 📄 Sample CSV Template:")
    with open("sample_employee_file.csv", "rb") as file:
        st.download_button("⬇️ Download Sample File", data=file, file_name="sample_employee_file.csv", mime="text/csv")

    uploaded_file = st.sidebar.file_uploader("📤 Upload Employee CSV", type=["csv"])

    if uploaded_file:
        try:
            df, summary = process_file(uploaded_file)
            save_processed_data(df)
            st.session_state["data_uploaded"] = True
            st.success("✅ File uploaded and processed successfully.")
        except Exception as e:
            st.error(f"❌ Error processing file: {e}")
            return
    elif os.path.exists("employee_data.json"):
        df = pd.read_json("employee_data.json")
        st.info("📁 Loaded previous session file.")

        df['Joining Date'] = pd.to_datetime(df['Joining Date'])
        df['Exit Date'] = pd.to_datetime(df['Exit Date'], errors='coerce')

        def recalc(row):
            end = row['Exit Date'] if pd.notnull(row['Exit Date']) else pd.Timestamp.now()
            delta = end - row['Joining Date']
            days = delta.days
            years = days // 365
            months = (days % 365) // 30
            rem_days = (days % 365) % 30
            return f"{years}y {months}m {rem_days}d", years

        df[['Duration', 'Years Completed']] = df.apply(lambda row: pd.Series(recalc(row)), axis=1)
        df['Eligible'] = df['Years Completed'] >= 5
        df['Gratuity Status'] = df.apply(
            lambda x: "✅ Eligible (Exited)" if x['Eligible'] and pd.notnull(x['Exit Date']) else (
                "🕒 Tracking..." if not x['Eligible'] else "✅ Eligible"
            ), axis=1
        )
    else:
        st.warning("📤 Upload a CSV file to begin.")
        return

    df = apply_filters(df)

    st.markdown("### 🎯 Eligibility Report")
    st.dataframe(df.style.applymap(lambda x: 'background-color: #d1ffd6' if x == "✅ Eligible (Exited)" else '', subset=["Gratuity Status"]))

    st.markdown("### ⏳ Years Progress")
    for i, row in df.iterrows():
        st.markdown(f"**{row['Name']} ({row['Emp Code']})** — `{row['Duration']}`")
        render_progress_bar(row['Years Completed'])

    show_analytics(df)
