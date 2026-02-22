import streamlit as st
import PyPDF2
import ai_utils
import io

def render_learning_engine():
    st.header("📚 Custom Module Engine")
    st.markdown("Upload your University PDF modules. The AI will analyze the text, memorize it, and generate highly targeted quizzes exclusively from this material.")
    
    uploaded_file = st.file_uploader("Upload Course Material (PDF)", type="pdf")
    
    if uploaded_file is not None:
        with st.spinner("Extracting text and feeding contextual memory..."):
            # Read PDF
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            text = ""
            for page in range(len(pdf_reader.pages)):
                text += pdf_reader.pages[page].extract_text()
                
            st.success(f"Successfully memorized {len(pdf_reader.pages)} pages of content.")
            
            with st.expander("Preview Extracted Text"):
                st.text(text[:1000] + "...\n[Content truncated for display]")
                
            if st.button("🧠 Generate Custom Quiz"):
                with st.spinner("Analyzing text and framing questions..."):
                    quiz = ai_utils.generate_pdf_quiz(text)
                    st.session_state.pdf_quiz = quiz
                    st.session_state.pdf_answers = {}
                    
        if 'pdf_quiz' in st.session_state:
            st.markdown("---")
            st.subheader("📝 Module Assessment")
            with st.form("pdf_quiz_form"):
                for i, q in enumerate(st.session_state.pdf_quiz):
                    st.markdown(f"**Q{i+1}: {q['question']}**")
                    st.session_state.pdf_answers[i] = st.radio(
                        "Options",
                        options=q['options'],
                        key=f"pdf_q_{i}",
                        index=None
                    )
                    st.write("---")
                    
                if st.form_submit_button("Submit Answers"):
                    score = 0
                    for i, q in enumerate(st.session_state.pdf_quiz):
                        if st.session_state.pdf_answers.get(i) == q['answer']:
                            score += 1
                    st.success(f"You scored {score}/{len(st.session_state.pdf_quiz)} on this module!")

