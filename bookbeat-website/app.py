import streamlit as st
import os
import json

import numpy as np
import pandas as pd

import sys
sys.path.append("..")

from bookbeat.playlist_generation import playlist_popularity
from spotify_functions import login, get_access_token, create_playlist

'''
# BOOKBEAT'''

st.markdown("""
## Select a book
""")
uri_tracks = []
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

def guardar_tracks_json(tracks):
    with open('tracks.json', 'w') as file:
        json.dump(tracks, file)

# Recuperar desde un archivo JSON
def obtener_tracks_json():
    with open('tracks.json', 'r') as file:
        return json.load(file)

# Llamar a la función de generación de playlist
if st.button("Generar Playlist"):
    # Resultados de la función basada en el título del libro
    libro = title[0]
    resultados_playlist = playlist_popularity(libro,data_book, data_songs)

    uri_tracks = resultados_playlist['URI'].tolist()
    print(uri_tracks)
    guardar_tracks_json(uri_tracks)

    # Mostrar resultados en Streamlit
    st.write(resultados_playlist[['track_name','track_artist','URI']])

if st.button("Login with Spotify"):
    auth_url = login()
    st.experimental_set_query_params(auth_url=auth_url)

if "auth_url" in st.experimental_get_query_params():
    auth_url = st.experimental_get_query_params()["auth_url"]
    st.write(f"You are being redirected to Spotify authorization: {auth_url}")


if "code" in st.experimental_get_query_params():
    code = st.experimental_get_query_params()["code"]
    access_token, refresh_token, expires_at = get_access_token(code)
    st.write("Se detectó el código de autorización de Spotify")

    if access_token:
        uri_tracks = obtener_tracks_json()
        if uri_tracks:  # Verificar si uri_tracks existe y tiene contenido
            st.write("hay uri_Tracks")
            if st.button("botono"):
                st.write("Botón presionado")
            else:
                st.write("Botón no presionado")

            if st.button("Crear Playlist"):
                st.write("llamando")
                playlist_result = create_playlist(access_token, uri_tracks)
                st.write("holaaa")
                if "error" in playlist_result:
                    st.error(f"Error: {playlist_result['error']}")
                else:
                    st.success("¡Playlist creada exitosamente!")
        else:
            st.write("La variable uri_tracks no está definida o está vacía")
