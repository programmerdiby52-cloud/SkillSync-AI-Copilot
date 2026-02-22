import streamlit as st
import database as db
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def render_settings():
    st.header("⚙️ Settings & Privacy")
    st.markdown("Manage your account security and review our platform guidelines.")
    
    st.markdown("---")
    st.subheader("🔑 Change Password")
    with st.form("password_change_form"):
        old_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submit_pw = st.form_submit_button("Update Password")
        
        if submit_pw:
            if not old_password or not new_password or not confirm_password:
                st.error("Please fill in all fields.")
            elif new_password != confirm_password:
                st.error("New passwords do not match.")
            else:
                user_record = db.get_user_by_username(st.session_state.user['username'])
                if user_record and user_record['password_hash'] == hash_password(old_password):
                    db.update_password(st.session_state.user['id'], hash_password(new_password))
                    st.success("Password updated successfully!")
                else:
                    st.error("Incorrect current password.")

    st.markdown("---")
    st.subheader("📜 Terms and Conditions")
    with st.expander("Read SkillSync Terms of Service"):
        st.markdown("""
        **1. Acceptance of Terms**
        By accessing and using this platform, you accept and agree to be bound by the terms and provision of this agreement.
        
        **2. Educational Purpose**
        This application is an AI-powered educational dashboard. All AI-generated content (including roadmaps, resumes, and mentor advice) is provided for informational and preparatory purposes. You are responsible for verifying the accuracy of AI outputs.
        
        **3. User Conduct**
        Users agree to not misuse the API constraints or attempt to maliciously overload the GenAI endpoints. 
        
        **4. Privacy Policy**
        We value your privacy. Your progress, diagnostic scores, and uploaded PDFs are stored locally in the application database and are not sold to third parties. 
        
        **5. Disclaimer of Warranties**
        The platform is provided "as is". We make no warranties, expressed or implied, regarding the reliability or availability of the Google GenAI services.
        """)
