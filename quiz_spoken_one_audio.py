import csv
import random
from gtts import gTTS
import streamlit as st
import io

st.title("Audioquiz – alle vragen in één fragment")

def create_tts_mp3(text):
    if not text.strip():
        text = "Ik herhaal:"  # fallback bij lege tekst
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl')
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()

def herhaal():
    # Simuleer stilte met herhaling van "uh"
    text = "Ik herhaal:"
    return create_tts_mp3(text)
    
if st.button("Start quiz"):
    with open('vragen.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vragenlijst = list(reader)

   random_10_vragen = random.sample(vragenlijst, 10)

    combined_mp3 = b""

    for rij in random_10_vragen:
        vraag = rij['vraag']
        antwoord = rij['antwoord']
        vraag_audio = create_tts_mp3(vraag)
        herhaal = create_tts_mp3("Ik herhaal")
        antwoord_audio = create_tts_mp3(antwoord)
        combined_mp3 += vraag_audio + herhaal + vraag_audio + antwoord_audio

    st.audio(io.BytesIO(combined_mp3), format="audio/mp3")
    st.download_button("Download mp3", data=combined_mp3, file_name="quiz.mp3", mime="audio/mpeg")
