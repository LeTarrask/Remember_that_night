import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import requests

class Spotifier():
    #  Client Keys
    CLIENT_ID = "359147e53bf542949f7bd0edb39278e5"
    CLIENT_SECRET = "23f089c667e14775b5fb7a2b5dd2aac4"

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

    def add_songs_to_playlist(self, user, access_token, playlist_name, spotifyURIs):
        """
        Get list of spotify URIs and a playlist name and creates a playlist that is added to a Spotify user's account
        """

        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        #TODO bug is not reading festival name here
        data = '{"name":"A New Playlist","public":false}'

        response = requests.post(f'https://api.spotify.com/v1/users/{user}/playlists', headers=headers, data=data)

        print(response.text)

        URIs = ", ".join(spotifyURIs)
        params = (('uris', f'{URIs}'),)

        response = requests.post('https://api.spotify.com/v1/playlists/7oi0w0SLbJ4YyjrOxhZbUv/tracks', headers=headers, params=params)
        print(response.text)
