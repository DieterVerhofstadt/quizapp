import csv
import random
from utils import create_tts_mp3
from utils import pauze
from utils import merge_csv
import streamlit as st
import io

st.title("Audioquiz")
st.write("Kies een onderwerp. De app bouwt een mp3 met het getoonde aantal vragen, uit een grote vragenlijst over het onderwerp. Die mp3 kan je vervolgens afspelen. Als je hetzelfde onderwerp nog eens kiest, krijg je opnieuw dat aantal random vragen, dus misschien soms dezelfde. Je kan met de slider het aantal aanpassen, dat standaard op 20 ingesteld staat. Reken op een minuut per vijf vragen.")

aantal_vragen = st.slider("Aantal vragen.", min_value=5, max_value=50, value=20, step=5)

if 'screen' not in st.session_state:
    st.session_state.screen = 'home'
def go_to_home():
    st.session_state.screen = 'home'

col1, col2, col3 = st.columns(3)

def create_one_mp3_quiz(vragen):
    with open(vragen, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vragenlijst = list(reader)

    random_vragen = random.sample(vragenlijst, aantal_vragen)

    combined_mp3 = b""

    for rij in random_vragen:
        vraag = rij['vraag']
        antwoord = rij['antwoord']
        vraag_audio = create_tts_mp3(vraag)
        pauze_na_vraag_audio = pauze(15)
        antwoord_audio = create_tts_mp3(antwoord)
        pauze_na_antwoord_audio = pauze(5)
        combined_mp3 += vraag_audio + pauze_na_vraag_audio + antwoord_audio + pauze_na_antwoord_audio

    return st.audio(io.BytesIO(combined_mp3), format="audio/mpeg")

with col1: 
    if st.button("Wetenschap"):
        create_one_mp3_quiz('csv/wetenschap.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Aardrijkskunde"):
        create_one_mp3_quiz('csv/aardrijkskunde.csv')
        if st.button("Terug naar start"):
            go_to_home() 
    elif st.button("Geschiedenis"):
        create_one_mp3_quiz('csv/geschiedenis.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Sport"):
        create_one_mp3_quiz('csv/sport.csv')
        if st.button("Terug naar start"):
            go_to_home()     
    elif st.button("Kunst"):
        create_one_mp3_quiz('csv/kunst.csv')
        if st.button("Terug naar start"):
            go_to_home() 
    elif st.button("Literatuur"):
        create_one_mp3_quiz('csv/literatuur.csv')
        if st.button("Terug naar start"):
            go_to_home()     
    elif st.button("Actua en personalia"):
        create_one_mp3_quiz('csv/actuapersonalia.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Mythologie en religie"):
        create_one_mp3_quiz('csv/mythologie.csv')
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
    elif st.button("Chemische elementen"):
        create_one_mp3_quiz('csv/chemische elementen.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Presidenten van de VS"):
        create_one_mp3_quiz('csv/presidenten.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Hoofdsteden van de wereld"):
        create_one_mp3_quiz('csv/hoofdsteden.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Romeinse keizers"):
        create_one_mp3_quiz('csv/romeinse_keizers.csv')
        if st.button("Terug naar start"):
            go_to_home()
with col3:             
    if st.button("Schaduw Red Michiel"):
        create_one_mp3_quiz('csv/Schaduw Red Michiel.csv')
        if st.button("Terug naar start"):
            go_to_home()         
    elif st.button("Schaduw Plaziet"):
        create_one_mp3_quiz('csv/Schaduw Plaziet.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Schaduw Kwisspels"):
        create_one_mp3_quiz('csv/Schaduw Kwisspels.csv')
        if st.button("Terug naar start"):
            go_to_home()
    elif st.button("Alles door elkaar"):
        merge_csv()
        create_one_mp3_quiz('csv/samengevoegd.csv')
        if st.button("Terug naar start"):
            go_to_home()
























