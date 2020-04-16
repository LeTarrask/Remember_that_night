from flask import render_template, flash, redirect, url_for, get_flashed_messages, request, session
from app import app
from app.forms import PlaylistForm, SendForm
from spotifier.festivalprocessor import FestivalProcessor
from spotifier.spotconnect import Spotifier
import requests
from urllib.parse import quote


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PlaylistForm()
    if form.validate_on_submit():
        data_load = [form.festivalname.data, form.festivalyear.data, form.bands.data.splitlines()]
        flash(data_load)
        return redirect(url_for("playlist"))
    return render_template("index.html", title="Remember that night", form = form)

@app.route("/playlist", methods=['GET', 'POST'])
def playlist():
    form = SendForm()

    if request.method == "GET":
        data_load = get_flashed_messages()[0]

        processor = FestivalProcessor(data_load[0], data_load[1], data_load[2])

        playlist = processor.playlist_storage

        songs = playlist.get_songs()

        session["playlist_name"] = playlist.name
        songURIs = []
        for song in songs:
            songURIs.append(song.uri)
        session["songs"] = songURIs

        return render_template("playlist.html", title="Your Playlist", playlist=playlist, songs=songs, form=form)

    elif request.method == "POST":
        return redirect(url_for("authorize"))

@app.route("/authorize")
def authorize():
    # Auth Step 1: Authorization
    sp = Spotifier()
    url_args = "&".join(["{}={}".format(key, quote(val)) for key, val in sp.auth_query_parameters.items()])
    auth_url = "{}/?{}".format(sp.SPOTIFY_AUTH_URL, url_args)
    return redirect(auth_url)

@app.route("/callback/q")
def callback():
    sp = Spotifier()
    # Auth Step 4: Requests refresh and access tokens
    auth_token = request.args['code']

    #Send auth_token to Spotify Connect and process playlist and songs, returning the info that should be displayed on page
    songs_data = sp.add_songs_to_playlist(auth_token)

    return render_template("spotify.html", sorted_array=songs_data)
