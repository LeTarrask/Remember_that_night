from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import PlaylistForm
from spotifier.festivalprocessor import FestivalProcessor

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PlaylistForm()
    if form.validate_on_submit():
        data_load = [form.festivalname.data, form.festivalyear.data, form.bands.data.splitlines()]
        #TODO: how to pass data load to the following page????
        return redirect(url_for("playlist"))
    return render_template("index.html", title="Remember that night", form = form)

@app.route("/playlist")
def playlist():
    processor = FestivalProcessor(data_load)
    playlist = processor.playlist_storage
    return render_template("playlist.html", title="Your Playlist")
