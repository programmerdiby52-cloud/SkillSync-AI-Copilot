import streamlit as st
import random
from roadmap_data import ROADMAP_DATA
from pages.cert_intern import CERT_DATA
from i18n_dict import get_t

def render_roadmap():
    st.header("🗺️ Master Roadmap")
    st.markdown("Your personalized path to mastery based on your target role.")
    
    target_role = st.session_state.get('target_role', 'Software Engineer')
    if not target_role:
        target_role = "Software Engineer"
        
    st.subheader(f"📅 Career Path: {target_role}")
    st.markdown("---")
    
    session_key = f'roadmap_{target_role}'
    
    if session_key not in st.session_state:
        with st.spinner(f"Compiling a custom curriculum for {target_role}..."):
            role_lower = target_role.lower()
            selected_roadmap = None
            
            # 1 & 2: Keyword search with specific keywords checked before generic "engineer"
            if "software" in role_lower:
                selected_roadmap = random.choice(ROADMAP_DATA["software"])
            elif "ai" in role_lower or "artificial intelligence" in role_lower or "machine learning" in role_lower:
                selected_roadmap = random.choice(ROADMAP_DATA["ai"])
            elif "data" in role_lower:
                selected_roadmap = random.choice(ROADMAP_DATA["data"])
            elif "full stack" in role_lower or "fullstack" in role_lower:
                selected_roadmap = random.choice(ROADMAP_DATA["full stack"])
            elif "ui" in role_lower or "ux" in role_lower or "design" in role_lower:
                selected_roadmap = random.choice(ROADMAP_DATA["ui"])
            elif "engineer" in role_lower:
                selected_roadmap = random.choice(ROADMAP_DATA["engineer"])
            else:
                # 4: Default fallback
                selected_roadmap = random.choice(ROADMAP_DATA["engineer"])
                
            st.session_state[session_key] = selected_roadmap
            
    roadmap = st.session_state[session_key]
    
    for idx, week in enumerate(roadmap):
        week_num = week.get('week', f'Week {idx+1}')
        with st.expander(f"📌 {week_num}", expanded=(idx == 0)):
            st.write(f"**Goal**: {week.get('goal', '')}")
            st.markdown("### Suggested Resources:")
            for res in week.get('resources', []):
                st.markdown(f"- {res}")
            if st.button("Mark as Complete (+50 XP)", key=f"rm_wk_{idx}_{target_role}"):
                st.success("Module Completed! Keep going!")
                
    # --- Priority Logic: Certifications & Internships Injection ---
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
        <div style="animation: fadeSlideUp 0.8s ease-out;">
            <h3 style="margin-bottom: 5px; font-weight: 700;">Suggested Opportunities</h3>
            <p style="color: var(--text-secondary); margin-bottom: 20px;">Based on your roadmap, here are top certifications and internships to accelerate your career.</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Simple mapping heuristic based on target role to select the right category from CERT_DATA
    role_lower = target_role.lower()
    mapping_key = "Core Engineering" # Default fallback
    
    if "data" in role_lower: mapping_key = "Data Science"
    elif "ai" in role_lower or "machine" in role_lower: mapping_key = "AI & Machine Learning"
    elif "web" in role_lower or "full stack" in role_lower or "frontend" in role_lower or "backend" in role_lower: mapping_key = "Web Development"
    elif "mobile" in role_lower or "android" in role_lower or "ios" in role_lower: mapping_key = "Mobile Development"
    elif "cyber" in role_lower or "security" in role_lower: mapping_key = "Cybersecurity"
    elif "cloud" in role_lower or "aws" in role_lower or "azure" in role_lower: mapping_key = "Cloud Computing"
    elif "devops" in role_lower or "sre" in role_lower: mapping_key = "DevOps"
    elif "block" in role_lower or "web3" in role_lower: mapping_key = "Blockchain"
    elif "ui" in role_lower or "ux" in role_lower or "design" in role_lower: mapping_key = "UI/UX Design"
    
    # Fetch and shuffle targeted opportunities
    targeted_opps = list(CERT_DATA.get(mapping_key, CERT_DATA["Core Engineering"]))
    random.shuffle(targeted_opps)
    top_3_opps = targeted_opps[:3]
    
    # Render horizontally (3 columns)
    c1, c2, c3 = st.columns(3, gap="medium")
    cols = [c1, c2, c3]
    
    for idx, item in enumerate(top_3_opps):
        with cols[idx]:
            type_color = "var(--accent-gradient)" if item['type'] == 'Certification' else "#10B981"
            level_color = "#3B82F6" if item['level'] == 'Beginner' else ("#F59E0B" if item['level'] == 'Intermediate' else "#EF4444")
            
            st.markdown(f"""
            <div style="background: var(--surface-color); border: 1px solid var(--border-color); border-radius: 16px; padding: 20px; height: 100%; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); transition: transform 0.3s ease, box-shadow 0.3s ease;" class="cert-card">
                <div>
                    <div style="display: flex; gap: 8px; margin-bottom: 12px;">
                        <span style="background: {type_color}; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">{item['type']}</span>
                        <span style="background: {level_color}; color: white; padding: 4px 10px; border-radius: 20px; font-size: 11px; font-weight: 600;">{item['level']}</span>
                    </div>
                    <h4 style="margin: 0 0 10px 0; font-size: 15px; font-weight: 600; line-height: 1.3;">{item['title']}</h4>
                </div>
                <button style="width: 100%; margin-top: 15px; background: transparent; color: var(--text-primary); border: 1px solid var(--border-color); border-radius: 8px; padding: 6px; font-size: 13px; font-weight: 600; cursor: pointer;">View Details</button>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("""
    <style>
        .cert-card:hover {
            transform: translateY(-4px) !important;
            box-shadow: 0 10px 25px -5px rgba(0,0,0,0.1), 0 0 15px rgba(59, 130, 246, 0.1) !important;
            border-color: rgba(59, 130, 246, 0.3) !important;
        }
    </style>
    """, unsafe_allow_html=True)
