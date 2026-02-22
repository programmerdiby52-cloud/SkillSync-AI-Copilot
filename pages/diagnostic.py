import streamlit as st
import random
from question_bank import QUESTION_BANK
import database as db

def render_diagnostic():
    st.header("🧠 Role-Based Diagnostic Assessment")
    st.markdown("Determine your baseline skills for your target job role.")
    
    target_role = st.text_input("Enter your target Job Role (e.g., Software Engineer, Data Scientist):", 
                                value=st.session_state.get('current_target_role', ''))
                                
    if target_role != st.session_state.get('current_target_role', ''):
        st.session_state.current_target_role = target_role
        st.session_state.diagnostic_generated = False
        st.session_state.diagnostic_submitted = False
        if 'diagnostic_questions' in st.session_state:
            del st.session_state.diagnostic_questions
    
    if target_role:
        if not st.session_state.get('diagnostic_generated', False):
            if st.button("Generate Assessment"):
                with st.spinner(f"Fetching 10 questions from the Question Bank..."):
                    
                    # Target Role Matching Logic
                    matched_category = "General IT"
                    for key in QUESTION_BANK.keys():
                        if key.lower() in target_role.lower():
                            matched_category = key
                            break
                    
                    st.session_state.diagnostic_questions = random.sample(QUESTION_BANK[matched_category], 10)
                    st.session_state.diagnostic_answers = {}
                    st.session_state.diagnostic_submitted = False
                    st.session_state.diagnostic_generated = True
                    st.rerun()
        
        if st.session_state.get('diagnostic_generated', False):
            if not st.session_state.get('diagnostic_questions'):
                st.error("Failed to generate questions. Please try again.")
                return
                
            if st.session_state.diagnostic_submitted:
                st.success("Assessment Complete! Evaluating your skill gaps...")
                
                # Calculate Score
                score = 0
                total = len(st.session_state.diagnostic_questions)
                for i, q in enumerate(st.session_state.diagnostic_questions):
                    selected = st.session_state.diagnostic_answers.get(i)
                    correct = q['answer']
                    if selected == correct:
                        score += 1
                        st.markdown(f"✅ **Q{i+1}: {q['q']}** - Correct!")
                    else:
                        st.markdown(f"❌ **Q{i+1}: {q['q']}** - Incorrect.")
                        st.markdown(f"*Your Answer: {selected} | Correct Answer: {correct}*")
                        
                st.metric(label="Diagnostic Score", value=f"{score}/{total}")
                
                if score == total:
                    st.balloons()
                    st.markdown("### 🌟 Outstanding! You have a solid foundation.")
                else:
                    st.markdown("### 📈 Baseline Established. The AI is crafting your roadmap.")
                    
                if st.button("Retake Assessment"):
                    st.session_state.diagnostic_generated = False
                    st.session_state.diagnostic_submitted = False
                    del st.session_state.diagnostic_questions
                    st.rerun()
                    
                st.markdown("---")
                if st.button("🚀 Generate My Custom AI Roadmap", type="primary"):
                    st.session_state['target_role'] = target_role
                    st.session_state['change_page_to'] = "Learning Roadmap"
                    st.rerun()
            else:
                with st.form("diagnostic_form"):
                    for i, q in enumerate(st.session_state.diagnostic_questions):
                        st.markdown(f"**Q{i+1}: {q['q']}**")
                        st.session_state.diagnostic_answers[i] = st.radio(
                            "Select your answer",
                            options=q['options'],
                            key=f"q_{i}",
                            index=None
                        )
                        st.write("---")
                        
                    submitted = st.form_submit_button("Submit Assessment")
                    if submitted:
                        # Check if all answered
                        if None in st.session_state.diagnostic_answers.values() or len(st.session_state.diagnostic_answers) < len(st.session_state.diagnostic_questions):
                            st.error("Please answer all questions before submitting.")
                        else:
                            st.session_state.diagnostic_submitted = True
                            # In a real app, save score to db
                            db.update_user_xp(st.session_state.user['id'], 100) # Give XP for taking diagnostic
                            st.session_state.user['xp'] += 100 # update local state
                            st.rerun()
