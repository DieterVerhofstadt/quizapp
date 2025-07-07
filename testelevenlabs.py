import streamblabs as st
import io
from elevenlabs import generate, play, save, set_api_key
set_api_key(st.secrets["elevenlabs"]["api_key"])

def create_eleven_mp3(text, voice, model):
    audio = generate(
        text=text,
        voice=voice,
	model=model
        stream=False  # stream=True geeft een generator, stream=False geeft bytes
    )
    mp3_fp = io.BytesIO(audio)  # audio is al mp3-bytestream
    return mp3_fp

if st.button("Einde"):
    create_eleven_mp3('Leuk dat je deze quiz gespeeld hebt', voice="Tijs", model="eleven_monolingual_v1")
