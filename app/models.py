from app import db

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=False)
    year = db.Column(db.Integer(), index=True, unique=False)
    bands = db.Column(db.String(200), index=True, unique=False) #TODO: this should be an array of bands, not a string

    def __repr__(self):
        return '<Playlist {}>'.format(self.name)
