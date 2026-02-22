import streamlit as st
import database as db
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import date, timedelta
import random

def render_dashboard():
    st.header("✨ Command Center Dashboard")
    st.markdown("Track your academic and career progression in real-time.")
    
    user = st.session_state.user
    
    # --- Top Metrics Row ---
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Current XP", value=f"{user['xp']} ⚡", delta="+50 this week")
    with col2:
        st.metric(label="Daily Streak", value=f"{user['streak']} 🔥", delta="Keep it up!")
    with col3:
        st.metric(label="Soft Skills Score", value=f"{user['soft_skills_score']}/100 🎯", delta="+5 from last sim")
    with col4:
        st.metric(label="Rank", value=f"🛡️ {user['level']}", delta="Top 15%")
        
    st.markdown("---")
    
    # --- Charts & Analytics Row ---
    col_chart1, col_chart2 = st.columns(2)
    
    with col_chart1:
        st.subheader("📊 Skill Acquisition Rate")
        # Dummy data for the chart
        dates = [date.today() - timedelta(days=x) for x in range(6, -1, -1)]
        xp_gains = [random.randint(20, 100) for _ in range(7)]
        df_xp = pd.DataFrame({'Date': dates, 'XP Gained': xp_gains})
        
        fig = px.area(df_xp, x='Date', y='XP Gained', color_discrete_sequence=['#3B82F6'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0',
            margin=dict(l=0, r=0, t=20, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col_chart2:
        st.subheader("🔋 Burnout & Study Analytics")
        # Dummy data
        categories = ['Focus', 'Consistency', 'Module Completion', 'Assessment Score']
        scores = [85, 92, 78, 88]
        
        fig2 = go.Figure(data=go.Scatterpolar(
          r=scores + [scores[0]], # Close the loop
          theta=categories + [categories[0]],
          fill='toself',
          line_color='#10B981'
        ))
        fig2.update_layout(
            polar=dict(
                radialaxis=dict(visible=True, range=[0, 100])
            ),
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#E2E8F0',
            margin=dict(l=40, r=40, t=20, b=0)
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        # --- AI Wellness Coach ---
        import ai_utils
        st.markdown("### 🧘 AI Wellness Coach")
        # Mocking values for study hours and modules completed
        coach_msg = ai_utils.get_wellness_coaching(study_hours=4.5, modules_completed=3)
        st.info(f"**Coach:** {coach_msg}")
        
    st.markdown("---")
    
    # --- Next Micro-Goals ---
    st.subheader("🎯 Active Micro-Goals")
    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.info("**Complete C Pointers Module**\n\nReward: +50 XP\n\nDeadline: Tomorrow")
        st.button("Start Now", key="btn_c_pointers")
    with g_col2:
        st.success("**Take Soft Skills Assessment**\n\nReward: +100 XP\n\nDeadline: Inside 3 Days")
        st.button("Start Now", key="btn_soft_skills")
    with g_col3:
        st.warning("**Apply for 2 Internships**\n\nReward: +200 XP\n\nDeadline: End of Week")
        st.button("View Matches", key="btn_internships")

