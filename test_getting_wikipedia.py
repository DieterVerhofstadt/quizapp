import streamlit as st
from utils import get_pages_from_category, get_summary
categorie = "Winnaar_van_de_Nobelprijs_voor_Literatuur"
pagina_titels = get_pages_from_category(categorie)
if st.button("Go"):
    for titel in pagina_titels:
        samenvatting = get_summary(titel)
        print(f"** {titel} **")
        print(samenvatting)
        print()
