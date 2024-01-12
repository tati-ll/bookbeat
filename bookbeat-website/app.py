import streamlit as st
import os
import json
from datetime import datetime
import numpy as np
import pandas as pd

import sys
import webbrowser
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
import json

def guardar_tokens_json(access_token, refresh_token, expires_at):
    # Convertir expires_at a una cadena ISO 8601 para hacerla serializable
    expires_at_str = expires_at.isoformat()

    # Crear un diccionario con los tres tokens
    tokens = {"access_token": access_token, "refresh_token": refresh_token, "expires_at": expires_at_str}

    # Guardar en un archivo JSON
    with open('tokens.json', 'w') as file:
        json.dump(tokens, file)

def obtener_tokens_json():
    try:
        # Intentar cargar desde el archivo JSON
        with open('tokens.json', 'r') as file:
            tokens = json.load(file)
            return tokens["access_token"], tokens["refresh_token"], tokens["expires_at"]
    except (FileNotFoundError, json.JSONDecodeError):
        # Manejar errores si el archivo no existe o no es un JSON válido
        return None, None, None

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
    webbrowser.open(auth_url, new=2)
    st.stop()


if "code" in st.experimental_get_query_params():
    code = st.experimental_get_query_params()["code"]
    access_token, refresh_token, expires_at = obtener_tokens_json()

    if access_token is None or refresh_token is None or expires_at is None:
        # Si no tenemos tokens, obtenerlos
        access_token, refresh_token, expires_at = get_access_token(code)
        guardar_tokens_json(access_token, refresh_token, expires_at)
    if st.button("Crear Playlist en Spotify"):
        access_token, refresh_token, expires_at = obtener_tokens_json()
        uri_tracks = obtener_tracks_json()
        playlist_result = create_playlist(access_token, expires_at, uri_tracks)
        if "error" in playlist_result:
            st.error(f"Error: {playlist_result['error']}")
        else:
            st.success("¡Playlist creada exitosamente!")
