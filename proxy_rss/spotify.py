import flask
import os
import spotipy
from flask import render_template
from spotipy.oauth2 import SpotifyClientCredentials

from proxy_rss import settings


blueprint = flask.Blueprint(
    'spotify', __name__,
    template_folder=os.path.join(
        os.path.dirname(__file__),
        'templates/spotify',
    ),
)


def get_spotify():
    auth = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET,
    )
    return spotipy.Spotify(client_credentials_manager=auth)


@blueprint.route('/artist_albums/<artist_id>')
def artist_albums(artist_id):
    api = get_spotify()

    albums = []
    res = api.artist_albums(artist_id)
    while res and res['items']:
        albums.extend(res['items'])
        res = api.next(res)

    return(
        render_template(
            'albums.rss',
            albums=albums,
        ),
        {'Content-Type': 'application/rss+xml'},
    )


@blueprint.route('/artist_tracks/<artist_id>')
def artist_tracks(artist_id):
    api = get_spotify()

    albums = []
    res = api.artist_albums(artist_id)
    while res and res['items']:
        albums.extend(res['items'])
        res = api.next(res)

    tracks = []
    for album in albums:
        res = api.album_tracks(album['id'])
        while res and res['items']:
            for track in res['items']:
                tracks.append(dict(track, album=album))
            res = api.next(res)

    return(
        render_template(
            'tracks.rss',
            tracks=tracks,
        ),
        {'Content-Type': 'application/rss+xml'},
    )
