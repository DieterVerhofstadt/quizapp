import streamlit as st
import io

from elevenlabs.client import ElevenLabs

client = ElevenLabs(
    api_key=st.secrets["elevenlabs"]["api_key"]
)

def create_eleven_mp3(text, voice, model):
    audio = client.text_to_speech.convert(
        text=text,
        voice_id=voice,
	model_id=model,
    )
    mp3_fp = io.BytesIO(audio)  # audio is al mp3-bytestream
    return mp3_fp

if st.button("Einde"):
    audio_bytes = create_eleven_mp3('Leuk dat je deze quiz gespeeld hebt', voice="Rachel", model="eleven_monolingual_v1")
    st.audio(audio_bytes, format="audio/mp3")
