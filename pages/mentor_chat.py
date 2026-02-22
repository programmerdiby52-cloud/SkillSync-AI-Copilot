import streamlit as st
import ai_utils
import database as db

def render_mentor():
    st.header("🤖 24/7 AI Mentor & Soft Skills Simulator")
    
    mode_toggle = st.radio("Select Interaction Mode", ["Academic Mentor", "HR Manager (Soft Skills Simulator)"], horizontal=True)
    mode_key = "mentor_chat" if mode_toggle == "Academic Mentor" else "hr_chat"
    ai_mode = "mentor" if mode_toggle == "Academic Mentor" else "hr"
    
    if mode_key not in st.session_state:
        st.session_state[mode_key] = []
        if ai_mode == "hr":
            st.session_state[mode_key].append({"role": "assistant", "content": "Welcome to the behavioral interview simulation. To begin, tell me about a time you had to overcome a disagreement in a team project."})
        else:
             st.session_state[mode_key].append({"role": "assistant", "content": f"Hi {st.session_state.user['username']}! What engineering concepts can I help explain today?"})

    # Display chat messages from history
    for message in st.session_state[mode_key]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
    # Check for HR mode rating logic (Dummy injection for soft skill score)
    if ai_mode == "hr" and len(st.session_state[mode_key]) > 4:
         st.sidebar.success("Soft skill assessment logged.")
         if st.sidebar.button("Update Soft Skills Score"):
              db.update_user_xp(st.session_state.user['id'], 0) # Just pinging db in real app, let's just update local
              st.session_state.user['soft_skills_score'] = min(100, st.session_state.user['soft_skills_score'] + 10)
              st.sidebar.write("Score bumped to", st.session_state.user['soft_skills_score'])
              
    # React to user input
    if prompt := st.chat_input("Type your message here..."):
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        # Add user message to chat history
        st.session_state[mode_key].append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            stream = ai_utils.mentor_chat_stream(st.session_state[mode_key], mode=ai_mode)
            response = st.write_stream(stream)
        # Add assistant response to chat history
        st.session_state[mode_key].append({"role": "assistant", "content": response})

# Force Streamlit to reload the cache and clear out the old Python bytecode
