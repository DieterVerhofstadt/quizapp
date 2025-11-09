import io
from gtts import gTTS
import pandas as pd
import os
import boto3
import requests

def create_tts_mp3(text):
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl', tld='be', slow=False)
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

def get_summary(title):
    safe_title = title.replace(" ", "_")
    url = f"https://nl.wikipedia.org/api/rest_v1/page/summary/{safe_title}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("extract")
    else:
        return None

def create_polly_mp3(text):
    """
    Genereer Vlaamse spraak (Amazon Polly) als MP3-bytes.
    voice: 'Lotte' (vrouw) of 'Arnaud' (man)
    """
    # Maak een Polly-client aan (veronderstelt dat je AWS-keys ingesteld zijn)
    polly = boto3.client('polly', region_name='eu-west-1')  # Ierland-regio ondersteunt nl-BE

    # Vraag de synthese aan
    response = polly.synthesize_speech(
        Text=text,
        OutputFormat='mp3',
        VoiceId='Lotte",
        LanguageCode='nl-BE'  # belangrijk: Belgische variant
    )

    # Lees de audio-output
    if "AudioStream" in response:
        mp3_fp = io.BytesIO(response["AudioStream"].read())
        return mp3_fp.getvalue()
    else:
        raise Exception("Geen audio ontvangen van Polly.")
