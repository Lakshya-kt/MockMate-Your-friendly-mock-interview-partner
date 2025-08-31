import streamlit as st
import pandas as pd
from murf_api import play_tts
from evaluator import evaluate_answer

st.set_page_config(page_title="MockMate - Mock Interview", layout="centered")

# --- Load CSV with questions and answers ---
@st.cache_data
def load_questions():
    try:
        # Update this path to your CSV with Question & Answer columns
        return pd.read_csv("D:\project\interview_questions_with_answers.csv")
    except FileNotFoundError:
        st.error("Error: 'interview_questions_tech_with_answers.csv' file not found.")
        return pd.DataFrame()

questions_df = load_questions()

# --- Streamlit Session State ---
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

# --- Sidebar: Role & Company Selection ---
with st.sidebar:
    st.header("Interview Settings")
    if not questions_df.empty:
        roles = sorted(questions_df["Role"].unique())
        companies = sorted(questions_df["Company"].unique())

        selected_role = st.selectbox("Select Role", roles)
        selected_company = st.selectbox("Select Company", companies)

        if st.button("Start Interview"):
            st.session_state.interview_started = True
            # Filter and shuffle
            filtered = questions_df[
                (questions_df["Role"] == selected_role) &
                (questions_df["Company"] == selected_company)
            ].sample(frac=1).reset_index(drop=True)
            st.session_state.filtered_questions = filtered.to_dict('records')
            st.session_state.current_question_index = 0
            st.session_state.user_answers = {}
            st.session_state.feedback_results = {}
    else:
        st.info("Please ensure the CSV file with answers is available.")

# --- Interview Section ---
if st.session_state.interview_started:
    if st.session_state.current_question_index < len(st.session_state.filtered_questions):
        current = st.session_state.filtered_questions[st.session_state.current_question_index]
        question_text = current['Question']
        correct_answer = current['Answer']

        st.subheader(f"Question {st.session_state.current_question_index + 1}:")
        st.write(question_text)

        # Play question audio
        play_tts(question_text)

        # Answer input
        user_answer = st.text_area("Your Answer", key=f"answer_{st.session_state.current_question_index}", height=150)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Submit Answer"):
                # Evaluate with improved evaluator
                feedback = evaluate_answer(user_answer, correct_answer)
                st.session_state.user_answers[st.session_state.current_question_index] = user_answer
                st.session_state.feedback_results[st.session_state.current_question_index] = feedback
                st.write(f"**Feedback:** {feedback}")
                # Play feedback audio
                play_tts(feedback)

        with col2:
            if st.button("Next Question"):
                if not user_answer.strip():
                    st.warning("Please provide an answer before moving on.")
                else:
                    st.session_state.current_question_index += 1
                    st.rerun()

    else:
        # --- Interview Summary ---
        st.subheader("Interview Complete!")
        st.write("Here is a summary of your answers and feedback:")
        st.balloons()

        for i, q in enumerate(st.session_state.filtered_questions):
            st.markdown("---")
            st.write(f"**Q{i+1}:** {q['Question']}")
            st.write(f"**Correct Answer:** {q['Answer']}")
            st.write(f"**Your Answer:** {st.session_state.user_answers.get(i, 'No answer')}")
            st.write(f"**Feedback:** {st.session_state.feedback_results.get(i, 'No feedback')}")

        if st.button("Restart Interview"):
            st.session_state.interview_started = False
            st.session_state.current_question_index = 0
            st.session_state.filtered_questions = []
            st.session_state.user_answers = {}
            st.session_state.feedback_results = {}
            st.rerun()

else:
    st.info("Select your role and company from the sidebar and click 'Start Interview' to begin.")
