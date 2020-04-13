from flask import render_template
from app import app
from app.forms import PlaylistForm

@app.route('/')
@app.route('/index')
def index():
    form = PlaylistForm()
    return render_template("index.html", title="Remember that night", form = form)
