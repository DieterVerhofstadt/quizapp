import csv
import random
from gtts import gTTS
from pydub import AudioSegment
import streamlit as st
import tempfile

st.title("Audio Quiz")

if st.button("Genereer quiz en speel af"):
    # Lees vragen in
    with open('vragen.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vragenlijst = list(reader)

    random.shuffle(vragenlijst)

    quiz_audio = AudioSegment.empty()
    stilte = AudioSegment.silent(duration=5000)  # 5 seconden stilte

    for i, rij in enumerate(vragenlijst):
        vraag = rij['vraag']
        antwoord = rij['antwoord']

        # Vraag en antwoord genereren met gTTS
        tts_vraag = gTTS(text=vraag, lang='nl')
        tts_antwoord = gTTS(text=antwoord, lang='nl')

        # Tijdelijke opslag om te laden met pydub
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_vraag_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_antwoord_file:

            tts_vraag.save(tmp_vraag_file.name)
            tts_antwoord.save(tmp_antwoord_file.name)

            vraag_audio = AudioSegment.from_file(tmp_vraag_file.name)
            antwoord_audio = AudioSegment.from_file(tmp_antwoord_file.name)

            # Voeg toe aan quiz audio
            quiz_audio += vraag_audio + stilte + antwoord_audio + stilte

    # Exporteer gecombineerde quiz
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_quiz:
        quiz_audio.export(tmp_quiz.name, format="mp3")
        st.audio(tmp_quiz.name, format="audio/mp3", start_time=0)