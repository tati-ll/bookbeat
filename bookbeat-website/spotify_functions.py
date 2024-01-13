import requests
import urllib.parse
from dotenv import load_dotenv
import os
from datetime import datetime, timedelta

load_dotenv()
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
CLIENT_ID = 'be74c9aaf5c448c08b74412b92eb7ca3'
REDIRECT_URI = "http://localhost:8501"
#USER_ID = "tjllana"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"


def login():
    scope = "user-read-private user-read-email playlist-modify-public playlist-modify-private"
    params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": scope,
        "show_dialog": True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return auth_url

def get_access_token(code):
    req_body = {
        "code": code,
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=req_body)
    if response.status_code == 200:
        token_info = response.json()
        access_token = token_info.get("access_token")
        refresh_token = token_info.get("refresh_token")
        expires_in = token_info.get("expires_in")

        if access_token and refresh_token and expires_in:
            expires_at = datetime.now() + timedelta(seconds=expires_in)
            return access_token, refresh_token, expires_at

    # Manejar errores aquí si la solicitud falla o los datos son incorrectos
    return None, None, None

def refresh_access_token(refresh_token):

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    response = requests.post(TOKEN_URL, data=data)
    token_info = response.json()
    new_access_token = token_info.get("access_token")

    return new_access_token


# Función para verificar si el token está vencido
def token_expired(expires_at):
    current_time = datetime.now()
    expiration_time = datetime.fromtimestamp(expires_at)
    return current_time > expiration_time

def get_user_id(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://api.spotify.com/v1/me", headers=headers)
    return response.json()["id"]

def create_playlist(access_token, expires_at, tracks_uris, book_title):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    #access_token = refresh_access_token("tu_refresh_token")

    # Datos para la nueva playlist (cambia estos valores según tu lógica)
    playlist_data = {
        "name": f"{book_title} playlist",
        "description": f"Una playlist creada para leer {book_title}",
        "public": True
    }

    USER_ID = get_user_id(access_token)
    # URL para crear la playlist y agregar canciones en la API de Spotify
    url = f"{API_BASE_URL}users/{USER_ID}/playlists"

    # Crear la playlist y agregar canciones en una sola solicitud
    response = requests.post(url, headers=headers, json={**playlist_data})
    print(response.status_code)
    if response.status_code == 201:  # 201: Created
        new_playlist = response.json()
        playlist_id = new_playlist['id']
        url_add = f"{API_BASE_URL}playlists/{playlist_id}/tracks"
        response_add = requests.post(url_add, headers=headers, json={"uris": tracks_uris})

        if response_add.status_code == 201:
            return new_playlist
        else:
            return {"error": "No se pudo agregar canciones"}
    else:
        return {"error": "No se pudo crear la playlist"}
