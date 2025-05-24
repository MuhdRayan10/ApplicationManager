import streamlit as st
import pandas as pd

st.set_page_config(page_title="BPSMUN'25 Review", layout="centered")

input_file = "BPSMUN'25 Student Officers.xlsx"
output_file = "BPSMUN25_Reviewed.xlsx"

@st.cache_data
def load_data():
    original_df = pd.read_excel(input_file)
    original_df.columns = original_df.columns.str.strip()
    if 'Status' not in original_df.columns:
        original_df['Status'] = None
    return original_df

original_df = load_data()
df = original_df.sample(frac=1, random_state=42).reset_index(drop=True)

st.title("\ud83d\udccb BPSMUN'25 Student Officer Review")

unreviewed = df[df['Status'].isna()].reset_index(drop=True)

if unreviewed.empty:
    st.success("\u2705 All applications have been reviewed!")
else:
    i = st.session_state.get("index", 0)
    if i >= len(unreviewed):
        st.session_state.index = 0
        i = 0
    app = unreviewed.iloc[i]

    st.subheader(f"\ud83d\udccc Application {i+1} of {len(unreviewed)}")

    with st.container():
        st.markdown(f"""
        <h2 style='color:#2C3E50;'>{app.get("Full Name", "")}</h2>
        <p style='font-size:18px;'>
        <strong>Grade:</strong> {str(app.get("Grade", ""))} {str(app.get("Section", ""))}  <br>
        <strong>Admission No:</strong> {app.get("Admission Number", "")}  <br>
        <strong>\ud83d\udcde Mobile:</strong> {app.get("Mobile Number", "")}
        </p>
        """, unsafe_allow_html=True)

    st.divider()

    with st.expander("\ud83c\udfaf Position Preferences", expanded=True):
        st.markdown(f"""
        <ul style='font-size:17px;'>
        <li><strong>1st Preference:</strong> {app.get("First Preference", "Not Provided")}</li>
        <li><strong>2nd Preference:</strong> {app.get("Second Preference", "Not Provided")}</li>
        <li><strong>3rd Preference:</strong> {app.get("Third Preference", "Not Provided")}</li>
        </ul>
        """, unsafe_allow_html=True)

    experience_text = app.get("List your prior MUN experiences (eg. conferences, awards, chairing, etc.)", "")
    mun_count = app.get("How many MUNs have you participated in?", "N/A")

    with st.expander("\ud83e\uddd9 MUN Experience", expanded=True):
        st.markdown(f"<p style='font-size:16px;'>{experience_text}</p>", unsafe_allow_html=True)
        st.info(f"\ud83d\uddc2\ufe0f MUNs Participated (as entered): **{mun_count}**")

    why_this_role = app.get("Why do you want this role?", "Not provided")
    with st.expander("\ud83d\udcac Why do you want this role?", expanded=True):
        st.markdown(f"<p style='font-size:16px;'>{why_this_role}</p>", unsafe_allow_html=True)

    fit_for_role = app.get("What skills make you a good fit for this role?", "Not provided")
    with st.expander("\ud83d\udd11 Why are you a good fit?", expanded=True):
        st.markdown(f"<p style='font-size:16px;'>{fit_for_role}</p>", unsafe_allow_html=True)

    upload_link = app.get("Upload any supporting certificates, works, awards, etc.", "")
    if pd.notna(upload_link) and upload_link.strip():
        with st.expander("\ud83d\udccc Uploaded File", expanded=False):
            st.markdown(f"[\u2b07\ufe0f Download Certificates & Awards]({upload_link})")

    st.divider()

    with st.expander("\ud83d\udee0\ufe0f Skills", expanded=False):
        st.markdown(f"<p style='font-size:16px;'>{app.get('Do you have experience in any of the following?', 'N/A')}</p>", unsafe_allow_html=True)

    portfolio = app.get("Share any relevant links to your work (e.g., portfolio, writing samples, designs, videos).", "")
    with st.expander("\ud83d\udcc1 Portfolio / Work Links", expanded=False):
        st.markdown(f"<p style='font-size:16px;'>{portfolio}</p>", unsafe_allow_html=True)

    upload_link = app.get("Upload your CV / work (if any)", "")
    if pd.notna(upload_link) and upload_link.strip():
        with st.expander("\ud83d\udccc Uploaded File", expanded=False):
            st.markdown(f"[Click to View File]({upload_link})")

    st.divider()

    col1, col2, col3 = st.columns([1, 1, 1])
    row_index = original_df[(original_df["Admission Number"] == app["Admission Number"])].index[0]

    with col1:
        if st.button("\u2705 Accept", use_container_width=True):
            original_df.at[row_index, 'Status'] = "Accepted"
            original_df.to_excel(output_file, index=False)
            st.session_state.index = i + 1
            st.rerun()

    with col2:
        if st.button("\u274c Reject", use_container_width=True):
            original_df.at[row_index, 'Status'] = "Rejected"
            original_df.to_excel(output_file, index=False)
            st.session_state.index = i + 1
            st.rerun()

    with col3:
        if st.button("\u27a1\ufe0f Skip", use_container_width=True):
            st.session_state.index = i + 1
            st.rerun()
