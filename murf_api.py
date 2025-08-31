from murf import Murf
import streamlit as st

# Initialize Murf client
API_KEY = "Your_api_key"  # Replace with your actual Murf API key
client = Murf(api_key=API_KEY)

# List of safe voices (fetched from Murf API or docs)
SAFE_VOICES = [
    "en-US-ken", "en-US-natalie","en-US-amara", "en-IN-aarav", "hi-IN-amit", "ta-IN-iniya"
]

def play_tts(text, voice_id="en-US-ken"):
    """
    Generate and play TTS audio using Murf.
    """
    if not text.strip():
        st.warning("No text provided for TTS.")
        return

    if voice_id not in SAFE_VOICES:
        st.error(f"Invalid voice_id '{voice_id}'. Please choose a valid one.")
        return

    try:
        response = client.text_to_speech.generate(
            text=text,
            voice_id=voice_id
        )
        audio_file = response.audio_file  # This is bytes
        st.audio(audio_file)
    except Exception as e:
        st.error(f"TTS Error: {str(e)}")


