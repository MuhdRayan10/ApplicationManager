import streamlit as st
import pandas as pd

# === Must come first ===
st.set_page_config(page_title="BPSMUN'25 Review", layout="centered")

# === Config ===
input_file = "BPSMUN'25 Student Officers.xlsx"
output_file = "BPSMUN25_Reviewed.xlsx"

# === Load data ===
@st.cache_data
def load_data():
    df = pd.read_excel(input_file)
    df.columns = df.columns.str.strip()
    if 'Status' not in df.columns:
        df['Status'] = None
    return df

df = load_data()

# === App UI ===
st.title("📋 BPSMUN'25 Student Officer Review")

# Filter unreviewed applications
unreviewed = df[df['Status'].isna()].reset_index(drop=True)

if unreviewed.empty:
    st.success("✅ All applications have been reviewed!")
else:
    i = st.session_state.get("index", 0)
    if i >= len(unreviewed):
        st.session_state.index = 0
        i = 0
    app = unreviewed.iloc[i]

    st.subheader(f"📌 Application {i+1} of {len(unreviewed)}")

    with st.container():
        st.markdown(f"""
        <h2 style='color:#2C3E50;'>{app.get("Full Name", "")}</h2>
        <p style='font-size:18px;'><strong>Grade:</strong> {str(app.get("Grade", ""))} {str(app.get("Section", ""))}  
        <br><strong>Admission No:</strong> {app.get("Admission Number", "")}  
        <br><strong>📞 Mobile:</strong> {app.get("Mobile Number", "")}</p>
        """, unsafe_allow_html=True)

    st.divider()

    with st.expander("🎯 Preferences", expanded=True):
        st.markdown(f"""
        <ul style='font-size:17px;'>
        <li><strong>1st Preference:</strong> {app.get("Position Preference 1", "")}</li>
        <li><strong>2nd Preference:</strong> {app.get("Position Preference 2", "")}</li>
        <li><strong>3rd Preference:</strong> {app.get("Position Preference 3", "")}</li>
        </ul>
        """, unsafe_allow_html=True)

    with st.expander("🧭 MUN Experience", expanded=True):
        st.markdown(f"<p style='font-size:16px;'>{app.get('List your prior MUN experiences (eg. conferences, awards, chairing, etc.)', 'N/A')}</p>", unsafe_allow_html=True)

    with st.expander("🛠️ Skills", expanded=False):
        st.markdown(f"<p style='font-size:16px;'>{app.get('Do you have experience in any of the following?', 'N/A')}</p>", unsafe_allow_html=True)

    with st.expander("📁 Portfolio / Work Links", expanded=False):
        st.markdown(f"<p style='font-size:16px;'>{app.get('Share any relevant links to your work (e.g., portfolio, writing samples, designs, videos).', 'N/A')}</p>", unsafe_allow_html=True)

    st.divider()

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button("✅ Accept", use_container_width=True):
            df.loc[df.index == app.name, 'Status'] = "Accepted"
            df.to_excel(output_file, index=False)
            st.session_state.index = i + 1
            st.rerun()
    with col2:
        if st.button("❌ Reject", use_container_width=True):
            df.loc[df.index == app.name, 'Status'] = "Rejected"
            df.to_excel(output_file, index=False)
            st.session_state.index = i + 1
            st.rerun()
    with col3:
        if st.button("➡️ Skip", use_container_width=True):
            st.session_state.index = i + 1
            st.rerun()
