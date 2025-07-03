import csv
import random
from gtts import gTTS
import streamlit as st
import io

st.title("Audioquiz – tien vragen op een rij")

def create_tts_mp3(text):
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl')
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()

def pauze():
    text = '<speak>Pauze<break time="5000ms"/>, Einde pauze.</speak>'  
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl', tld='com') 
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()


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
        pauze_audio = pauze()
        antwoord_audio = create_tts_mp3(antwoord)
        volgende = create_tts_mp3("Volgende vraag")
        combined_mp3 += vraag_audio + pauze_audio + antwoord_audio + volgende

    st.audio(io.BytesIO(combined_mp3), format="audio/mp3")
