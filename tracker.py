import streamlit as st
import json
import os
import pandas as pd

st.set_page_config(page_title="Role Tracker", layout="wide")

TRACKER_FILE = "role_tracker.json"
REVIEW_FILE = "BPSMUN25_Reviewed.xlsx"

def load_tracker():
    if os.path.exists(TRACKER_FILE):
        with open(TRACKER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_tracker(data):
    with open(TRACKER_FILE, "w") as f:
        json.dump(data, f)

def get_filled_count_from_excel(role):
    if os.path.exists(REVIEW_FILE):
        df = pd.read_excel(REVIEW_FILE)
        df.columns = df.columns.str.strip()
        if "Assigned Role" in df.columns and "Status" in df.columns:
            return df[(df["Assigned Role"] == role) & (df["Status"] == "Accepted")].shape[0]
    return 0

roles_data = load_tracker()

st.title("📊 Role Tracker View")

st.markdown("---")

col1, col2 = st.columns(2)
with col1:
    new_role = st.text_input("Role Name")
    new_max = st.number_input("Number of Positions", min_value=1, value=1, step=1)
    if st.button("Add Role") and new_role:
        roles_data[new_role] = {"max": new_max}
        save_tracker(roles_data)
        st.rerun()

st.markdown("---")

for role, info in roles_data.items():
    st.subheader(role)
    max_count = info.get("max", 0)
    filled_count = get_filled_count_from_excel(role)

    boxes = ""
    for i in range(max_count):
        if i < filled_count:
            boxes += "<div style='display:inline-block;width:25px;height:25px;background-color:#27ae60;margin:3px;border-radius:5px;'></div>"
        else:
            boxes += "<div style='display:inline-block;width:25px;height:25px;background-color:#1c1e23;margin:3px;border-radius:5px;border:1px solid #444;'></div>"

    st.markdown(f"<div style='margin-bottom:10px;'>{boxes}</div>", unsafe_allow_html=True)

    if st.button(f"Reset {role}"):
        roles_data[role]["max"] = max_count  # keep max unchanged
        save_tracker(roles_data)
        st.rerun()
