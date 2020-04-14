from spotifier import spotconnect
from app.models import Playlist, Song
from app import db

class FestivalProcessor:
    def __init__(self, festival, year, bands):
        self.festival = festival
        self.year = year
        self.bands = bands

        self.playlist_storage = Playlist(name=self.festival, year=int(year), bands=", ".join(self.bands))
        db.session.add(self.playlist_storage)

        for band in self.bands:
            self.process_band(band, year)

        db.session.commit()

    def process_band(self, band, year):
        """
        Iterate through the best songs from band before specific date in Spotify's database
        Stores them in app's DB
        """
        #Searching songs for band
        sp = spotconnect.Spotifier()
        songs = sp.get_songs_before(band, year) #gets songs from Spotify

        for song in songs:
            song_storage = Song(artist_name = song["artists"][0]["name"],
            song_name = song["name"], album_name = song["album"]["name"],
            release_date = song["album"]["release_date"], popularity = song["popularity"], uri = song["uri"],
            external_urls = song["external_urls"]["spotify"], list=self.playlist_storage)
            db.session.add(song_storage)

    #TODO: get the URI source to add to this function
    def add_found_songs_to_playlist(song_list):
        """Get the list of songs from the playlist from database and sends to spotconnect to save in spotify
        """
        spotifyURIs = song_list
        request_URIs = []
        request_batch = []
        for x in range(len(spotifyURIs)):
            request_batch.append(spotifyURIs[x])
            if len(request_batch) % 100 == 0 or x == len(spotifyURIs)-1:
                request_URIs.append(request_batch)
                request_batch = []
                print("reseting batch %i" %x)
        for batch in request_URIs:
            # using remove() to  perform removal
            while("" in batch):
                batch.remove("")
            print("Batch size = %i" %len(batch))
            sp.add_songs_to_playlist(self.festival, batch)
            sleep(100)
