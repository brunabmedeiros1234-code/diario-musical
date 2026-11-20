"""XOXO My Music Diary — revista musical digital (Flask)."""
import json
import os
import re
import secrets
import unicodedata
from pathlib import Path
from urllib.parse import quote

import requests
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth

ROOT = Path(__file__).parent
CATALOG = json.loads((ROOT / 'content.json').read_text(encoding='utf-8'))
app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY') or secrets.token_hex(32)
app.config.update(SESSION_COOKIE_HTTPONLY=True, SESSION_COOKIE_SAMESITE='Lax', SESSION_COOKIE_SECURE=os.getenv('RENDER') == 'true')
TOKENS = {}   # para um site pequeno; em produção de alta escala, usar Redis
SCOPES = 'user-read-currently-playing user-read-playback-state'


def normalized(value):
    value = unicodedata.normalize('NFKD', (value or '').casefold())
    return re.sub(r'[^a-z0-9]+', ' ', ''.join(c for c in value if not unicodedata.combining(c))).strip()


def find_entry(title, artist):
    title_norm, artist_norm = normalized(title), normalized(artist)
    for key, item in CATALOG.items():
        key_norm = normalized(key)
        track_match = title_norm == key_norm or title_norm.startswith(key_norm + ' ') or title_norm.startswith(key_norm + ' feat ')
        expected = normalized(item.get('artista', ''))
        artist_match = expected and (expected in artist_norm or artist_norm in expected)
        if track_match and artist_match:
            return key, item
    return None, None


def oauth():
    return SpotifyOAuth(client_id=os.getenv('SPOTIPY_CLIENT_ID'),
                        client_secret=os.getenv('SPOTIPY_CLIENT_SECRET'),
                        redirect_uri=os.getenv('SPOTIPY_REDIRECT_URI','http://127.0.0.1:5000/callback'),
                        scope=SCOPES, open_browser=False, cache_handler=None)


def configured():
    return bool(os.getenv('SPOTIPY_CLIENT_ID') and os.getenv('SPOTIPY_CLIENT_SECRET'))


def spotify_client():
    sid = session.get('sid')
    token = TOKENS.get(sid)
    if not token:
        return None
    try:
        manager = oauth()
        if manager.is_token_expired(token):
            token = manager.refresh_access_token(token['refresh_token'])
            TOKENS[sid] = token
        return Spotify(auth=token['access_token'], requests_timeout=8)
    except Exception:
        TOKENS.pop(sid, None)
        return None


def catalog_item(key):
    item = CATALOG[key]
    return {'key': key, 'title': key.title(), 'artist': item['artista'].title(),
            'summary': item['editorial']['summary'], 'mood': item['editorial']['mood'],
            'tags': item['editorial']['tags'], 'translation': item['letra_limpa'],
            'gossip': item['curiosidades_lista'], 'psychology': item['psicologia'],
            'quiz_topic': item['editorial']['test_topic'], 'spotify_search':
            'https://open.spotify.com/search/' + quote(key + ' ' + item['artista'])}


@app.route('/')
def home():
    return render_template('index.html', catalog=[catalog_item(k) for k in CATALOG],
                           configured=configured(), connected=bool(session.get('sid') in TOKENS))


@app.route('/login')
def login():
    if not configured():
        return redirect(url_for('home'))
    session.setdefault('sid', secrets.token_urlsafe(24))
    state = secrets.token_urlsafe(24)
    session['oauth_state'] = state
    return redirect(oauth().get_authorize_url(state=state))


@app.route('/callback')
def callback():
    if not configured():
        return redirect(url_for('home'))
    if request.args.get('state') != session.pop('oauth_state', None):
        return 'Sessão inválida. Tente conectar novamente.', 400
    if request.args.get('error'):
        return redirect(url_for('home'))
    code = request.args.get('code')
    if not code:
        return redirect(url_for('home'))
    try:
        TOKENS[session['sid']] = oauth().get_access_token(code, as_dict=True, check_cache=False)
    except Exception:
        return 'Não foi possível conectar ao Spotify. Verifique as credenciais e o endereço de retorno.', 400
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    sid = session.pop('sid', None)
    TOKENS.pop(sid, None)
    return redirect(url_for('home'))


@app.route('/api/catalog')
def api_catalog():
    return jsonify([catalog_item(k) for k in CATALOG])


@app.route('/api/now-playing')
def now_playing():
    client = spotify_client()
    if not client:
        return jsonify({'connected': False, 'playing': False})
    try:
        state = client.current_user_playing_track()
        if not state or not state.get('item'):
            return jsonify({'connected': True, 'playing': False})
        tr = state['item']
        title = tr.get('name','')
        artists = tr.get('artists') or []
        artist = artists[0].get('name','') if artists else ''
        key, _ = find_entry(title,artist)
        images = tr.get('album',{}).get('images') or []
        art = images[0].get('url') if images else None
        artist_art = None
        try:
            if artists and artists[0].get('id'):
                more = client.artist(artists[0]['id'])
                pictures = more.get('images') or []
                artist_art = pictures[0].get('url') if pictures else None
        except Exception:
            pass
        return jsonify({'connected': True, 'playing': bool(state.get('is_playing')),
                        'id': tr.get('id'), 'name':title,'artist':artist,
                        'album':tr.get('album',{}).get('name',''),
                        'image':art, 'artist_image':artist_art,
                        'url':tr.get('external_urls',{}).get('spotify',''),
                        'progress':state.get('progress_ms') or 0,
                        'duration':tr.get('duration_ms') or 0,
                        'key':key})
    except Exception:
        return jsonify({'connected': True, 'playing':False, 'error':'Não foi possível consultar o Spotify agora.'})


@app.route('/health')
def health():
    return jsonify({'status':'ok'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', '5000')), debug=os.getenv('FLASK_DEBUG') == '1')
