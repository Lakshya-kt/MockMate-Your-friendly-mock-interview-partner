# 🎤 MockMate – Your Friendly Mock Interview Partner

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-green.svg)](https://streamlit.io/)
[![Murf AI](https://img.shields.io/badge/Murf-TTS-orange.svg)](https://murf.ai/)

**MockMate** is an interactive voice-enabled mock interview platform for technical roles. It uses Murf AI Text-to-Speech (TTS) and Streamlit to simulate realistic interview experiences. Users can listen to questions, type or record answers, get instant feedback, and receive a spoken performance summary. The project includes a CSV dataset of 1000+ curated technical interview questions across top tech companies and roles such as Software Engineer, Data Scientist, AI Engineer, DevOps Engineer, and QA Engineer.

---

## ✨ Features

- Select role and company for your mock interview  
- Questions read aloud using Murf TTS voices  
- Answer via typing or voice recording  
- Instant feedback highlighting missed key points  
- End-of-session voice summary of performance  
- Export session results to CSV or JSON for review  
- Modular and beginner-friendly Python code

---

## 🛠️ Installation & Setup

Clone the repository and install dependencies:

```bash
---

git clone https://github.com/Lakshya_kt/MockMate-Your-friendly-mock-interview-partner.git
cd MockMate-Your-friendly-mock-interview-partner
pip install -r requirements.txt

---

Create a `.streamlit/secrets.toml` file in the project folder with your Murf API key:

[MURF]  
api_key = "YOUR_MURF_KEY"

Ensure the `interview_questions_tech.csv` dataset is in the project folder.

---

## 🖥️ Usage

Run the Streamlit app:

streamlit run main.py

-Select your role and company in the sidebar
-Press Start Interview
-Answer each question by typing or recording your voice
-Receive feedback after each question
-Listen to the voice summary at the end
-Export your session results using the Download button

---

## 📂 Project Structure

MockMate-Your-friendly-mock-interview-partner/  
├── main.py                       # Streamlit app  
├── murf_api.py                    # Murf TTS interface  
├── evaluator.py                   # Answer evaluation logic  
├── interview_questions_tech.csv   # Dataset of 1000+ technical interview questions  
├── requirements.txt               # Python dependencies  
├── README.md                      # Project documentation  

---

## 📝 Dataset

`interview_questions_tech.csv` contains 1000+ questions:  
Company, Role, Question ID, Question, Category, Difficulty, Keywords  

Covers multiple technical roles and top tech companies. Keywords are used to provide feedback during the session.

---

## ⚡ Dependencies

- Python 3.8+
- Streamlit
- Murf SDK
- pandas
- SpeechRecognition
- PyAudio
- sentence-transformers

---

## 🧩 How It Works

- Loads questions from CSV filtered by role and company  
- Plays questions using Murf TTS  
- Accepts typed or voice answers  
- Evaluates answers with keyword matching  
- Provides feedback after each question  
- Generates a voice summary at the end  
- Allows exporting results as CSV or JSON

---

## 🔒 Notes

- Your Murf API key must remain private. Do not commit it to GitHub  
- Feedback is based on simple keyword matching  
- Streamlit `st.audio_input` captures microphone answers

---

## 📄 License

This project is licensed under the **MIT License**.  
See the [LICENSE](LICENSE) file for more details.

---

## 🙏 Acknowledgements

- Murf AI for TTS API  
-Streamlit for the interactive interface
-Sentence Transformers for semantic similarity




