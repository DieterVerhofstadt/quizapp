import pandas as pd
import os

# Pad naar de map met CSV-bestanden
map_pad = "/csv"

# Alle CSV-bestanden in de map vinden
alle_bestanden = [f for f in os.listdir(map_pad) if f.endswith('.csv')]

# Lege lijst om alle dataframes op te slaan
dataframes = []

for bestand in alle_bestanden:
    volledig_pad = os.path.join(map_pad, bestand)
    df = pd.read_csv(volledig_pad)
    dataframes.append(df)

# Alle dataframes samenvoegen
samengevoegd_df = pd.concat(dataframes, ignore_index=True)

# Resultaat opslaan naar een nieuwe CSV
samengevoegd_df.to_csv("/csv/samengevoegd.csv", index=False)
