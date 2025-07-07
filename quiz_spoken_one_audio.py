import csv
import random
from utils import create_tts_mp3
#from utils import create_eleven_mp3
from utils import pauze
import streamlit as st
import io

st.title("Audioquiz")
st.write("Kies je onderwerp. De app bouwt een mp3 met 20 vragen, random gekozen uit een vragenlijst over het onderwerp, die je kan afspelen. Als je hetzelfde onderwerp nog eens kiest, krijg je opnieuw 20 random vragen, dus misschien soms dezelfde.")

if 'screen' not in st.session_state:
    st.session_state.screen = 'home'
def go_to_home():
    st.session_state.screen = 'home'

col1, col2 = st.columns(2)

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
        pauze_na_vraag_audio = pauze(15)
        antwoord_audio = create_tts_mp3(antwoord)
        pauze_na_antwoord_audio = pauze(5)
        combined_mp3 += vraag_audio + pauze_na_vraag_audio + antwoord_audio + pauze_na_antwoord_audio

    return st.audio(io.BytesIO(combined_mp3), format="audio/mp3")

with col1: 
    if st.button("Wetenschap"):
        create_one_mp3_quiz('csv/wetenschap.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Presidenten"):
        create_one_mp3_quiz('csv/presidenten.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Hoofdsteden van de wereld"):
        create_one_mp3_quiz('csv/hoofdsteden.csv')
        if st.button("Terug naar start"):
            go_to_home()

with col2:    
    if st.button("Wereldkampioenen F1"):
        create_one_mp3_quiz('csv/formule1.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Nobelprijswinnaars literatuur"):
        create_one_mp3_quiz('csv/nobelprijsliteratuur.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Winnaars Ronde van Frankrijk"):
        create_one_mp3_quiz('csv/tourdefrance.csv')
        if st.button("Terug naar start"):
            go_to_home()

#if st.button("Einde"):
    #create_eleven_mp3('Leuk dat je deze quiz gespeeld hebt', voice="Tijs", model="eleven_monolingual_v1")
