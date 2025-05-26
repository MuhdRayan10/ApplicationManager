import streamlit as st
import pandas as pd

st.set_page_config(page_title="BPSMUN'25 Review", layout="wide")

input_file = "BPSMUN'25 Student Officers.xlsx"
output_file = "BPSMUN25_Reviewed.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(input_file)
    df.columns = df.columns.str.strip()
    if 'Status' not in df.columns:
        df['Status'] = None
    if 'Assigned Role' not in df.columns:
        df['Assigned Role'] = ""
    df["Original Index"] = df.index
    return df

if "review_df" not in st.session_state:
    st.session_state.review_df = load_data()
    st.session_state.shuffled_df = st.session_state.review_df.sample(frac=1, random_state=42).reset_index(drop=True)
    st.session_state.index = 0

review_df = st.session_state.review_df
shuffled_df = st.session_state.shuffled_df

with st.container():
    st.markdown("""
    <div style='text-align:center;'>
        <h1>📋 BPSMUN'25 Student Officer Review</h1>
    </div>
    """, unsafe_allow_html=True)

    mode = st.radio("Select Mode", ["Single Review", "Multi View"], horizontal=True)

unreviewed_df = shuffled_df[shuffled_df["Status"].isna()].reset_index(drop=True)

if unreviewed_df.empty:
    st.success("✅ All applications have been reviewed!")

elif mode == "Multi View":
    st.subheader(f"📚 Viewing {len(unreviewed_df)} Unreviewed Applications")

    updates = []
    for idx, app in unreviewed_df.iterrows():
        st.markdown("---")
        st.markdown(f"**{app.get('Full Name', 'Unnamed').strip()}** — {app.get('Grade', '')} {app.get('Section', '')}")
        st.markdown(f"Admission No: {app.get('Admission Number', '')} | 📞 {app.get('Mobile Number', '')}")
        st.markdown(f"Preferences: {app.get('First Preference', '-')}, {app.get('Second Preference', '-')}, {app.get('Third Preference', '-')}")
        col1, col2 = st.columns(2)
        with col1:
            decision = st.selectbox("Decision", ["", "Accept", "Reject"], key=f"multi_decision_{idx}")
        with col2:
            role = st.text_input("Assigned Role", key=f"multi_role_{idx}")

        updates.append({
            "original_idx": app["Original Index"],
            "decision": decision,
            "role": role
        })

    if st.button("💾 Save All Decisions"):
        for upd in updates:
            if upd["decision"]:
                review_df.at[upd["original_idx"], "Status"] = "Accepted" if upd["decision"] == "Accept" else "Rejected"
                review_df.at[upd["original_idx"], "Assigned Role"] = upd["role"]
        review_df.to_excel(output_file, index=False)
        st.success("✅ All decisions saved!")
        st.rerun()

else:
    i = st.session_state.index
    if i >= len(unreviewed_df):
        st.session_state.index = 0
        i = 0
    jump_to = st.number_input(
    f"🔍 Jump to Application # (1 to {len(unreviewed_df)})", 
    min_value=1, 
    max_value=len(unreviewed_df), 
    step=1, 
    value=i+1, 
    key="jump_input")

    if jump_to - 1 != i:
        st.session_state.index = jump_to - 1
        st.rerun()

    app = unreviewed_df.iloc[i]

    st.markdown(f"""
    <div style='text-align:center;'>
    <h3>📌 Application {i+1} of {len(unreviewed_df)}</h3>
    </div>
    """, unsafe_allow_html=True)

    with st.container():
        st.markdown(f"""
        <div style='text-align:center;'>
        <h2 style='color:#2C3E50;'>{app.get("Full Name", "")}</h2>
        <p style='font-size:18px;'>
        <strong>Grade:</strong> {str(app.get("Grade", ""))} {str(app.get("Section", ""))}  <br>
        <strong>Admission No:</strong> {app.get("Admission Number", "")}  <br>
        <strong>📞 Mobile:</strong> {app.get("Mobile Number", "")}
        </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    with st.expander("🎯 Position Preferences", expanded=True):
        st.markdown(f"""
        <ul style='font-size:17px;'>
        <li><strong>1st Preference:</strong> {app.get("First Preference", "Not Provided")}</li>
        <li><strong>2nd Preference:</strong> {app.get("Second Preference", "Not Provided")}</li>
        <li><strong>3rd Preference:</strong> {app.get("Third Preference", "Not Provided")}</li>
        </ul>
        """, unsafe_allow_html=True)

    experience_text = app.get("List your prior MUN experiences (eg. conferences, awards, chairing, etc.)", "")
    mun_count = app.get("How many MUNs have you participated in?", "N/A")

    with st.expander("🧝 MUN Experience", expanded=True):
        st.markdown(f"<p style='font-size:16px;'>{experience_text}</p>", unsafe_allow_html=True)
        st.info(f"🗂️ MUNs Participated (as entered): **{mun_count}**")

    why_this_role = app.get("Why do you want this role?", "Not provided")
    with st.expander("💬 Why do you want this role?", expanded=True):
        st.markdown(f"<p style='font-size:16px;'>{why_this_role}</p>", unsafe_allow_html=True)

    fit_for_role = app.get("What skills make you a good fit for this role?", "Not provided")
    with st.expander("🔑 Why are you a good fit?", expanded=True):
        st.markdown(f"<p style='font-size:16px;'>{fit_for_role}</p>", unsafe_allow_html=True)

    upload_link = app.get("Upload any supporting certificates, works, awards, etc.", "")
    if pd.notna(upload_link) and upload_link.strip():
        with st.expander("📌 Uploaded File", expanded=False):
            st.markdown(f"[⬇️ Download Certificates & Awards]({upload_link})")

    st.divider()

    with st.expander("🛠️ Skills", expanded=False):
        st.markdown(f"<p style='font-size:16px;'>{app.get('Do you have experience in any of the following?', 'N/A')}</p>", unsafe_allow_html=True)

    portfolio = app.get("Share any relevant links to your work (e.g., portfolio, writing samples, designs, videos).", "")
    with st.expander("📁 Portfolio / Work Links", expanded=False):
        st.markdown(f"<p style='font-size:16px;'>{portfolio}</p>", unsafe_allow_html=True)

    upload_link = app.get("Upload your CV / work (if any)", "")
    if pd.notna(upload_link) and upload_link.strip():
        with st.expander("📌 Uploaded File", expanded=False):
            st.markdown(f"[Click to View File]({upload_link})")

    st.divider()

    role_input = st.text_input("🎖️ Assign Role (if accepting)", "")

    col1, col2, col3 = st.columns([1, 1, 1])
    original_index = app["Original Index"]

    with col1:
        if st.button("✅ Accept", use_container_width=True):
            st.session_state.review_df.at[original_index, 'Status'] = "Accepted"
            st.session_state.review_df.at[original_index, 'Assigned Role'] = role_input
            st.session_state.review_df.to_excel(output_file, index=False)
            st.session_state.index += 1
            st.rerun()

    with col2:
        if st.button("❌ Reject", use_container_width=True):
            st.session_state.review_df.at[original_index, 'Status'] = "Rejected"
            st.session_state.review_df.to_excel(output_file, index=False)
            st.session_state.index += 1
            st.rerun()

    with col3:
        if st.button("➡️ Skip", use_container_width=True):
            st.session_state.index += 1
            st.rerun()
