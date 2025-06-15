
import streamlit as st
import pandas as pd

def show_analytics(df):
    st.markdown("### 📊 Smart Gratuity Analytics")

    if df is None or df.empty or 'Eligible' not in df.columns:
        st.warning("⚠️ No valid data to analyze.")
        return

    st.markdown("### ✅ Eligible Employees by Department")
    dept_counts = df[df["Eligible"]].groupby("Department").size()
    if not dept_counts.empty:
        st.bar_chart(dept_counts)
    else:
        st.info("No eligible employees found.")

    st.markdown("### 📈 Tenure Trend (Years Completed)")
    if 'Years Completed' in df.columns:
        st.line_chart(df["Years Completed"])
