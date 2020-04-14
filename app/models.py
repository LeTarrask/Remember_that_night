from app import db



class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), index=True, unique=False)
    year = db.Column(db.Integer(), index=True, unique=False)
    bands = db.Column(db.String(200), index=True, unique=False) #TODO: this should be an array of bands, not a string
    songs = db.relationship("Song", backref="list", lazy="dynamic")

    def __repr__(self):
        return '<Playlist {}>'.format(self.name)

    def get_songs(self):
        songs = Song.query.filter_by(list=self)
        for song in songs:
            print(song)
        return songs

class Song(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    artist_name = db.Column(db.String(120), index=True, unique=False)
    song_name = db.Column(db.String(120), index=True, unique=False)
    album_name = db.Column(db.String(120), index=True, unique=False)
    release_date = db.Column(db.String(64), index=True, unique=False)
    popularity = db.Column(db.String(64), index=True, unique=False)
    uri = db.Column(db.String(120), index=True, unique=False)
    external_urls = db.Column(db.String(200), index=True, unique=False)
    playlist = db.Column(db.Integer, db.ForeignKey("playlist.id"))

    def __repr__(self):
        return '<Song {}>'.format(self.song_name)
