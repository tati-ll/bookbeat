from flask import Flask, redirect, request, session, make_response
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import requests
import random

# Crear la aplicación Flask
app = Flask(__name__)

# Configurar las credenciales y el alcance de la API de Spotify
app.config["CLIENT_ID"] = 'be74c9aaf5c448c08b74412b92eb7ca3'
app.config["CLIENT_SECRET"] = '4fb7c919ee5146559142ba4f8f374f5e'
app.config["REDIRECT_URI"] = "http://localhost:8000/callback/"
app.config["SCOPE"] = "playlist-modify-public"

# Crear una clave aleatoria para el estado de la sesión
def create_state_key(length):
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(letters) for i in range(length))

# Solicitar la autorización del usuario
@app.route("/authorize")
def authorize():
    client_id = app.config["CLIENT_ID"]
    redirect_uri = app.config["REDIRECT_URI"]
    scope = app.config["SCOPE"]
    state_key = create_state_key(15)
    session["state_key"] = state_key
    authorize_url = "https://accounts.spotify.com/en/authorize?"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "state": state_key,
    }
    query_params = requests.utils.urlencode(params)
    response = make_response(redirect(authorize_url + query_params))
    return response

# Obtener el token de acceso
@app.route("/callback")
def callback():
    code = request.args.get("code")
    state = request.args.get("state")
    stored_state = session.get("state_key")
    if state is None or state != stored_state:
        return redirect("/error")
    else:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=app.config["CLIENT_ID"], client_secret=app.config["CLIENT_SECRET"], redirect_uri=app.config["REDIRECT_URI"], scope=app.config["SCOPE"]))
        token_info = sp.oauth2.get_access_token(code)
        access_token = token_info["access_token"]
        session["access_token"] = access_token
        return redirect("/create_playlist")

# Crear la playlist
@app.route("/create_playlist")
def create_playlist():
    access_token = session.get("access_token")
    if access_token is None:
        return redirect("/authorize")
    else:
        sp = spotipy.Spotify(auth=access_token)
        user_id = sp.current_user()["id"]
        session["user_id"] = user_id
        playlist_name = "Mi playlist genial"
        playlist_description = "Una playlist creada con la API de Spotify y Flask"
        playlist = sp.user_playlist_create(user_id, playlist_name, public=True, description=playlist_description)
        playlist_id = playlist["id"]
        session["playlist_id"] = playlist_id
        return redirect("/add_tracks")

# Añadir canciones a la playlist
@app.route("/add_tracks")
def add_tracks():
    access_token = session.get("access_token")
    if access_token is None:
        return redirect("/authorize")
    else:
        sp = spotipy.Spotify(auth=access_token)
        user_id = session.get("user_id")
        playlist_id = session.get("playlist_id")
        playlist_name = "Mi playlist genial"
        tracks = ["spotify:track:6rqhFgbbKwnb9MLmUQDhG6", "spotify:track:0eGsygTp906u18L0Oimnem", "spotify:track:7GhIk7Il098yCjg4BQjzvb"]
        sp.user_playlist_add_tracks(user_id, playlist_id, tracks)
        return f"Playlist {playlist_name} creada con éxito"
