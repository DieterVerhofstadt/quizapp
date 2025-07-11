import streamlit as st
from utils import get_pages_from_category
categorie = "Winnaars_van_de_Nobelprijs_voor_Literatuur"
pagina_titels = get_pages_from_category(categorie)
if st.button("Go"):
    for titel in pagina_titels:
        print(titel)
       

