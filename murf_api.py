from murf import Murf
import streamlit as st

# Initialize Murf Client
client = Murf(api_key="Your_api_key")

def play_tts(text, voice_id="en-US-terrell"):
    try:
        # Generate TTS audio using Murf
        res = client.text_to_speech.generate(
            text=text,
            voice_id=voice_id,
            format="MP3",
            sample_rate=44100.0
        )

        # Get the audio file URL
        audio_url = res.audio_file

        if audio_url:
            st.audio(audio_url, format="audio/mp3")
        else:
            st.error("No audio file URL returned from Murf API.")
    except Exception as e:
        st.error(f"Failed to generate TTS: {e}")

