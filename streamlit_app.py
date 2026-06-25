
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Victorine Companion & Home Care", page_icon="🏥")
st.title("🏥 Victorine Companion & Home Care")
st.subheader("Caregiver Clock-In/Out Portal")

conn = st.connection("gsheets", type=GSheetsConnection)

caregivers = ["Select Caregiver...", "Caregiver A", "Caregiver B", "Caregiver C"]
selected_caregiver = st.selectbox("Who is clocking in/out?", caregivers)

action = st.radio("Select Action:", ["Clock In", "Clock Out"])
notes = st.text_area("Notes (Optional):", placeholder="Enter any shift notes here...")

if st.button("Submit Log"):
    if selected_caregiver == "Select Caregiver...":
        st.error("Please select your name before submitting!")
    else:
        new_data = pd.DataFrame([{
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Caregiver": selected_caregiver,
            "Action": action,
            "Notes": notes
        }])
        
        try:
            existing_data = conn.read()
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
            conn.update(data=updated_data)
            st.success(f"Successfully logged {action} for {selected_caregiver}! 🎉")
            st.balloons()
        except Exception as e:
            st.error(f"Error connecting to Google Sheets: {e}"]
