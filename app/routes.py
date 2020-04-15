from flask import render_template, flash, redirect, url_for, get_flashed_messages, request, session
from app import app
from app.forms import PlaylistForm, SendForm
from spotifier.festivalprocessor import FestivalProcessor
from spotifier.spotconnect import Spotifier
import requests, json
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
    code_payload = {
        "grant_type": "authorization_code",
        "code": str(auth_token),
        "redirect_uri": sp.REDIRECT_URI,
        'client_id': sp.CLIENT_ID,
        'client_secret': sp.CLIENT_SECRET,
    }
    post_request = requests.post(sp.SPOTIFY_TOKEN_URL, data=code_payload)

    # Auth Step 5: Tokens are Returned to Application
    response_data = json.loads(post_request.text)
    access_token = response_data["access_token"]
    refresh_token = response_data["refresh_token"]
    token_type = response_data["token_type"]
    expires_in = response_data["expires_in"]

    # Auth Step 6: Use the access token to access Spotify API
    authorization_header = {"Authorization": "Bearer {}".format(access_token)}

    # Get profile data
    user_profile_api_endpoint = "{}/me".format(sp.SPOTIFY_API_URL)
    profile_response = requests.get(user_profile_api_endpoint, headers=authorization_header)
    profile_data = json.loads(profile_response.text)

    #sp.add_songs_to_playlist(authorization_header, profile_data["id"],session.get("playlist_name", None), session.get("songs", None))

    #TODO: should fix this line to add custom playlist name
    data = '{"name":"A New Playlist","public":false}'

    #creates playlist
    playlist_api_endpoint = "{}/playlists".format(profile_data["href"])
    playlists_add = requests.post(playlist_api_endpoint, headers=authorization_header, data=data)
    playlist_data = json.loads(playlists_add.text)

    # Get created playlist data
    playlist_id = playlist_data["id"]

    # Merges URIs into params format
    URIs = ",".join(session.get("songs", None))
    params = (('uris', f'{URIs}'),)

    songs_add = requests.post("https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id), headers=authorization_header, params=params)
    print(songs_add)
    songs_data = json.loads(songs_add.text)

    return render_template("spotify.html", sorted_array=songs_data)
