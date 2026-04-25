import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

# --- APP CONFIGURATION ---
st.set_page_config(page_title="Victorine Care Portal", page_icon="🏥")

st.title("Victorine Companion & Home Care")
st.subheader("Shift Log & Time Tracker")

# Connect to Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# --- LOGIC: CALCULATE HOURS ---
def calculate_hours(name):
    try:
        existing_data = conn.read(worksheet="Logs")
        user_logs = existing_data[existing_data["Caregiver Name"] == name]
        # Find the last "Clock In"
        last_in_idx = user_logs[user_logs["Action"] == "Clock In"].index
        if not last_in_idx.empty:
            last_in_row = user_logs.loc[last_in_idx[-1]]
            in_time = datetime.strptime(last_in_row["Timestamp"], "%Y-%m-%d %H:%M:%S")
            out_time = datetime.now()
            duration = out_time - in_time
            return round(duration.total_seconds() / 3600, 2)
    except:
        return 0
    return 0

# --- UI FORM ---
with st.form("log_form", clear_on_submit=True):
    name = st.selectbox("Select Caregiver", ["Victorine", "Caregiver 1", "Caregiver 2"])
    action = st.radio("Action", ["Clock In", "Clock Out"])
    notes = st.text_area("Caregiver Notes / Observations")
    
    submit = st.form_submit_button("Submit Entry")

if submit:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hours_worked = 0
    
    if action == "Clock Out":
        hours_worked = calculate_hours(name)
        if hours_worked > 0:
            st.info(f"Shift Duration: {hours_worked} hours")

    # Prepare data for Google Sheets
    new_entry = pd.DataFrame([{
        "Caregiver Name": name,
        "Timestamp": timestamp,
        "Action": action,
        "Notes": notes,
        "Hours Calculated": hours_worked
    }])

    # Update the Sheet
    try:
        existing_df = conn.read(worksheet="Logs")
        updated_df = pd.concat([existing_df, new_entry], ignore_index=True)
        conn.update(worksheet="Logs", data=updated_df)
        st.success(f"Successfully logged {action} for {name}!")
    except Exception as e:
        st.error("Connection Error: Make sure your Google Sheet is set to 'Anyone with the link can Edit'.")
