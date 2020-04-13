from spotifier import spotconnect

class FestivalProcessor:
    def __init__(self, festival, year, bands):
        sp = spotconnect.Spotifier()
        self.festival = festival
        self.year = year
        self.bands = bands

    def process_festival(self):
        band_count = 1
        for band in self.bands:
            print(str(band_count) + " bands to go...")
            print(band)
            process_band(band, self.year)
            band_count += 1

    def process_band(band, year):
        """Iterate through the best songs from band before specific date in Spotify's database
        Stores them in app's DB
        """
        print("Searching songs for band: " + band)
        songs = self.sp.get_songs_before(band, year) #gets songs from Spotify
        print("Found " + str(len(songs)) + " songs")

        for song in songs:
            print("Song found: " + song["name"])
            print("Storing song...")
            print(song["artists"][0]["name"], song["name"], song["album"]["name"], song["album"]["release_date"], song["popularity"], song["uri"], song["external_urls"]["spotify"])

            #TODO: store song into app DB
            storeSong(page, song["artists"][0]["name"], song["name"], song["album"]["name"], song["album"]["release_date"], song["popularity"], song["uri"], song["external_urls"]["spotify"])
            print("Done")

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
