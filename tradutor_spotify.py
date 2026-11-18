import json
import os
from datetime import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, render_template_string, request

ID = "51ebc5fc21fa4e359bebdd37175c9f13"
SEC = "8670dd178bb0463086bdbda323dc889f"
ARQUIVO_HISTORICO = "historico_diario_brunabmed.json"

MESES_PT = {
    "01": "Janeiro", "02": "Fevereiro", "03": "Marco", "04": "Abril",
    "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
    "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
}

app = Flask(__name__)

def get_spotify_client():
    host = request.host
    if "onrender.com" in host:
        redirect_uri = f"https://{host}/callback"
    else:
        redirect_uri = "http://127.0.0.1:5000/callback"
        
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=ID,
            client_secret=SEC,
            redirect_uri=redirect_uri,
            scope="user-read-playback-state user-read-currently-playing",
            cache_path=".cache",
            open_browser=False
        )
    )

MUSICAS_MANUAIS = {
    "pillowtalk": {
        "artista": "zayn",
        "letra_limpa": """Vem comigo
Vamos devagar e depois em ritmo acelerado
Entre a luz e a escuridão
Me abraça forte e depois com suavidade

Eu vejo a dor, vejo o prazer
Ninguém além de você, ninguém além de mim
Só nós dois, nossos corpos juntos
Eu amo te abraçar bem perto, hoje e sempre
Eu amo acordar ao seu lado

Então vamos incomodar os vizinhos
No lugar onde as lágrimas encontram espaço
Onde você deixa seus medos para trás
É, um comportamento inconsequente
Um lugar tão puro
Tão sujo e intenso
Na cama o dia inteiro, o dia inteiro, o dia inteiro
Transando e brigando
Esse é o nosso paraíso e a nossa zona de guerra""",
        "curiosidades_lista": [
            "✨ <b>O GRANDE LANÇAMENTO:</b> “PILLOWTALK” marcou o debut solo de Zayn Malik logo após o drama da sua saída do One Direction!",
            "🔥 <b>ALÉM DO PRAZER:</b> Zayn revelou que sexo é super natural e não deveria ser tabu."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — PILLOWTALK</b><br><br>Relações intensas, dualidades e regulação emocional.",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    }
}

last_saved_id = None

def salvar_no_historico(n, a, img_url):
    historico = []
    if os.path.exists(ARQUIVO_HISTORICO):
        try:
            with open(ARQUIVO_HISTORICO, "r", encoding="utf-8") as f:
                historico = json.load(f)
        except:
            pass

    mes_atual = MESES_PT.get(datetime.now().strftime("%m"), "Mes")
    encontrada = False
    for item in historico:
        if item["nome"].lower() == n.lower() and item["artista"].lower() == a.lower():
            item["vezes"] += 1
            item["mes"] = mes_atual
            encontrada = True
            break

    if not encontrada:
        historico.insert(0, {"nome": n, "artista": a, "img": img_url, "vezes": 1, "mes": mes_atual})

    try:
        with open(ARQUIVO_HISTORICO, "w", encoding="utf-8") as f:
            json.dump(historico[:10], f, ensure_ascii=False, indent=4)
    except:
        pass

def get_lyrics(t, a):
    try:
        url = f"https://lrclib.net/api/get?artist_name={a}&track_name={t}"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return r.json().get("plainLyrics")
    except:
        pass
    return None

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>~* xoxo My Music Diary *~</title>
    <link href="https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono:ital,wght@0,400;0,700;1,400&display=swap" rel="stylesheet">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #E3F0E8; font-family: 'Space Mono', monospace; color: #2c2c2c; padding: 50px; min-height: 100vh; }
        .container { max-width: 1200px; margin: 0 auto; text-align: center; }
        h1 { font-family: 'VT323', monospace; font-size: 70px; color: #B85D81; margin-bottom: 20px; }
        .box { background: #FFFDF9; border: 4px solid #2c2c2c; border-radius: 20px; padding: 30px; margin-top: 20px; font-size: 24px; }
        .btn { display: inline-block; background: #4A7C59; color: white; padding: 15px 30px; border-radius: 15px; text-decoration: none; font-weight: bold; margin-top: 20px; border: 3px solid #2c2c2c; }
    </style>
</head>
<body>
    <div class="container">
        <h1>~* xoxo My Music Diary *~</h1>
        <div class="box" id="content-box">
            Carregando o seu diário musical... 🎧✨
        </div>
        <div id="auth-box"></div>
    </div>
    <script>
        async function checkMusic() {
            try {
                let res = await fetch('/api/now-playing');
                let data = await res.json();
                let box = document.getElementById('content-box');
                let auth = document.getElementById('auth-box');

                if (data.auth_url) {
                    auth.innerHTML = `<a href="${data.auth_url}" class="btn">Conectar com o Spotify 🎧</a>`;
                    box.innerHTML = "Por favor, autorize o acesso à sua conta do Spotify para ver o diário.";
                } else if (data.playing) {
                    auth.innerHTML = "";
                    box.innerHTML = `<b>Tocando agora:</b> ${data.name} - ${data.artist}`;
                } else {
                    box.innerHTML = "Nenhuma música tocando no momento. Dê o play no Spotify!";
                }
            } catch(e) { console.log(e); }
        }
        setInterval(checkMusic, 2000);
        checkMusic();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    if code:
        sp_auth = get_spotify_client().auth_manager
        sp_auth.get_access_token(code)
    return "Autenticação realizada com sucesso! Pode fechar esta aba e voltar para o seu site. ✨"

@app.route("/api/now-playing")
def now_playing():
    global last_saved_id
    try:
        sp = get_spotify_client()
        token_info = sp.auth_manager.get_cached_token()
        if not token_info:
            auth_url = sp.auth_manager.get_authorize_url()
            return jsonify({"playing": False, "auth_url": auth_url})

        cur = sp.current_user_playing_track()
        if cur and cur.get("is_playing"):
            tr = cur["item"]
            tn = tr["name"]
            ar = tr["artists"][0]["name"]
            tid = tr["id"]
            img = tr["album"]["images"][0]["url"]
            p = cur.get("progress_ms", 0)
            dur = tr.get("duration_ms", 1)

            if tid != last_saved_id:
                last_saved_id = tid
                salvar_no_historico(tn, ar, img)

            return jsonify({
                "playing": True, "id": tid, "name": tn, "artist": ar,
                "image": img, "progress": p, "duration": dur
            })
    except Exception as e:
        print(f"Erro na API: {e}")
    return jsonify({"playing": False})

if __name__ == "__main__":
    app.run(port=5000)