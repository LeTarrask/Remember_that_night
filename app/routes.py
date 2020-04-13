from flask import render_template, flash, redirect, url_for, get_flashed_messages
from app import app
from app.forms import PlaylistForm
from spotifier.festivalprocessor import FestivalProcessor

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = PlaylistForm()
    if form.validate_on_submit():
        data_load = [form.festivalname.data, form.festivalyear.data, form.bands.data.splitlines()]
        flash(data_load)
        return redirect(url_for("playlist"))
    return render_template("index.html", title="Remember that night", form = form)

@app.route("/playlist")
def playlist():
    data_load = get_flashed_messages()[0]

    processor = FestivalProcessor(data_load[0], data_load[1], data_load[2])

    return render_template("playlist.html", title="Your Playlist", playlist=processor)
