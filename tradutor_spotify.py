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
Esse é o nosso paraíso e a nossa zona de guerra

Conversas no travesseiro
Minha inimiga, minha aliada
Prisioneiros e depois somos livres
É uma linha muito tênue

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
            "✨ <b>O GRANDE LANÇAMENTO:</b> “PILLOWTALK” marcou o debut solo de Zayn Malik logo após o drama da sua saída do One Direction! A música veio sem filtro, misturando total o lado físico e emocional do sexo.",
            "🔥 <b>ALÉM DO PRAZER:</b> Zayn revelou que sexo é super natural e não deveria ser tabu. Ele define o quarto do casal como “nosso paraíso e nossa zona de guerra”, misturando dor, pureza e intensidade.",
            "💖 <b>MAIS QUE UMA NOITE:</b> Ele deixa bem claro que não quer só curtição passageira. Quando canta sobre acordar juntinho, o boy mostra que quer toda a intimidade que vem depois!",
            "💋 <b>O SIGNIFICADO DE PILLOW TALK:</b> A famosa 'conversa no travesseiro' que deveria ser sobre segredos e fofocas românticas vira pura eletricidade física e catarse emocional. É o momento de baixar a guarda e confiar na pessoa! 🖤"
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — PILLOWTALK</b><br><br>Relações intensas, dualidades e regulação emocional sob a ótica da psicologia analítica e da teoria do apego.",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    },
    "it's you": {
        "artista": "zayn",
        "letra_limpa": """Ela tem, ela tem, ela tem
Os motivos dela para falar comigo
Ela não, ela não, ela não
Se importa nem um pouco com o que eu preciso

E eu não consigo te dizer o porquê, porque minha cabeça não consegue entender
Me conte suas mentiras, porque eu simplesmente não consigo encarar a verdade

É você, é você, é você
É você, é você, é você""",
        "curiosidades_lista": [
            "💔 <b>DR DRAMA NA ÁREA:</b> Zayn percebeu que a cremosa só age por interesse próprio e tem planos próprios. Ele sabe que está rolando mentira purinha."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL:</b> Assimetria, negação e conflito entre razão e emoção.",
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
        body {
            background-color: #E3F0E8;
            background-image: radial-gradient(#b8d8c5 2.5px, transparent 2.5px);
            background-size: 32px 32px;
            font-family: 'Space Mono', monospace;
            color: #2c2c2c;
            padding: 50px;
            min-height: 100vh;
        }
        .container { max-width: 2050px; margin: 0 auto; }
        .site-header { text-align: center; margin-bottom: 35px; }
        .site-header h1 { font-family: 'VT323', monospace; font-size: 90px; color: #B85D81; text-shadow: 4px 4px 0px #FFFDF9; letter-spacing: 6px; }
        .marquee-bar { background: #F9E4EC; border: 3.5px solid #2c2c2c; border-radius: 35px; padding: 18px 30px; font-size: 26px; color: #B85D81; font-weight: bold; margin-bottom: 40px; box-shadow: 7px 7px 0px #2c2c2c; }
        .player-card { background: #F9E4EC; border: 4px solid #2c2c2c; border-radius: 32px; padding: 40px; display: flex; align-items: center; gap: 45px; margin-bottom: 45px; box-shadow: 12px 12px 0px #2c2c2c; }
        .album-art { width: 250px; height: 250px; border-radius: 22px; border: 3.5px solid #2c2c2c; object-fit: cover; background: #FFFDF9; }
        .track-info { flex: 1; }
        .badge { display: inline-block; background: #4A7C59; color: #FFFDF9; font-size: 22px; padding: 10px 25px; border-radius: 20px; margin-bottom: 18px; font-weight: bold; }
        .track-title { font-size: 50px; font-weight: 700; color: #2c2c2c; margin-bottom: 18px; }
        .clipe-btn { display: inline-block; color: #B85D81; font-weight: bold; text-decoration: none; font-size: 24px; margin-bottom: 25px; background: #FFFDF9; padding: 12px 28px; border: 3.5px solid #2c2c2c; border-radius: 16px; }
        .progress-wrapper { display: flex; align-items: center; gap: 28px; font-size: 24px; font-weight: bold; }
        .progress-bg { flex: 1; height: 26px; background: #FFFDF9; border: 3.5px solid #2c2c2c; border-radius: 18px; overflow: hidden; }
        .progress-fill { height: 100%; background: #4A7C59; width: 0%; transition: width 0.5s linear; }
        .main-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 45px; }
        .column-side { display: flex; flex-direction: column; gap: 45px; }
        .window-box { background: #FFFDF9; border: 4px solid #2c2c2c; border-radius: 32px; overflow: hidden; box-shadow: 12px 12px 0px #2c2c2c; display: flex; flex-direction: column; height: 900px; }
        .window-header { padding: 22px 32px; font-weight: bold; font-size: 26px; border-bottom: 4px solid #2c2c2c; display: flex; justify-content: space-between; align-items: center; }
        .header-green { background: #EBF5EE; color: #4A7C59; }
        .header-pink { background: #F9E4EC; color: #B85D81; }
        .header-red { background: #FDEDEC; color: #C0392B; }
        .window-content { padding: 45px; overflow-y: auto; white-space: pre-wrap; line-height: 2.1; font-size: 28px; font-weight: 700; color: #222222; flex: 1; }
        .gossip-card { background: #FFFDF9; border: 3.5px solid #2c2c2c; border-radius: 22px; padding: 32px; margin-bottom: 26px; box-shadow: 7px 7px 0px #F9E4EC; font-size: 28px; line-height: 2.0; color: #333; }
    </style>
</head>
<body>
    <div class="container">
        <div class="site-header"><h1>~* xoxo My Music Diary *~</h1></div>
        <div class="marquee-bar"><marquee scrollamount="5">★ bem-vinda ao seu diário musical interativo ★ conectado ao seu spotify em tempo real ★</marquee></div>
        <div class="player-card">
            <img id="album-img" class="album-art" src="https://via.placeholder.com/250/FFFDF9/B85D81?text=Play" alt="Capa">
            <div class="track-info">
                <span class="badge" id="status-badge">● NOW PLAYING</span>
                <div class="track-title" id="track-title">* esperando o play no Spotify... *</div>
                <div id="clipe-container"></div>
                <div class="progress-wrapper">
                    <span id="time-current">0:00</span>
                    <div class="progress-bg"><div class="progress-fill" id="progress-bar"></div></div>
                    <span id="time-total">0:00</span>
                </div>
            </div>
        </div>
        <div class="main-grid">
            <div class="column-side">
                <div class="window-box" style="height: 1850px;">
                    <div class="window-header header-green"><span>[ lyrics / tradução ]</span></div>
                    <div class="window-content" id="lyrics-box">Dê o play em uma música para ler a tradução aqui...</div>
                </div>
            </div>
            <div class="column-side">
                <div class="window-box">
                    <div class="window-header header-pink"><span>[ gossip girl / bastidores ]</span></div>
                    <div class="window-content" id="gossip-box">Os segredos vão aparecer aqui! ✨</div>
                </div>
                <div class="window-box">
                    <div class="window-header header-red"><span>[ psicologia ]</span></div>
                    <div class="window-content" id="psych-box">A análise psicológica vai aparecer aqui... 🧠</div>
                </div>
            </div>
        </div>
    </div>
    <script>
        let currentTrackId = null;
        function formatTime(ms) {
            let totalSec = Math.floor(ms / 1000);
            return Math.floor(totalSec / 60) + ":" + (totalSec % 60 < 10 ? "0" : "") + (totalSec % 60);
        }
        async function atualizarDados() {
            try {
                const res = await fetch('/api/now-playing');
                const data = await res.json();
                if (data.playing) {
                    document.getElementById('status-badge').innerText = "● TOCANDO AGORA";
                    document.getElementById('track-title').innerText = `~* ${data.name} — ${data.artist} *~`;
                    document.getElementById('time-current').innerText = formatTime(data.progress);
                    document.getElementById('time-total').innerText = formatTime(data.duration);
                    document.getElementById('progress-bar').style.width = ((data.progress / data.duration) * 100) + "%";
                    if (data.id !== currentTrackId) {
                        currentTrackId = data.id;
                        document.getElementById('album-img').src = data.image;
                        document.getElementById('lyrics-box').innerText = data.lyrics;
                        document.getElementById('gossip-box').innerHTML = Array.isArray(data.gossip) ? data.gossip.map(i => `<div class="gossip-card">${i}</div>`).join('') : data.gossip;
                        document.getElementById('psych-box').innerHTML = data.psychology;
                        document.getElementById('clipe-container').innerHTML = data.clipe ? `<a href="${data.clipe}" target="_blank" class="clipe-btn">▶ assistir clipe oficial no youtube</a>` : "";
                    }
                } else {
                    document.getElementById('status-badge').innerText = "❚❚ PAUSADO";
                }
            } catch (e) { console.log(e); }
        }
        setInterval(atualizarDados, 1500);
        atualizarDados();
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE)

@app