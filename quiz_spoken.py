import csv
import random
from gtts import gTTS
import streamlit as st
import os
import time

# Load the CSV file
@st.cache_data
def load_questions():
    with open('vragenENG.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

vragenlijst = load_questions()
random.shuffle(vragenlijst)

# Session state to keep track of current question
if 'index' not in st.session_state:
    st.session_state.index = 0

# Show next question
if st.session_state.index < len(vragenlijst):
    vraag = vragenlijst[st.session_state.index]['vraag']
    antwoord = vragenlijst[st.session_state.index]['antwoord']

    st.markdown(f"### Vraag {st.session_state.index + 1}:")
    st.write(vraag)

    tts_vraag = gTTS(text=vraag, lang='nl')
    vraag_file = f"vraag_{st.session_state.index}.mp3"
    tts_vraag.save(vraag_file)
    st.audio(vraag_file, format='audio/mp3')

    if st.button("Toon antwoord"):
        st.write(antwoord)
        tts_antwoord = gTTS(text=antwoord, lang='nl')
        antwoord_file = f"antwoord_{st.session_state.index}.mp3"
        tts_antwoord.save(antwoord_file)
        st.audio(antwoord_file, format='audio/mp3')

        if st.button("Volgende vraag"):
            st.session_state.index += 1
            st.rerun()
else:
    st.write("🎉 Je bent klaar met alle vragen!")
