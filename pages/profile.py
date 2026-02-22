import streamlit as st
from datetime import date

def render_profile():
    st.markdown("""
        <div style="animation: fadeSlideUp 0.6s ease-out;">
            <h2 style="margin-bottom: 5px; font-weight: 700;">User Profile</h2>
            <p style="color: var(--text-secondary); margin-bottom: 25px;">Manage your account details and view your SkillSync progress.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Initialize mock frontend states if not present
    if "profile_edit_mode" not in st.session_state:
        st.session_state.profile_edit_mode = False
    
    user_data = st.session_state.user
    
    # Split layout: 1/3 Avatar & Quick Stats, 2/3 Details Form
    col_avatar, col_details = st.columns([1, 2], gap="large")
    
    with col_avatar:
        st.markdown("""
            <div style="text-align: center; padding: 30px; background: var(--surface-color); border: 1px solid var(--border-color); border-radius: 16px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <div style="width: 120px; height: 120px; margin: 0 auto 20px auto; border-radius: 50%; background: var(--accent-gradient); display: flex; align-items: center; justify-content: center; color: white; font-size: 48px; font-weight: bold; border: 4px solid var(--bg-color); box-shadow: 0 0 0 2px var(--border-color);">
                    👤
                </div>
                <h3 style="margin: 0; font-weight: 600;">""" + user_data['username'] + """</h3>
                <p style="color: var(--text-secondary); margin-top: 5px; font-size: 14px;">""" + user_data['level'] + """ Scholar</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Interactive faux-upload feature
        st.markdown("**(Optional) Update Avatar**")
        uploaded_file = st.file_uploader("Choose a square image", type=["png", "jpg", "jpeg"], label_visibility="collapsed")
        if uploaded_file:
            st.success("Avatar updated for the current session! ✨")
            
        st.markdown("### Career Stats")
        st.metric(label="Total XP", value=f"{user_data['xp']} XP")
        st.metric(label="Current Streak", value=f"🔥 {user_data['streak']} Days")
        st.metric(label="Soft Skills Rating", value=f"{user_data.get('soft_skills_score', 0)} / 100")

    with col_details:
        st.markdown("<h3 style='margin-bottom: 15px;'>Account Information</h3>", unsafe_allow_html=True)
        
        if not st.session_state.profile_edit_mode:
            with st.container():
                c1, c2 = st.columns(2)
                with c1:
                    st.text_input("Username", value=user_data['username'], disabled=True)
                with c2:
                    st.text_input("Email", value=user_data['email'], disabled=True)
                
                c3, c4 = st.columns(2)
                with c3:
                    st.text_input("Account Created", value=user_data.get('created_at', str(date.today()))[:10], disabled=True)
                with c4:
                    st.text_input("Last Login", value=user_data.get('last_login', str(date.today())), disabled=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Read-only display of advanced fields if they exist in the mock state
            c5, c6 = st.columns(2)
            with c5:
                st.text_input("Course", value=user_data.get('course', 'Not Set'), disabled=True)
            with c6:
                st.text_input("Branch", value=user_data.get('branch', 'Not Set'), disabled=True)
            
            st.text_area("About Me", value=user_data.get('bio', 'No bio provided.'), disabled=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Edit Profile Details", use_container_width=False):
                st.session_state.profile_edit_mode = True
                st.rerun()

        else:
            with st.form("edit_profile_form"):
                st.info("Edit mode active. Note: This frontend mockup temporarily updates local session states to avoid backend mutations.")
                new_username = st.text_input("Username", value=user_data['username'])
                new_email = st.text_input("Email", value=user_data['email'])
                
                # Advanced Fields: Academic & Preferences
                st.markdown("---")
                st.markdown("<h4 style='margin-bottom: 10px;'>Academic Details</h4>", unsafe_allow_html=True)
                
                c5, c6 = st.columns(2)
                with c5:
                    new_course = st.selectbox("Course", ["B.Tech", "MCA", "BCA", "M.Tech", "B.Sc", "Other"], index=0)
                with c6:
                    new_branch = st.selectbox("Branch / Specialization", ["Computer Science", "Information Technology", "AI & Data Science", "Electronics", "Mechanical", "Other"], index=0)
                    
                c7, c8 = st.columns(2)
                with c7:
                    new_year = st.selectbox("Current Year", ["1st Year", "2nd Year", "3rd Year", "4th Year"], index=2)
                with c8:
                    new_field = st.selectbox("Desired Career Field", ["AI/ML Engineer", "Data Scientist", "Full Stack Developer", "Backend Engineer", "Cloud Architect", "DevOps Engineer", "Frontend Developer", "Cybersecurity Analyst"], index=0)

                st.markdown("---")
                st.markdown("<h4 style='margin-bottom: 10px;'>Professional Goals</h4>", unsafe_allow_html=True)
                new_role = st.text_input("Target Role", placeholder="e.g. Lead Generative AI Developer")
                new_work_type = st.radio("Preferred Work Type", ["Remote", "Hybrid", "Onsite"], horizontal=True)
                
                new_bio = st.text_area("Short Bio / About Me", placeholder="I am a passionate developer looking for...")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                col_save, col_cancel = st.columns([1,1])
                with col_save:
                    submit_save = st.form_submit_button("Save Advanced Profile ✨", use_container_width=True)
                with col_cancel:
                    submit_cancel = st.form_submit_button("Cancel", use_container_width=True)
                
                if submit_save:
                    # Frontend pseudo-update
                    import copy
                    updated_user = copy.deepcopy(dict(st.session_state.user))
                    updated_user['username'] = new_username
                    updated_user['email'] = new_email
                    # Injecting mock data explicitly to prevent backend mutation while keeping UI rich
                    updated_user['course'] = new_course
                    updated_user['branch'] = new_branch
                    updated_user['career_field'] = new_field
                    updated_user['bio'] = new_bio
                    
                    st.session_state.user = updated_user
                    st.session_state.profile_edit_mode = False
                    st.rerun()
                    
                if submit_cancel:
                    st.session_state.profile_edit_mode = False
                    st.rerun()
