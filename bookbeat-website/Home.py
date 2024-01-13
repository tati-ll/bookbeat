import streamlit as st
import os

import numpy as np
import pandas as pd

import sys
sys.path.append("..")

from bookbeat.isbn_number import book_isbn
from bookbeat.api_google_book import obtener_descripcion_isbn
from bookbeat.data_cleaning import cleaning_books
from bookbeat.playlist_generation import obtain_compound, playlist_popularity

# -- Set page config
apptitle = 'BookBeat'

st.set_page_config(page_title=apptitle, page_icon=":book:")

@st.cache_data
def carga_dataset():
    # Ruta al archivo CSV
    ruta_books = "../raw_data/isbn_titulo_autor.csv"
    ruta_songs = "../raw_data/songs_sentiment.csv"

    # Cargar datos desde el archivo CSV
    data_book = pd.read_csv(ruta_books)
    data_songs = pd.read_csv(ruta_songs)

    return data_book, data_songs

st.image("../raw_data/BookBeat_3.png")

# Cargar datos desde el archivo CSV
data_book, data_songs = carga_dataset()

# Crear un menú desplegable con la lista de libros
# Filtrar títulos únicos
unique_title = data_book['Title'].unique()
libro_seleccionado = st.selectbox("**Selecciona el título de tu libro**", unique_title, index=None, key='libro', placeholder="Choose an option")

if libro_seleccionado:
    unique_authors = data_book[data_book['Title'] == libro_seleccionado]['Author'].unique()
    selected_author = st.selectbox("**Selecciona el autor de tu libro**", unique_authors, index=None)

if libro_seleccionado and selected_author:
    st.write(f"Libro seleccionado: **{libro_seleccionado}** del autor **{selected_author}**")
    button = st.button(":gray[Generar Playlist]")

    # Cálculo del sentimiento
    if button:
        # Resultados de la función basada en el título del libro
        isbn = book_isbn(libro_seleccionado,selected_author,data_book)
        sentence = obtener_descripcion_isbn(isbn)
        if sentence == 'No se encontro libro':
            st.write('Select another book')

        else:
            clean_sentence = cleaning_books(sentence)
            book_sentiment = obtain_compound(clean_sentence)
            resultados_playlist = playlist_popularity(book_sentiment, data_songs)

            uri= resultados_playlist['URI'].tolist()

            # Mostrar resultados en Streamlit
            st.write(resultados_playlist[['track_name','track_artist']])
