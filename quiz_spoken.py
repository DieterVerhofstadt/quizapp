import csv
import random
from gtts import gTTS
import streamlit as st
import os
import atexit

# Maak mp3-bestanden en geef de lijst terug
def generate_audio_files():
    with open('vragenENG.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        vragenlijst = list(reader)

    random.shuffle(vragenlijst)

    audio_files = []
    os.makedirs("static", exist_ok=True)

    for i, rij in enumerate(vragenlijst):
        vraag = rij['vraag']
        antwoord = rij['antwoord']

        vraag_file = f"static/vraag_{i}.mp3"
        antwoord_file = f"static/antwoord_{i}.mp3"

        gTTS(text=vraag, lang='nl').save(vraag_file)
        gTTS(text=antwoord, lang='nl').save(antwoord_file)

        audio_files.append(vraag_file)
        audio_files.append(antwoord_file)

    return audio_files

if "audio_files" not in st.session_state:
    st.session_state.audio_files = generate_audio_files()

audio_html = """
<audio id="audioPlayer" src="{src}" autoplay></audio>
<script>
  const files = {files};
  let index = 0;
  const player = document.getElementById("audioPlayer");
  player.onended = () => {
    index++;
    if (index < files.length) {
      player.src = files[index];
      player.play();
    }
  };
</script>
"""

# URLs voor Streamlit Cloud moeten naar /static/ map wijzen
files_url = [f"/{file}" for file in st.session_state.audio_files]
first_file = files_url[0]

st.markdown(audio_html.format(src=first_file, files=files_url), unsafe_allow_html=True)

# Optioneel: opschonen van mp3 bestanden bij afsluiten
@atexit.register
def cleanup():
    for file in st.session_state.audio_files:
        if os.path.exists(file):
            os.remove(file)
