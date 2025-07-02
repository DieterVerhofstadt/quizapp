import streamlit as st
import pandas as pd
from gtts import gTTS
import os
import random
import tempfile

# Laad CSV
@st.cache_data
def load_questions():
    return pd.read_csv("vragen.csv")

data = load_questions()

# Selecteer een random vraag
if "index" not in st.session_state:
    st.session_state.index = random.randint(0, len(data) - 1)

vraag = data.loc[st.session_state.index, "vraag"]
antwoord = data.loc[st.session_state.index, "antwoord"]

st.title("🎤 Quiz met Spraak")
st.write(f"**vraag:** {vraag}")

# Genereer en speel TTS-audio af
if st.button("Lees de vraag voor"):
    tts = gTTS(vraag, lang='nl')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# Toon antwoord
if st.button("Toon antwoord"):
    st.write(f"**antwoord:** {antwoord}")
    tts = gTTS(antwoord, lang='nl')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        st.audio(fp.name, format="audio/mp3")

# Nieuwe vraag
if st.button("Nieuwe vraag"):
    st.session_state.index = random.randint(0, len(data) - 1)
    st.rerun()
