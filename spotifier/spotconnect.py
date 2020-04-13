import spotipy
import spotipy.util as util

class Spotifier():
    def create_connection():
        """Connects to spotify using the apps credentials, to query the songs that should be added to the playlist
        """
        #TODO: connect to spotify via Client Credentials
        username = "tarrask"
        scope_read = 'user-library-read'
        token_read = util.prompt_for_user_token(username, scope_read, client_id='359147e53bf542949f7bd0edb39278e5',client_secret='23f089c667e14775b5fb7a2b5dd2aac4',redirect_uri='http://localhost/')

        return spotipy.Spotify(auth=token_read)

    def get_songs_before(self, band_name, concert_date):
        """Prompts spotify for an artist songs from before a date
        Needs name and date
        output is the most popular songs before concert date
        """

        connection = create_connection()

        result_search = connection.search(q=band_name + " year: 1900-" + str(concert_date), type="track")
        search_songs = []
        for track in result_search["tracks"]["items"]:
            if track["artists"][0]["name"] == band_name:
                search_songs.append(track)
        return search_songs

    def add_songs_to_playlist(self, playlist_name, spotifyURIs):
        """Get list of spotify URIs and a playlist name and creates a playlist that is added to a Spotify user's account
        """

        #TODO implement API authorization here. should use implicit grant
        username = "tarrask"
        scope_create_playlist = "playlist-modify-public"
        token_write_playlists = util.prompt_for_user_token(self.username, scope_create_playlist, client_id='359147e53bf542949f7bd0edb39278e5',client_secret='23f089c667e14775b5fb7a2b5dd2aac4',redirect_uri='http://localhost/')
        connection = spotipy.Spotify(auth=token_write_playlists)

        playlist = connection.user_playlist_create(self.username, playlist_name, public=True, description= "teste")

        connection.user_playlist_add_tracks(self.username, playlist["id"], spotifyURIs)
