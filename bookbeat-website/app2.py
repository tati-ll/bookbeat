import streamlit as st
import os

import numpy as np
import pandas as pd

import sys
sys.path.append("..")

from bookbeat.playlist_generation import playlist_popularity

# -- Set page config
apptitle = 'BookBeat'

st.set_page_config(page_title=apptitle, page_icon=":book:")


@st.cache_data
def carga_dataset():
    # Ruta al archivo CSV
    ruta_books = "../raw_data/books_sentiment.csv"
    ruta_songs = "../raw_data/songs_sentiment.csv"

    # Cargar datos desde el archivo CSV
    data_book = pd.read_csv(ruta_books)
    data_songs = pd.read_csv(ruta_songs)

    return data_book, data_songs

col1, col2 = st.columns(2)

with col1:
   st.title(":blue[BOOKBEAT]")
   st.markdown(''':blue[***¡Disfruta de tus libros favoritos con la banda sonora perfecta!***]''')

with col2:
   st.image("../raw_data/bookbeat.jpg")


#st.markdown("""
#**Selecciona el título de tu libro**
#""")

# data_book, data_songs = carga_dataset()

# # Crear un menú desplegable con la lista de libros
# title = st.selectbox("Selecciona el título de tu libro:", data_book['Book'].tolist(), index=None, key='libro1', placeholder="Choose an option", label_visibility='hidden')

# #Selección de géneros musicales
# # genero = ['pop', 'rock', 'r&b', 'rap', 'edm', 'latin']
# #tipo_musica = st.multiselect("Selecciona generos:", genero, key="musica")

# if not title:
#     st.warning("No se seleccionó ningún libro.")

# # Llamar a la función de generación de playlist
# if st.button("Generar Playlist"):
#     # Resultados de la función basada en el título del libro
#     libro = title
#     resultados_playlist = playlist_popularity(libro, data_book, data_songs)

#     uri= resultados_playlist['URI'].tolist()

#     # Mostrar resultados en Streamlit
#     st.write(resultados_playlist[['track_name','track_artist','URI']])
