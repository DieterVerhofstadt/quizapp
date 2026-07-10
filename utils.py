import io
import os
import csv
from gtts import gTTS
import pandas as pd


RESULTATEN_MAP = "resultaten"


def create_tts_mp3(text):
    mp3_fp = io.BytesIO()
    tts = gTTS(text=text, lang='nl', tld='be', slow=False)
    tts.write_to_fp(mp3_fp)
    return mp3_fp.getvalue()


def pauze(number):
    mp3_fp = io.BytesIO()
    tts = gTTS("¤", lang='fr')
    tts.write_to_fp(mp3_fp)
    return number * mp3_fp.getvalue()


def merge_csv():
    map_pad = "csv"
    alle_bestanden = [f for f in os.listdir(map_pad) if f.endswith('.csv')]
    dataframes = []
    for bestand in alle_bestanden:
        volledig_pad = os.path.join(map_pad, bestand)
        df = pd.read_csv(volledig_pad)
        dataframes.append(df)
    return pd.concat(dataframes, ignore_index=True)


def dataset_key(csv_path):
    """Veilige, vaste sleutel voor een dataset (geen spaties), gebruikt in
    bestandsnamen van de resultaten-CSV's."""
    naam = os.path.splitext(os.path.basename(csv_path))[0]
    return naam.lower().replace(" ", "-")


def load_weights(csv_path, vragenlijst):
    """Berekent per vraag een gewicht op basis van eerdere resultaten:
    vragen die je vaker fout had, krijgen een hoger gewicht (tot 5x).
    Vragen zonder geschiedenis krijgen een neutraal gewicht van 1.0."""
    key = dataset_key(csv_path)
    result_file = os.path.join(RESULTATEN_MAP, f"{key}.csv")

    stats = {}  # vraag -> [aantal_fout, aantal_totaal]
    if os.path.exists(result_file):
        with open(result_file, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                vraag = row.get('vraag', '')
                correct_raw = str(row.get('correct', '')).strip().lower()
                correct = correct_raw in ('true', '1', 'goed', 'yes')
                stats.setdefault(vraag, [0, 0])
                stats[vraag][1] += 1
                if not correct:
                    stats[vraag][0] += 1

    weights = []
    for rij in vragenlijst:
        vraag = rij['vraag']
        fout, totaal = stats.get(vraag, [0, 0])
        if totaal == 0:
            weights.append(1.0)
        else:
            foutratio = fout / totaal
            weights.append(1.0 + 4.0 * foutratio)
    return weights


def verwerk_geuploade_resultaten(geuploade_bestanden):
    """Voegt geuploade resultaten-CSV's (gedownload vanuit de quiz-component)
    samen met de bestaande logs per dataset. Bestandsnamen van de upload
    moeten beginnen met de dataset_key, gevolgd door '_' (zo genereert de
    component ze automatisch)."""
    os.makedirs(RESULTATEN_MAP, exist_ok=True)
    verwerkt = 0
    for bestand in geuploade_bestanden:
        naam = bestand.name
        key = naam.split('_')[0]
        doelpad = os.path.join(RESULTATEN_MAP, f"{key}.csv")

        df_nieuw = pd.read_csv(bestand)
        if os.path.exists(doelpad):
            df_oud = pd.read_csv(doelpad)
            df_samen = pd.concat([df_oud, df_nieuw], ignore_index=True)
        else:
            df_samen = df_nieuw
        df_samen.to_csv(doelpad, index=False)
        verwerkt += 1
    return verwerkt
