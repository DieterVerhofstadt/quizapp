import csv
import random
from gtts import gTTS
import streamlit as st
import os
import time

with open('vragen.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    vragenlijst = list(reader)  # maak er een lijst van

random.shuffle(vragenlijst)  # schud de lijst door elkaar

for i, rij in enumerate(vragenlijst):
    vraag = rij['vraag']
    antwoord = rij['antwoord']

    tts_vraag = gTTS(text=vraag, lang='nl')
    vraag_file = f"vraag_{i}.mp3"
    tts_vraag.save(vraag_file)
    st.audio(vraag_file, format='audio/mp3')

    time.sleep(5)  # wacht 5 seconden

    tts_antwoord = gTTS(text=antwoord, lang='nl')
    antwoord_file = f"antwoord_{i}.mp3"
    tts_antwoord.save(antwoord_file)
    st.audio(antwoord_file, format='audio/mp3')
