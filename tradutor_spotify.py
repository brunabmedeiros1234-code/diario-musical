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
        "letra_limpa": "Vem comigo\nVamos devagar e depois em ritmo acelerado\nEntre a luz e a escuridão\nMe abraça forte e depois com suavidade\n\nEu vejo a dor, vejo o prazer\nNinguém além de você, ninguém além de mim\nSó nós dois, nossos corpos juntos\nEu amo te abraçar bem perto, hoje e sempre\nEu amo acordar ao seu lado\n\nEntão vamos incomodar os vizinhos\nNo lugar onde as lágrimas encontram espaço\nOnde você deixa seus medos para trás\nÉ, um comportamento inconsequente\nUm lugar tão puro\nTão sujo e intenso\nNa cama o dia inteiro, o dia inteiro, o dia inteiro\nTransando e brigando\nEsse é o nosso paraíso e a nossa zona de guerra",
        "curiosidades_lista": [
            "✨ <b>O GRANDE LANÇAMENTO:</b> “PILLOWTALK” marcou o debut solo de Zayn Malik logo após o drama da sua saída do One Direction! A música veio sem filtro, misturando total o lado físico e emocional do sexo.",
            "🔥 <b>ALÉM DO PRAZER:</b> Zayn revelou que sexo é super natural e não deveria ser tabu. Ele define o quarto do casal como “nosso paraíso e nossa zona de guerra”, misturando dor, pureza e intensidade."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — PILLOWTALK</b><br><br><b>1. Dualidades extremas e funcionamento psíquico</b><br>A letra apresentada descreve um relacionamento profundamente intenso, marcado por dualidades extremas: luz e escuridão, dor e prazer, amor e conflito.<br><br><b>2. A Teoria do Apego e a regulação emocional</b><br>Relacionamentos que oscilam violentamente entre a fusão total e o conflito costumam apontar para um padrão de apego ansioso-ambivalente.",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    },
    "it's you": {
        "artista": "zayn",
        "letra_limpa": "Ela tem, ela tem, ela tem\nOs motivos dela para falar comigo\nEla não, ela não, ela não\nSe importa nem um pouco com o que eu preciso\n\nE eu não consigo te dizer o porquê, porque minha cabeça não consegue entender\nMe conte suas mentiras, porque eu simplesmente não consigo encarar a verdade\n\nÉ você, é você, é você\nÉ você, é você, é você",
        "curiosidades_lista": [
            "💔 <b>DR DRAMA NA ÁREA:</b> Zayn percebeu que a cremosa só age por interesse próprio e tem planos próprios. Ele sabe que está rolando mentira purinha, mas fica totalmente sem entender tanta frieza e insensibilidade."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — IT'S YOU</b><br><br>Apresenta uma dinâmica emocional bem interessante: apego, ambivalência, dificuldade de aceitar a realidade do relacionamento e sofrimento diante de uma relação que machuca.",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    },
    "befour": {
        "artista": "zayn",
        "letra_limpa": "Eu já passei por isso antes\nMas nunca desse jeito\n\nEu não bebo só pra ficar bêbado\nEu sei aproveitar o momento\nSe tem algo que eu quero\nVou atrás, mesmo que dê errado\nVou ficar na minha\nCansei de ficar remoendo isso\nE não tenho mais vontade de brigar por isso",
        "curiosidades_lista": [
            "🏆 <b>O SIGNIFICADO DE BEFOUR:</b> O título é um trocadilho genial! Significa 'Before' (antes), fazendo alusão à época anterior à sua fama mundial e ao One Direction."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — BEFOUR</b><br><br>Autonomia, identidade e a quebra de amarras externas sob a ótica da autodeterminação.",
        "link_clipe": "https://www.youtube.com/watch?v=_EaPxw5exts"
    },
    "love like this": {
        "artista": "zayn",
        "letra_limpa": "Ah, eu adoro quando você mostra, quando você mostra\nQuando você mostra que está do meu lado\n\nSe alguém tentar falar, tentar falar\nTentar falar mal de you, eu acabo com eles",
        "curiosidades_lista": [
            "🚀 <b>O GRANDE RETORNO:</b> Depois de sumir, Zayn voltou com tudo na Mercury Records!"
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — LOVE LIKE THIS</b><br><br>Disposição ao risco emocional e a quebra de defesas de apego após um histórico de cautela.",
        "link_clipe": "https://www.youtube.com/watch?v=918oGJFtjjw"
    },
    "she": {
        "artista": "zayn",
        "letra_limpa": "Ela coloca um pouco de si em cada drinque\nEla sempre sabe onde a galera está\nEla leva o cigarro à boca\nEu apago, porque ela gosta assim\nEla dança até quando está chovendo",
        "curiosidades_lista": [
            "🌙 <b>A DONA DA NOITE E DOS DRINQUES:</b> A misteriosa garota de 'She' vive até altas horas da madrugada."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — SHE</b><br><br>Busca por afeto, comportamentos de risco, ambivalência emocional e a relação entre liberdade e autodestruição.",
        "link_clipe": "https://www.youtube.com/watch?v=4MZjcAAn380"
    },
    "drunk": {
        "artista": "zayn",
        "letra_limpa": "Noites que viram madrugada, olhos vermelhos\nAmnésia no gelo\nMadrugadas, olhos vermelhos\nAmnésia, eu preciso de você\n\nAgora, não consigo nem enxergar direito\nÉ verdade, fico bêbado quando estou com você",
        "curiosidades_lista": [
            "🍷 <b>AS DUAS FORMAS DE EMBRIAGUEZ:</b> Zayn apresenta a ideia central de duas formas de embriaguez: a pelo álcool e a provocada pela paixão."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — DRUNK</b><br><br>A confusão entre a intoxicação por substâncias e a intensidade emocional de estar apaixonado.",
        "link_clipe": "https://www.youtube.com/watch?v=mpmpfKyM1i4"
    },
    "rear view": {
        "artista": "zayn",
        "letra_limpa": "Será que seu coração pode ser meu\nEnquanto você procura?\nPorque eu não tenho tempo\nPra te ajudar a encontrar as palavras\nMelodias e lembranças\nHistórias que parecem absurdas\nNão vou mentir pra você",
        "curiosidades_lista": [
            "🪞 <b>UMA CONVERSA COM O PRÓPRIO REFLEXO:</b> 'Rear View' foi construída como uma reflexão diante do espelho."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — REAR VIEW</b><br><br>Autoconhecimento, conflitos internos, ruminação e a exaustão de olhar para o próprio passado.",
        "link_clipe": "https://www.youtube.com/watch?v=xV3QUVbOhnI"
    },
    "wrong (feat. kehlani)": {
        "artista": "zayn",
        "letra_limpa": "Ah, não estamos na mesma sintonia\nMe mostra tudo sob a mesma luz\nParece certo quando a gente se solta\nRoupa no chão, porque ela é tão suave\nEssa não é uma disputa justa\nQuero deixar tudo bem claro\nVou te deixar mais molhada do que nunca",
        "curiosidades_lista": [
            "🔥 <b>A QUÍMICA DE MILHÕES:</b> Parceria impecável com a Kehlani sobre desejo noturno e expectativas desalinhadas."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — WRONG</b><br><br>Indisponibilidade emocional, intimidade física versus afetiva e o conflito de expectativas.",
        "link_clipe": "https://www.youtube.com/watch?v=gT_WbE9D-4w"
    },
    "fool for you": {
        "artista": "zayn",
        "letra_limpa": "Esse amor tá marcado\nEu preciso de você e odeio isso\nVocê fica entre um sonho e uma cena de filme\nDe certa forma, você sabe o que eu quero dizer",
        "curiosidades_lista": [
            "🎸 <b>A INFLUÊNCIA CLÁSSICA DOS BEATLES:</b> Acordes de piano inspirados nos Beatles em uma balada super dramática."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — FOOL FOR YOU</b><br><br>A rendição emocional, a perda de controle e o ciclo inevitável da vulnerabilidade.",
        "link_clipe": "https://www.youtube.com/watch?v=yM2Gaxg1O28"
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
    <link href="https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=Playfair+Display:ital,wght@0,600;1,600&display=swap" rel="stylesheet">
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
        .window-box-tall { background: #FFFDF9; border: 4px solid #2c2c2c; border-radius: 32px; overflow: hidden; box-shadow: 12px 12px 0px #2c2c2c; display: flex; flex-direction: column; height: 1850px; }
        .window-box { background: #FFFDF9; border: 4px solid #2c2c2c; border-radius: 32px; overflow: hidden; box-shadow: 12px 12px 0px #2c2c2c; display: flex; flex-direction: column; height: 900px; }
        .window-header { padding: 22px 32px; font-weight: bold; font-size: 26px; border-bottom: 4px solid #2c2c2c; display: flex; justify-content: space-between; align-items: center; }
        .header-green { background: #EBF5EE; color: #4A7C59; }
        .header-pink { background: #F9E4EC; color: #B85D81; }
        .header-red { background: #FDEDEC; color: #C0392B; }
        .window-content { padding: 45px; overflow-y: auto; white-space: pre-wrap; line-height: 2.1; font-size: 28px; font-weight: 700; color: #222222; flex: 1; }
        .gossip-card { background: #FFFDF9; border: 3.5px solid #2c2c2c; border-radius: 22px; padding: 32px; margin-bottom: 26px; box-shadow: 7px 7px 0px #F9E4EC; font-size: 28px; line-height: 2.0; color: #333; position: relative; }
        .gossip-card::before { content: "♥"; position: absolute; top: 14px; right: 22px; color: #B85D81; font-size: 24px; }
        .auth-btn-container { margin-bottom: 20px; }
        .connect-btn { background: #4A7C59; color: #FFFDF9; padding: 12px 25px; border-radius: 16px; border: 3px solid #2c2c2c; font-weight: bold; font-size: 20px; text-decoration: none; display: inline-block; box-shadow: 4px 4px 0px #2c2c2c; }
    </style>
</head>
<body>
    <div class="container">
        <div class="site-header">
            <h1>~* xoxo My Music Diary *~</h1>
        </div>

        <div class="marquee-bar">
            <marquee scrollamount="5">★ bem-vinda ao seu diário musical interativo ★ conectado ao seu spotify em tempo real ★ xoxo gossip girl ★</marquee>
        </div>

        <div class="player-card">
            <img id="album-img" class="album-art" src="https://via.placeholder.com/250/FFFDF9/B85D81?text=Play" alt="Capa">
            <div class="track-info">
                <div id="auth-container" class="auth-btn-container"></div>
                <span class="badge" id="status-badge">● NOW PLAYING</span>
                <div class="track-title" id="track-title">* esperando o play no Spotify... *</div>
                <div id="clipe-container"></div>
                <div class="progress-wrapper">
                    <span id="time-current">0:00</span>
                    <div class="progress-bg">
                        <div class="progress-fill" id="progress-bar"></div>
                    </div>
                    <span id="time-total">0:00</span>
                </div>
            </div>
        </div>

        <div class="main-grid">
            <div class="column-side">
                <div class="window-box-tall">
                    <div class="window-header header-green">
                        <span>[ lyrics / tradução ]</span>
                    </div>
                    <div class="window-content" id="lyrics-box">Dê o play em uma música para ler a tradução aqui...</div>
                </div>
            </div>

            <div class="column-side">
                <div class="window-box">
                    <div class="window-header header-pink">
                        <span>[ gossip girl / bastidores & curiosidades ]</span>
                    </div>
                    <div class="window-content" id="gossip-box">Os segredos e bastidores da faixa vão aparecer aqui em formato de revistinha! ✨</div>
                </div>

                <div class="window-box">
                    <div class="window-header header-red">
                        <span>[ psicologia ]</span>
                    </div>
                    <div class="window-content" id="psych-box">A análise psicológica da faixa vai aparecer aqui... 🧠</div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let currentTrackId = null;

        function formatTime(ms) {
            let totalSec = Math.floor(ms / 1000);
            let min = Math.floor(totalSec / 60);
            let sec = totalSec % 60;
            return min + ":" + (sec < 10 ? "0" : "") + sec;
        }

        async function atualizarDados() {
            try {
                const res = await fetch('/api/now-playing');
                const data = await res.json();

                const authDiv = document.getElementById('auth-container');
                if (data.auth_url) {
                    authDiv.innerHTML = `<a href="${data.auth_url}" class="connect-btn">🔗 Conectar com o Spotify</a>`;
                } else {
                    authDiv.innerHTML = "";
                }

                if (data.playing) {
                    document.getElementById('status-badge').innerText = "● TOCANDO AGORA";
                    document.getElementById('track-title').innerText = `~* ${data.name} — ${data.artist} *~`;
                    document.getElementById('time-current').innerText = formatTime(data.progress);
                    document.getElementById('time-total').innerText = formatTime(data.duration);
                    
                    let pct = (data.progress / data.duration) * 100;
                    document.getElementById('progress-bar').style.width = pct + "%";

                    if (data.id !== currentTrackId) {
                        currentTrackId = data.id;
                        document.getElementById('album-img').src = data.image;
                        document.getElementById('lyrics-box').innerText = data.lyrics;
                        
                        const gossipContainer = document.getElementById('gossip-box');
                        if (Array.isArray(data.gossip)) {
                            gossipContainer.innerHTML = data.gossip.map(item => `<div class="gossip-card">${item}</div>`).join('');
                        } else {
                            gossipContainer.innerHTML = `<div class="gossip-card">${data.gossip}</div>`;
                        }

                        document.getElementById('psych-box').innerHTML = data.psychology;

                        const clipeDiv = document.getElementById('clipe-container');
                        if (data.clipe) {
                            clipeDiv.innerHTML = `<a href="${data.clipe}" target="_blank" class="clipe-btn">▶ assistir clipe oficial no youtube</a>`;
                        } else {
                            clipeDiv.innerHTML = "";
                        }
                    }
                } else {
                    document.getElementById('status-badge').innerText = "❚❚ PAUSADO";
                }
            } catch (e) {
                console.log(e);
            }
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

            key = tn.lower().strip()
            if key in MUSICAS_MANUAIS:
                letra = MUSICAS_MANUAIS[key]["letra_limpa"]
                gossip = MUSICAS_MANUAIS[key]["curiosidades_lista"]
                psych = MUSICAS_MANUAIS[key]["psicologia"]
                clipe = MUSICAS_MANUAIS[key]["link_clipe"]
            else:
                letra = get_lyrics(tn, ar) or "Letra não encontrada para esta faixa."
                gossip = [f"<b>BLOG DO SPOTIFY:</b><br>Tocando agora o som de {ar}! 🎧✨"]
                psych = "🧠 <b>ANÁLISE COMPORTAMENTAL:</b><br><br>Esta faixa está tocando livremente no seu player. Analise as emoções e os sentimentos despertados pela melodia!"
                clipe = None

            return jsonify({
                "playing": True,
                "id": tid,
                "name": tn,
                "artist": ar,
                "image": img,
                "progress": p,
                "duration": dur,
                "lyrics": letra,
                "gossip": gossip,
                "psychology": psych,
                "clipe": clipe
            })
    except Exception as e:
        print(f"Erro na API: {e}")
    return jsonify({"playing": False})

if __name__ == "__main__":
    app.run(port=5000)