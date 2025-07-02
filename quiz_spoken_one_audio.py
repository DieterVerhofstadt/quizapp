import csv
import random
from gtts import gTTS
import streamlit as st
import io

st.title("Audioquiz – alle vragen in één fragment")

def create_tts_mp3(text):
    if not text.strip():
        text = "Simulatie van stilte"  # fallback bij lege tekst
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl')
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()

def create_silence(duration=5):
    # Simuleer stilte met herhaling van "uh"
    text = " ".join(["Simulatie van stilte"] * duration)
    return create_tts_mp3(text)

if st.button("Start quiz"):
    with open('vragen.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vragenlijst = list(reader)

    random.shuffle(vragenlijst)

    combined_mp3 = b""

    for rij in vragenlijst:
        vraag = rij['vraag']
        antwoord = rij['antwoord']

        vraag_audio = create_tts_mp3(vraag)
        stilte = create_silence(duration=3)  # ongeveer 3 seconden “stilte”
        antwoord_audio = create_tts_mp3(antwoord)

        combined_mp3 += vraag_audio + stilte + antwoord_audio

    st.audio(io.BytesIO(combined_mp3), format="audio/mp3")
    st.download_button("Download mp3", data=combined_mp3, file_name="quiz.mp3", mime="audio/mpeg")
