import csv
import random
import base64
import numpy as np
import streamlit as st
import streamlit.components.v1 as components

from utils import create_tts_mp3, merge_csv, load_weights, dataset_key, verwerk_geuploade_resultaten
from quiz_component import build_quiz_html

st.title("Audioquiz")
st.write(
    "Kies een onderwerp. De app kiest random vragen uit een grote vragenlijst over dat "
    "onderwerp, speelt ze één voor één af (vraag, bedenktijd, antwoord), en luistert dan "
    "of je zelf 'goed' of 'fout' zegt. Vragen die je vaker fout had, krijgen bij een "
    "volgende ronde een hogere kans om terug te komen. Reken op een minuut per vijf vragen."
)

aantal_vragen = st.slider("Aantal vragen.", min_value=5, max_value=50, value=20, step=5)

if 'screen' not in st.session_state:
    st.session_state.screen = 'home'


def go_to_home():
    st.session_state.screen = 'home'


def weighted_sample_without_replacement(vragenlijst, weights, k):
    k = min(k, len(vragenlijst))
    weights_arr = np.array(weights, dtype=float)
    weights_arr = weights_arr / weights_arr.sum()
    indices = np.random.choice(len(vragenlijst), size=k, replace=False, p=weights_arr)
    return [vragenlijst[i] for i in indices]


def start_quiz(csv_path):
    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vragenlijst = list(reader)

    weights = load_weights(csv_path, vragenlijst)
    gekozen_vragen = weighted_sample_without_replacement(vragenlijst, weights, aantal_vragen)

    quiz_items = []
    with st.spinner("Audio genereren..."):
        for rij in gekozen_vragen:
            vraag = rij['vraag']
            antwoord = rij['antwoord']
            vraag_audio = create_tts_mp3(vraag)
            antwoord_audio = create_tts_mp3(antwoord)
            quiz_items.append({
                "vraag": vraag,
                "antwoord": antwoord,
                "vraag_b64": base64.b64encode(vraag_audio).decode('utf-8'),
                "antwoord_b64": base64.b64encode(antwoord_audio).decode('utf-8'),
            })

    key = dataset_key(csv_path)
    html = build_quiz_html(quiz_items, key)
    components.html(html, height=350, scrolling=True)


col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Wetenschap"):
        start_quiz('csv/wetenschap.csv')
    elif st.button("Aardrijkskunde"):
        start_quiz('csv/aardrijkskunde.csv')
    elif st.button("Geschiedenis"):
        start_quiz('csv/geschiedenis.csv')
    elif st.button("Sport"):
        start_quiz('csv/sport.csv')
    elif st.button("Kunst"):
        start_quiz('csv/kunst.csv')
    elif st.button("F & F"):
        start_quiz('csv/fauna en flora.csv')
    elif st.button("Film en TV"):
        start_quiz('csv/film en tv.csv')
    elif st.button("Literatuur"):
        start_quiz('csv/literatuur.csv')
    elif st.button("Actua en personalia"):
        start_quiz('csv/actuapersonalia.csv')
    elif st.button("Mythologie en religie"):
        start_quiz('csv/mythologie.csv')
    elif st.button("Gastronomie"):
        start_quiz('csv/gastronomie.csv')
    elif st.button("Varia"):
        start_quiz('csv/varia.csv')

with col2:
    if st.button("Wereldkampioenen F1"):
        start_quiz('csv/formule1.csv')
    elif st.button("Nobelprijswinnaars literatuur"):
        start_quiz('csv/nobelprijsliteratuur.csv')
    elif st.button("Winnaars Ronde van Frankrijk"):
        start_quiz('csv/tourdefrance.csv')
    elif st.button("Chemische elementen"):
        start_quiz('csv/chemische elementen.csv')
    elif st.button("Presidenten van de VS"):
        start_quiz('csv/presidenten.csv')
    elif st.button("Hoofdsteden wereld moeilijk"):
        start_quiz('csv/hoofdsteden moeilijk.csv')
    elif st.button("Hoofdsteden VS"):
        start_quiz('csv/hoofdsteden verenigde staten.csv')
    elif st.button("Romeinse keizers"):
        start_quiz('csv/Romeinse keizers.csv')
    elif st.button("Geneeskunde en Biologie"):
        start_quiz('csv/geneeskunde.csv')
    elif st.button("Napoleon"):
        start_quiz('csv/Napoleon.csv')
    elif st.button("Basket en NBA"):
        start_quiz('csv/Basket en NBA.csv')

with col3:
    if st.button("Schaduw Red Michiel"):
        start_quiz('csv/Schaduw Red Michiel.csv')
    elif st.button("Schaduw Plaziet"):
        start_quiz('csv/Schaduw Plaziet.csv')
    elif st.button("Schaduw Kwisspels"):
        start_quiz('csv/Schaduw Kwisspels.csv')
    elif st.button("Schaduw SSGB"):
        start_quiz('csv/Schaduw SSGB.csv')
    elif st.button("Schaduw Incognito"):
        start_quiz('csv/Schaduw Incognito.csv')
    elif st.button("Schaduw Wanhoop"):
        start_quiz('csv/Schaduw Wanhoop.csv')
    elif st.button("Schaduw Conoscenza"):
        start_quiz('csv/Schaduw Conoscenza.csv')
    elif st.button("Schaduw The Entity"):
        start_quiz('csv/Schaduw Entity.csv')
    elif st.button("Schaduw Da's zeker da"):
        start_quiz('csv/Schaduw DasZekerDa.csv')
    elif st.button("Schaduw Terug Naar Af"):
        start_quiz('csv/Schaduw terugnaaraf.csv')
    elif st.button("Schaduw Wodeismedoadde"):
        start_quiz('csv/Wodeismedoadde.csv')
    elif st.button("Ondernemerstool"):
        start_quiz('csv/Ondernemerstool.csv')

st.divider()
st.subheader("Resultaten verwerken")
st.write(
    "Na een quizronde krijg je een 'Download resultaten (CSV)'-knop. Sleep dat "
    "gedownloade bestand hieronder binnen zodat de volgende selectie voor dit "
    "onderwerp rekening houdt met wat je goed en fout had."
)
geuploade_bestanden = st.file_uploader(
    "Resultaten-CSV('s) uploaden", type="csv", accept_multiple_files=True
)
if geuploade_bestanden:
    aantal = verwerk_geuploade_resultaten(geuploade_bestanden)
    st.success(f"{aantal} bestand(en) verwerkt en samengevoegd met de bestaande logs.")
