import streamlit as st
import ai_utils
import time

def render_career():
    st.header("💼 Career & Opportunity Hub")
    st.markdown("Your transition from academia to industry starts here.")
    
    tab1, tab2 = st.tabs(["📝 ATS Resume Builder", "🌐 Live Opportunity Scraper"])
    
    with tab1:
        st.subheader("Automated Portfolio Builder")
        st.markdown("Convert your standard university projects into high-impact, ATS-friendly resume bullet points.")
        
        # Pre-filled dummy data as requested
        dummy_project = "Birla Global University 1st Sem Project: Rainwater Harvesting Science Exhibition. We built a model using pipes and a pump to show how rainwater can be saved. We presented it to the faculty and got an A grade."
        
        project_input = st.text_area("Describe your university project (Raw form):", value=dummy_project, height=150)
        
        if st.button("✨ Generate ATS-Friendly Bullets"):
            with st.spinner("AI is analyzing your project and extracting professional terminology..."):
                time.sleep(1) # Fake delay for dramatic effect if API is fast or offline
                result = ai_utils.analyze_resume_projects(project_input)
                
                st.success("Resume snippet generation successful!")
                st.markdown("### 📄 Your Enhanced Project Description:")
                st.info(result)
        
        st.markdown("---")
        st.subheader("📝 Full AI CV & Cover Letter Generator")
        
        target_role = st.session_state.get('target_role', 'Software Engineer')
        st.write(f"**Target Role:** {target_role}")
        
        user_skills = st.text_input("List your key skills (e.g., Python, C, HTML):")
        user_projects = st.text_area("List your key projects (e.g., Rainwater Harvesting Model, Streamlit Web App):", height=100)
        
        if st.button("✨ Generate AI CV & Cover Letter", type="primary"):
            if not user_skills or not user_projects:
                st.error("Please enter both skills and projects!")
            else:
                result = None
                with st.spinner(f"Crafting highly optimized CV and Cover Letter for a {target_role}..."):
                    try:
                        result = ai_utils.generate_cv_and_cover_letter(target_role, user_skills, user_projects)
                        st.success("Generation Complete! 🎉")
                        
                        st.markdown("### 📄 ATS-Optimized CV Draft")
                        st.markdown(result.get('cv', 'CV generation failed.'))
                        
                        st.markdown("---")
                        
                        st.markdown("### ✉️ Customized Cover Letter")
                        st.markdown(result.get('cover_letter', 'Cover Letter generation failed.'))
                        
                    except Exception as e:
                        print(f"CV Gen Error: {e}")
                        st.warning("API is cooling down. Please wait 60 seconds.")
                
                # Further dummy resume assembly (Leaving this here as a legacy feature)
                if result:
                    with st.expander("View Basic Legacy Resume Layout"):
                        st.markdown(f"""
                        **{st.session_state.user['username']} | B.Tech Student, Birla Global University**
                        
                        **SKILLS**: C Programming, HTML, Problem Solving, Embedded Systems
                        
                        **PROJECTS**:
                        *Rainwater Harvesting Science Exhibition Model*
                        
                        {result.get('cv', '')}
                        """)
                        st.button("Download as PDF")
                    
    with tab2:
        st.subheader("Live Internship & GitHub Issues Matcher")
        st.markdown(f"Scraping the web for opportunities matching **{st.session_state.user['username']}**'s verified skills: `C Programming`, `HTML`.")
        
        if st.button("🔍 Run Scraper Agency"):
            with st.spinner("Initializing web scraping agent..."):
                time.sleep(1.5)
                st.markdown("🔄 Scanning LinkedIn, Wellfound, and GitHub...")
                time.sleep(1.5)
                
                st.success("Found 3 High-Match Opportunities!")
                
                # Dummy Data Simulation
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### 🏢 Tech Mahindra")
                    st.caption("Internship - Bhubaneswar (Hybrid)")
                    st.markdown("**Role**: C/C++ Foundation Intern")
                    st.markdown("**Match Score**: 94%")
                    st.button("Apply Now", key="apply_1")
                
                with col2:
                    st.markdown("### 🌐 Open Source: ReactOS")
                    st.caption("GitHub Issue #4512")
                    st.markdown("**Role**: Fix minor pointer bugs in UI setup")
                    st.markdown("**Match Score**: 88%")
                    st.button("View Repo", key="apply_2")
                    
                with col3:
                    st.markdown("### 🧑‍💻 TCS NQT Prep")
                    st.caption("Apprenticeship - Remote")
                    st.markdown("**Role**: HTML/CSS Junior Developer")
                    st.markdown("**Match Score**: 85%")
                    st.button("Apply Now", key="apply_3")
