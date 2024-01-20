import streamlit as st
import os

import numpy as np
import pandas as pd

import sys
sys.path.append("..")

from bookbeat.playlist_generation import playlist_popularity

# -- Set page config
app_page_title = 'About BookBeat'

st.set_page_config(page_title=app_page_title, page_icon=":book:")

color_fondo = "#EFF5FF"

# Aplicar el estilo de fondo usando CSS
st.markdown(
    f"""
    <style>
        body {{
            background-color: {color_fondo};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

st.image("../raw_data/BookBeat_3.png")

st.write('''BookBeat revoluciona la lectura al sincronizar
         la música perfecta para cada libro. ''')

st.write('''Crea tu playlist única para
         tener una experiencia de *lectura inmersiva* y *emocionalmente sincronizada*.''')

st.write('''**¡Con BookBeat disfruta de tus libros favoritos con la banda sonora perfecta!**''')

st.image("../raw_data/Modelo_2.png")

st.image("../raw_data/Equipo_2.png")
