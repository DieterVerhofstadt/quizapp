import csv
import random
from gtts import gTTS
import streamlit as st
import io
import time

st.title("Audioquiz – alle vragen in één fragment")

def create_tts_mp3(text):
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl')
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()

def create_silence(duration_ms=5000):
    # 5 seconden stilte als lege MP3 – workaround: gebruik een stil stukje van TTS
    silent_text = "."  # gTTS maakt hiervan een korte pauze
    mp3_data = create_tts_mp3(silent_text)
    return mp3_data

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
        stilte = create_silence()
        antwoord_audio = create_tts_mp3(antwoord)

        combined_mp3 += vraag_audio + stilte + antwoord_audio + stilte

    st.audio(io.BytesIO(combined_mp3), format="audio/mp3")

    st.download_button("Download mp3", data=combined_mp3, file_name="quiz.mp3", mime="audio/mpeg")
