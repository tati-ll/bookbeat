import streamlit as st
import os

import numpy as np
import pandas as pd

import sys
sys.path.append("..")

from bookbeat.playlist_generation import playlist_popularity

'''
# BOOKBEAT'''

st.markdown("""
## Select a book
""")

# Ruta al archivo CSV
ruta_books = "../raw_data/books_sentiment.csv"
ruta_songs = "../raw_data/songs_sentiment.csv"

# Cargar datos desde el archivo CSV
data_book = pd.read_csv(ruta_books)
data_songs = pd.read_csv(ruta_songs)


# Crear un menú desplegable con la lista de libros
#libro_seleccionado = st.selectbox("Selecciona un libro:", data['Book'].tolist(), index=0, key='libro')
title = st.multiselect("Selecciona un libro:", data_book['Book'].tolist(), key="libro")

#Selección de géneros musicales
# genero = ['pop', 'rock', 'r&b', 'rap', 'edm', 'latin']
#tipo_musica = st.multiselect("Selecciona generos:", genero, key="musica")

if title:
    st.write(f"Libro seleccionado: {title[0]}")
else:
    st.warning("No se seleccionó ningún libro.")

# Llamar a la función de generación de playlist
if st.button("Generar Playlist"):
    # Resultados de la función basada en el título del libro
    libro = title[0]
    resultados_playlist = playlist_popularity(libro,data_book, data_songs)

    uri= resultados_playlist['URI'].tolist()

    # Mostrar resultados en Streamlit
    st.write(resultados_playlist[['track_name','track_artist','URI']])
