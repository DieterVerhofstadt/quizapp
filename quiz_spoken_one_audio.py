import csv
import random
from gtts import gTTS
import streamlit as st
import io

st.title("Audioquiz – twintig vragen op een rij")

def create_tts_mp3(text):
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl', slow=True)
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()

def pauze():
    mp3_fp = io.BytesIO()
    tts = gTTS("¤", lang='fr') 
    tts.write_to_fp(mp3_fp)
    return 15*mp3_fp.getvalue()

def create_one_mp3_quiz(vragen):
    with open(vragen, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vragenlijst = list(reader)

    random_20_vragen = random.sample(vragenlijst, 20)

    combined_mp3 = b""

    for rij in random_20_vragen:
        vraag = rij['vraag']
        antwoord = rij['antwoord']
        vraag_audio = create_tts_mp3(vraag)
        pauze_audio = pauze()
        antwoord_audio = create_tts_mp3(antwoord)
        volgende = create_tts_mp3("Volgende vraag")
        combined_mp3 += vraag_audio + pauze_audio + antwoord_audio + volgende

    return st.audio(io.BytesIO(combined_mp3), format="audio/mp3")
if st.button("Wetenschap"):
    create_one_mp3_quiz('wetenschap.csv')
elif st.button("Presidenten"):
    create_one_mp3_quiz('presidenten.csv')
elif st.button("Hoofdsteden van de wereld"):
    create_one_mp3_quiz('hoofdsteden.csv')
elif st.button("Wereldkampioenen F1"):
    create_one_mp3_quiz('formule1.csv')
elif st.button("Nobelprijswinnaars literatuur"):
    create_one_mp3_quiz('nobelprijsliteratuur.csv')
elif st.button("Winnaars Ronde van Frankrijk"):
    create_one_mp3_quiz('tourdefrance.csv')
