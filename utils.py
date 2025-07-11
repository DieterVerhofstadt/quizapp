import io
from gtts import gTTS
import pandas as pd
import os
import requests

def create_tts_mp3(text):
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl', slow=False)
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()
    
def pauze(number):
    mp3_fp = io.BytesIO()
    tts = gTTS("¤", lang='fr') 
    tts.write_to_fp(mp3_fp)
    return number*mp3_fp.getvalue()

def merge_csv():
    # Pad naar de map met CSV-bestanden
    map_pad = "csv"
    # Alle CSV-bestanden in de map vinden
    alle_bestanden = [f for f in os.listdir(map_pad) if f.endswith('.csv')]
    # Lege lijst om alle dataframes op te slaan
    dataframes = []
    for bestand in alle_bestanden:
        volledig_pad = os.path.join(map_pad, bestand)
        df = pd.read_csv(volledig_pad)
        dataframes.append(df)

import requests

def get_pages_from_category(category_name, limit=50):
    S = requests.Session()
    URL = "https://nl.wikipedia.org/w/api.php"
    
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": f"Categorie:{category_name}",
        "cmlimit": limit,
        "format": "json"
    }

    response = S.get(url=URL, params=params)
    data = response.json()
    return [item["title"] for item in data["query"]["categorymembers"]]

