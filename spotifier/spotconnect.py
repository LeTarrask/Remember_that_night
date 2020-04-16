import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests
import json
from flask import session
import os

class Spotifier():
    #  Client Keys
    CLIENT_ID = os.environ.get('CLIENT_ID', None)
    CLIENT_SECRET = os.environ.get('CLIENT_SECRET', None)

    # Spotify URLS
    SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
    SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"
    SPOTIFY_API_BASE_URL = "https://api.spotify.com"
    API_VERSION = "v1"
    SPOTIFY_API_URL = "{}/{}".format(SPOTIFY_API_BASE_URL, API_VERSION)

    # Server-side Parameters
    CLIENT_SIDE_URL = "http://127.0.0.1"
    PORT = 5000
    REDIRECT_URI = "{}:{}/callback/q".format(CLIENT_SIDE_URL, PORT)
    SCOPE = "playlist-modify-public playlist-modify-private"
    STATE = ""
    SHOW_DIALOG_bool = True
    SHOW_DIALOG_str = str(SHOW_DIALOG_bool).lower()

    auth_query_parameters = {
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPE,
        # "state": STATE,
        # "show_dialog": SHOW_DIALOG_str,
        "client_id": CLIENT_ID
    }

    def create_connection(self):
        """
        Connects to spotify using the apps credentials, to query the songs that should be added to the playlist
        """
        client_credentials_manager = SpotifyClientCredentials(self.CLIENT_ID, self.CLIENT_SECRET)

        return spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_songs_before(self, band_name, concert_date):
        """
        Prompts spotify for an artist songs from before a date
        Needs name and date
        output is the most popular songs before concert date
        """

        connection = self.create_connection()
        result_search = connection.search(q=band_name + " year: 1900-" + str(concert_date), type="track")
        search_songs = []
        #TODO: maybe this for loop is preventing some bands from being added
        for track in result_search["tracks"]["items"]:
            if track["artists"][0]["name"].lower() == band_name.lower():
                search_songs.append(track)
        return search_songs

    def add_songs_to_playlist(self, auth_token):
        """
        Get list of spotify URIs and a playlist name and creates a playlist that is added to a Spotify user's account
        """

        code_payload = {
            "grant_type": "authorization_code",
            "code": str(auth_token),
            "redirect_uri": self.REDIRECT_URI,
            'client_id': self.CLIENT_ID,
            'client_secret': self.CLIENT_SECRET,
        }
        post_request = requests.post(self.SPOTIFY_TOKEN_URL, data=code_payload)

        # Auth Step 5: Tokens are Returned to Application
        response_data = json.loads(post_request.text)
        access_token = response_data["access_token"]
        refresh_token = response_data["refresh_token"]
        token_type = response_data["token_type"]
        expires_in = response_data["expires_in"]

        # Auth Step 6: Use the access token to access Spotify API
        authorization_header = {"Authorization": "Bearer {}".format(access_token)}

        # Get profile data
        user_profile_api_endpoint = "{}/me".format(self.SPOTIFY_API_URL)
        profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
        profile_data = json.loads(profile_response.text)

        #TODO: should fix this line to add custom playlist name #session["playlist_name"]
        data = '{"name":"A New Playlist","public":false}'

        #creates playlist
        playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
        playlists_add = requests.post(playlist_api_endpoint, headers=authorization_header, data=data)
        playlist_data = json.loads(playlists_add.text)

        # Get created playlist data
        playlist_id = playlist_data["id"]

        # Merges URIs into params format
        URIs = ",".join(session.get("songs", None))
        params = (('uris', f'{URIs}'),)

        songs_add = requests.post("https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id), headers=authorization_header, params=params)
        print(songs_add)
        songs_data = json.loads(songs_add.text)

        return songs_data
