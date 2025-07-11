import streamlit as st
from utils import get_pages_from_category
categorie = "Winnaars_van_de_Nobelprijs_voor_Literatuur"
pagina_titels = get_pages_from_category(categorie)
if st.button("Go"):
    for titel in pagina_titels:
        print(titel)
        # Alle dataframes samenvoegen
        samengevoegd_df = pd.concat(dataframes, ignore_index=True)
        # Resultaat opslaan naar een nieuwe CSV
        samengevoegd_df.to_csv("csv/samengevoegd.csv", index=False)

