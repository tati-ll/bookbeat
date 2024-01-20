import streamlit as st
import os

import numpy as np
import pandas as pd

import json
from datetime import datetime, timezone
import numpy as np
import pandas as pd
import time
import sys
import webbrowser
sys.path.append("..")

from isbn_number import book_isbn
from api_google_book import obtener_descripcion_isbn
from data_cleaning import cleaning_books
from playlist_generation import obtain_compound, playlist_popularity
from spotify_functions import login, get_access_token, create_playlist

# -- Set page config
apptitle = 'BookBeat'

st.set_page_config(page_title=apptitle, page_icon=":book:")

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

AUTH_STATE_FILE = "auth_state.json"

# Comprobar si el estado de autenticación ya existe en el archivo
try:
    with open(AUTH_STATE_FILE, "r") as file:
        auth_state = json.load(file)
except FileNotFoundError:
    # Si el archivo no existe, inicializar el estado de autenticación
    auth_state = {"logged_in": False, "login_time": 0}

# Obtener el tiempo actual
current_time = time.time()

# Verificar si ya está autenticado y si ha pasado más de 9 minutos
if auth_state["logged_in"] and (current_time - auth_state["login_time"]) < (10 * 60):
    # Si ya está autenticado y no ha pasado el tiempo límite, mostrar un mensaje
    st.write("¡Logueado exitosamente en Spotify!")

    # Restar el tiempo que ha pasado desde el último login
    time_remaining = (9 * 60) - (current_time - auth_state["login_time"])

    if st.button("Volver a Logear"):
        # Volver a logear solo si se presiona el botón dentro del tiempo límite
        auth_url = login()
        st.experimental_set_query_params(auth_url=auth_url)
        webbrowser.open(auth_url, new=2)
        auth_state["login_time"] = time.time()
        with open(AUTH_STATE_FILE, "w") as file:
            json.dump(auth_state, file)
        st.stop()
else:
    # Si no está autenticado o ha pasado el tiempo límite, mostrar el botón de log in
    if st.button("Login with Spotify"):
        auth_url = login()
        st.experimental_set_query_params(auth_url=auth_url)
        webbrowser.open(auth_url, new=2)
        auth_state["logged_in"] = True
        auth_state["login_time"] = time.time()
        with open(AUTH_STATE_FILE, "w") as file:
            json.dump(auth_state, file)
        st.stop()
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

        access_token, refresh_token, expires_at = obtener_tokens_json()
        print(f"generar tokens: {access_token}")

        if expires_at is None or datetime.now().timestamp() > datetime.fromisoformat(expires_at).replace(tzinfo=timezone.utc).timestamp():
            # El token ha expirado o es nulo, obtén uno nuevo
            new_access_token, new_refresh_token, new_expires_at = get_access_token(code)
            print(f"se expiro, aqui el nuevo: {new_access_token}")

            if new_access_token is not None and new_refresh_token is not None and new_expires_at is not None:
                # Solo guarda los nuevos tokens si la obtención fue exitosa
                guardar_tokens_json(new_access_token, new_refresh_token, new_expires_at)
                access_token, refresh_token, expires_at = new_access_token, new_refresh_token, new_expires_at
                return access_token, refresh_token, expires_at
            else:
                st.error("Error al obtener nuevos tokens. Revise el flujo de autorización.")
                return None, None, None
        else:
            return access_token, refresh_token, expires_at


@st.cache_resource
def generar_playlist(title, book_sentiment, data_songs, n_tracks):
    libro = title[0]
    resultados_playlist = playlist_popularity(book_sentiment, data_songs, n_tracks)
    uri_tracks = resultados_playlist['URI'].tolist()
    guardar_tracks_json(uri_tracks)
    return resultados_playlist[['track_name', 'track_artist']]

# Cargar datos desde el archivo CSV
data_book, data_songs = carga_dataset()

# Crear un menú desplegable con la lista de libros
# Filtrar títulos únicos
unique_title = data_book['Title'].unique()
libro_seleccionado = st.selectbox("**Selecciona el título de tu libro**", unique_title, index=None, key='libro', placeholder="Choose a book")

if libro_seleccionado:
    unique_authors = data_book[data_book['Title'] == libro_seleccionado]['Author'].unique()
    selected_author = st.selectbox("**Selecciona el autor de tu libro**", unique_authors, index=None, placeholder="Choose the author")

if libro_seleccionado and selected_author:
    st.write(f"Libro seleccionado: **{libro_seleccionado}** del autor **{selected_author}**")
    # Título de la lista desplegable
    st.write("## Elige el número de canciones para tu playlist")

    # Opciones para la lista desplegable
    opciones_n_tracks = [20, 30, 40, 50]

    # Lista desplegable para elegir el número de canciones
    n_tracks = st.selectbox("Número de canciones:", opciones_n_tracks)

    # Mostrar el número de canciones seleccionado
    st.write(f"Has seleccionado {n_tracks} canciones para tu playlist.")
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
            playlist_result = generar_playlist(libro_seleccionado, book_sentiment, data_songs, n_tracks)
            playlist_result.to_csv("playlist_result.csv", index=False)
            st.session_state.playlist_result = playlist_result



# Mostrar la tabla si existe en st.session_state
if "playlist_result" in st.session_state:
    playlist_result = pd.read_csv("playlist_result.csv")
    columnas_mostrar = ['track_name', 'track_artist']
    nuevos_nombres = ['Título de la Canción', 'Artista']

    # Crea un nuevo DataFrame con las columnas seleccionadas y los nuevos nombres
    playlist_mostrada = playlist_result[columnas_mostrar].rename(columns=dict(zip(columnas_mostrar, nuevos_nombres)))
    st.write(playlist_mostrada)
    if st.button("Crear Playlist en Spotify"):
            access_token, refresh_token, expires_at = generar_tokens()
            uri_tracks = obtener_tracks_json()
            print(f"titul: {libro_seleccionado}, uri_tracks: {uri_tracks}, access_token: {access_token}")
            api_result = create_playlist(access_token, expires_at, uri_tracks, libro_seleccionado)
            if "error" in api_result:
                st.error(f"Error: {api_result['error']}")
            else:
                st.success("¡Playlist creada exitosamente!")
                playlist_link = f"[Visita la playlist aquí]({api_result['external_urls']['spotify']})"

                # Mostrar el enlace utilizando st.markdown
                st.markdown(playlist_link)
