import streamlit as st
import pandas as pd
from murf_api import play_tts, SAFE_VOICES
from evaluator import evaluate_answer

st.set_page_config(page_title="MockMate - Mock Interview", layout="centered")

# Load CSV
@st.cache_data
def load_questions():
    try:
        return pd.read_csv("D:/project/interview_questions_with_answers.csv")
    except FileNotFoundError:
        st.error("CSV file not found.")
        return pd.DataFrame()

questions_df = load_questions()

# --- Session State ---
if 'interview_started' not in st.session_state:
    st.session_state.interview_started = False
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'filtered_questions' not in st.session_state:
    st.session_state.filtered_questions = []
if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}
if 'feedback_results' not in st.session_state:
    st.session_state.feedback_results = {}

st.title("🎤 Mock Interview Session")

# Sidebar
with st.sidebar:
    st.header("Interview Settings")
    if not questions_df.empty:
        roles = sorted(questions_df["Role"].unique())
        companies = sorted(questions_df["Company"].unique())
        selected_role = st.selectbox("Select Role", roles)
        selected_company = st.selectbox("Select Company", companies)
        selected_voice = st.selectbox("Select Voice", SAFE_VOICES, index=0)

        if st.button("Start Interview"):
            st.session_state.interview_started = True
            filtered = questions_df[
                (questions_df["Role"] == selected_role) &
                (questions_df["Company"] == selected_company)
            ].sample(frac=1).reset_index(drop=True)
            st.session_state.filtered_questions = filtered.to_dict('records')
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.feedback_results = {}
    else:
        st.info("Ensure the CSV file is available.")

# Interview Section
if st.session_state.interview_started:
    if st.session_state.current_question_index < len(st.session_state.filtered_questions):
        current_q = st.session_state.filtered_questions[st.session_state.current_question_index]
        question_text = current_q['Question']
        model_answer = current_q.get('Answer', '')
        keywords = current_q.get('Keywords', '')

        st.subheader(f"Question {st.session_state.current_question_index + 1}: {question_text}")
        play_tts(question_text, voice_id=selected_voice)

        user_answer = st.text_area("Your Answer", key=f"answer_{st.session_state.current_question_index}", height=150)
        col1, col2 = st.columns(2)

        with col1:
            if st.button("Submit Answer"):
                feedback = evaluate_answer(user_answer, keywords, model_answer)
                st.session_state.user_answers[st.session_state.current_question_index] = user_answer
                st.session_state.feedback_results[st.session_state.current_question_index] = feedback
                st.write("**Model Answer:**", model_answer)
                st.write("**Feedback Comments:**", feedback['comments'])
                play_tts(feedback['comments'], voice_id=selected_voice)

        with col2:
            if st.button("Next Question"):
                if not user_answer.strip():
                    st.warning("Please provide an answer before moving on.")
                else:
                    st.session_state.current_question_index += 1
                    st.rerun()

    else:
        st.subheader("Interview Complete!")
        st.write("Summary of answers and feedback:")
        st.balloons()
        for i, q in enumerate(st.session_state.filtered_questions):
            st.markdown("---")
            st.write(f"**Q{i+1}:** {q['Question']}")
            st.write(f"**Your Answer:** {st.session_state.user_answers.get(i,'No answer')}")
            st.write(f"**Model Answer:** {q.get('Answer','')}")
            st.write(f"**Feedback:** {st.session_state.feedback_results.get(i,'No feedback')['comments']}")

        if st.button("Restart Interview"):
            st.session_state.interview_started = False
            st.session_state.current_question_index = 0
            st.session_state.filtered_questions = []
            st.session_state.user_answers = {}
            st.session_state.feedback_results = {}
            st.rerun()
else:
    st.info("Select your role, company, and voice from the sidebar and click 'Start Interview'.")
