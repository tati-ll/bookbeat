import requests
import urllib.parse

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session

app = Flask(__name__)
app.secret_key = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
CLIENT_ID = 'be74c9aaf5c448c08b74412b92eb7ca3'
CLIENT_SECRET = '4fb7c919ee5146559142ba4f8f374f5e'
REDIRECT_URI = "http://localhost:5000/callback"
USER_ID = "macamenarez"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

@app.route("/")
def index():
    return "Welcome to my Spotify app <a href='/login'>Login with Spotify</a>"

@app.route("/login")
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




    return redirect(auth_url)

@app.route("/callback")
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})
    if "code" in request.args:
        req_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "client_id": CLIENT_ID,
            "redirect_uri": REDIRECT_URI,
            "client_secret": CLIENT_SECRET

        }
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()

        session["access_token"] =  token_info["access_token"]
        session["refresh_token"] =  token_info["refresh_token"]
        session["expires_at"] =  datetime.now().timestamp() + token_info["expires_in"]

        return redirect("/create_playlist_page")

@app.route("/create_playlist_page")
def create_playlist_page():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Crear Playlist</title>
    </head>
    <body>
        <button id="createPlaylistBtn">Crear Playlist</button>

        <script>
            document.getElementById("createPlaylistBtn").addEventListener("click", function() {
                fetch("/create_playlist", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({})
                })
                .then(response => response.json())
                .then(data => {
                    if (data.message) {
                        alert(data.message);
                    } else if (data.error) {
                        alert(data.error);
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                    alert("Error al conectar con el servidor");
                });
            });
        </script>
    </body>
    </html>
    """

@app.route("/create_playlist", methods=['POST'])
def create_playlist():
    if "access_token" not in session:
        return redirect("/login")
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")

    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json"
    }

    # Datos para la nueva playlist (puedes cambiar estos valores según tu lógica)
    playlist_data = {
        "name": "Mi Nueva Playlist",
        "description": "Una playlist creada desde Flask",
        "public": True
    }

    # Lista de URI de canciones que quieres agregar a la playlist
    tracks_uris = [
        "spotify:track:6rqhFgbbKwnb9MLmUQDhG6",
        "spotify:track:0eGsygTp906u18L0Oimnem",
        "spotify:track:7GhIk7Il098yCjg4BQjzvb"
    ]

    # URL para crear una playlist y agregar canciones en la API de Spotify
    url = f"{API_BASE_URL}users/{USER_ID}/playlists"

    # Crear la playlist y agregar canciones en una sola solicitud
    response = requests.post(url, headers=headers, json={
        **playlist_data})


    if response.status_code == 201:  # 201: Created
        new_playlist = response.json()
        playlist_id = new_playlist['id']

        url_add = f"{API_BASE_URL}playlists/{playlist_id}/tracks"
        response_add = requests.post(url_add, headers=headers, json={"uris": tracks_uris})
        if response_add.status_code == 201:
            return jsonify(new_playlist)
        else:
            return jsonify({"error": "No se pudo agregar canciones"})
    else:
        return jsonify({"error": "No se pudo crear la playlist o agregar canciones"})



@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')
    if datetime.now().timestamp() > session["expires_at"]:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session["access_token"] = new_token_info["access_token"]
        session["expires_at"] = datetime.now().timestamp() + new_token_info["expires_in"]

        return redirect("/playlists")

if __name__ == "__main__":
    app.run(host= "0.0.0.0", debug=True)
