import csv
import time
import random
from gtts import gTTS
import streamlit as st
import os

with open('vragenENG.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    vragenlijst = list(reader)  # maak er een lijst van

random.shuffle(vragenlijst)  # schud de lijst door elkaar

for rij in vragenlijst:
    vraag = rij['vraag']
    antwoord = rij['antwoord']

    engine.say(vraag)
    engine.runAndWait()

    time.sleep(5)  # wacht 5 seconden

    engine.say(antwoord)
    engine.runAndWait()

    time.sleep(2)  # korte pauze voor volgende vraag
