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
ruta_books = "../raw_data/isbn_titulo_autor.csv"
ruta_songs = "../raw_data/songs_sentiment.csv"

# Cargar datos desde el archivo CSV
data_book = pd.read_csv(ruta_books)
data_songs = pd.read_csv(ruta_songs)


# Crear un menú desplegable con la lista de libros
# Filtrar títulos únicos
unique_title = data_book['Title'].unique()
libro_seleccionado = st.selectbox("Selecciona un libro:", unique_title, index=None, key='libro', placeholder="Choose an option")

unique_authors = data_book[data_book['Title'] == libro_seleccionado]['Author'].unique()
selected_author = st.selectbox("Selecciona el autor:", unique_authors)

# Filtrar autores si hay varios libros con el mismo título
#if data_book[data_book['Title'] == libro_seleccionado].shape[0] > 1:
#    unique_authors = data_book[data_book['Title'] == libro_seleccionado]['Author'].unique()
#    selected_author = st.selectbox("Selecciona el autor:", unique_authors)
#else:
    # Si solo hay un libro con ese título, no se muestra la selección de autor
#    selected_author = None

if libro_seleccionado:
    st.write(f"Libro seleccionado: {libro_seleccionado} del autor {selected_author}")

button = st.button(":blue[Generar Playlist]")

# Cálculo del sentimiento
if button:
    # Resultados de la función basada en el título del libro
    libro = libro_seleccionado
    resultados_playlist = playlist_popularity(libro, data_book, data_songs)

    uri= resultados_playlist['URI'].tolist()

    # Mostrar resultados en Streamlit
    st.write(resultados_playlist[['track_name','track_artist','URI']])
