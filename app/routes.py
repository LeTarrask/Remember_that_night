from flask import render_template, flash, redirect
from app import app
from app.forms import PlaylistForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    form = PlaylistForm()
    if form.validate_on_submit():
        flash('Playlist requested for festival {}, bands={}'.format(
            form.festivalname.data, form.bands.data))
        return redirect('/playlist')
    return render_template("index.html", title="Remember that night", form = form)

@app.route("/playlist")
def playlist():
    return render_template("playlist.html", title="Your Playlist")
