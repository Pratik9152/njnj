
import pandas as pd
import json

def process_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df['Joining Date'] = pd.to_datetime(df['Joining Date'])
    df['Exit Date'] = pd.to_datetime(df['Exit Date'], errors='coerce')

    def calculate_duration(row):
        end_date = row['Exit Date'] if pd.notnull(row['Exit Date']) else pd.Timestamp.now()
        delta = pd.DateOffset(years=0)
        duration = end_date - row['Joining Date']
        days = duration.days
        years = days // 365
        months = (days % 365) // 30
        rem_days = (days % 365) % 30
        return f"{years}y {months}m {rem_days}d", years

    df[['Duration', 'Years Completed']] = df.apply(lambda row: pd.Series(calculate_duration(row)), axis=1)
    df['Eligible'] = df['Years Completed'] >= 5

    df['Gratuity Status'] = df.apply(
        lambda x: "✅ Eligible (Exited)" if x['Eligible'] and pd.notnull(x['Exit Date']) else (
            "🕒 Tracking..." if not x['Eligible'] else "✅ Eligible"
        ), axis=1
    )

    summary = {
        "Total Records": int(len(df)),
        "Eligible": int(df['Eligible'].sum()),
        "Exited": int(df['Exit Date'].notnull().sum()),
    }

    return df, summary

def save_processed_data(df):
    df.to_json("employee_data.json", orient="records", indent=2, date_format="iso")

def clear_data():
    with open("employee_data.json", "w") as f:
        f.write("[]")
