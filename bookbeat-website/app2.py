import streamlit as st
import os
import json
from datetime import datetime, timezone
import numpy as np
import pandas as pd

import sys
import webbrowser
sys.path.append("..")

from bookbeat.playlist_generation import playlist_popularity
from spotify_functions import login, get_access_token, create_playlist

'''
# BOOKBEAT'''
import pathlib
ruta_parent = pathlib.Path(__file__).parent.resolve()
st.markdown("""
## Select a book
""")
uri_tracks = []
# Ruta al archivo CSV
ruta_books =os.path.join(ruta_parent,"..", "raw_data", "books_sentiment.csv")
ruta_songs = os.path.join(ruta_parent,"..", "raw_data", "songs_sentiment.csv")

# Cargar datos desde el archivo CSV
data_book = pd.read_csv(ruta_books)
data_songs = pd.read_csv(ruta_songs)

if st.button("Login with Spotify"):
    auth_url = login()
    st.markdown(f'<a href="{auth_url}" target="_blank">Click here to login with Spotify</a>', unsafe_allow_html=True)
    st.stop()


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


@st.cache_resource
def generar_tokens():
    if "code" in st.experimental_get_query_params():
        code = st.experimental_get_query_params()["code"]
        print("1")
        access_token, refresh_token, expires_at = obtener_tokens_json()
        print(access_token)

        if expires_at is None or datetime.now().timestamp() > datetime.fromisoformat(expires_at).replace(tzinfo=timezone.utc).timestamp():
            # El token ha expirado o es nulo, obtén uno nuevo
            new_access_token, new_refresh_token, new_expires_at = get_access_token(code)
            print("2")
            print(new_access_token)

            if new_access_token is not None and new_refresh_token is not None and new_expires_at is not None:
                # Solo guarda los nuevos tokens si la obtención fue exitosa
                guardar_tokens_json(new_access_token, new_refresh_token, new_expires_at)
                access_token, refresh_token, expires_at = new_access_token, new_refresh_token, new_expires_at
                print("3")
                print(access_token)
                return access_token, refresh_token, expires_at

            else:
                st.error("Error al obtener nuevos tokens. Revise el flujo de autorización.")
                return None, None, None

@st.cache_resource
def generar_playlist(title, data_book, data_songs):
    libro = title[0]
    resultados_playlist = playlist_popularity(libro, data_book, data_songs)
    uri_tracks = resultados_playlist['URI'].tolist()
    guardar_tracks_json(uri_tracks)
    return resultados_playlist[['track_name', 'track_artist', 'URI']]

# Llamar a la función de generación de playlist
if st.button("Generar Playlist"):
    playlist_result = generar_playlist(title, data_book, data_songs)
    st.session_state.playlist_result = playlist_result

# Mostrar la tabla si existe en st.session_state
if "playlist_result" in st.session_state:
    st.write(st.session_state.playlist_result)


if st.button("Crear Playlist en Spotify"):
        access_token, refresh_token, expires_at = generar_tokens()
        print("4")
        print(access_token)
        print(expires_at)
        uri_tracks = obtener_tracks_json()
        book_title = title[0]
        playlist_result = create_playlist(access_token, expires_at, uri_tracks, book_title)
        if "error" in playlist_result:
            st.error(f"Error: {playlist_result['error']}")
        else:
            st.success("¡Playlist creada exitosamente!")
