import os
import uuid
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, redirect, request, session, render_template_string

ID = os.getenv("SPOTIPY_CLIENT_ID", "51ebc5fc21fa4e359bebdd37175c9f13")
SEC = os.getenv("SPOTIPY_CLIENT_SECRET", "8670dd178bb0463086bdbda323dc889f")
URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:5000/callback")
SCOPES = "user-read-playback-state user-read-currently-playing"

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "xoxo-music-diary-secret-key")

TOKENS_POR_SESSAO = {}
ULTIMA_MUSICA_POR_SESSAO = {}

TRADUCAO_WHO = """Quando você estiver no escuro
E não conseguir encontrar uma saída
Quando tentar encontrar seu caminho
Mas parecer que não tem tempo pra isso

Eu vou até você
Você sabe que eu vou te salvar

Quem você vai chamar?
Quem você vai procurar?
Quando precisar de alguém
Quando precisar de companhia

Quem você vai chamar?
Quem você vai procurar?
Quando precisar de alguém
Quando precisar de companhia

Quando precisar de alguém
Quando precisar de companhia
Quando precisar de alguém
Quando precisar de companhia

Quando a água for funda demais
E você estiver fugindo de um perigo
Quando a pressão for grande demais
E você sentir o peso no coração

Eu vou até você
Você sabe que eu vou te salvar

Quem você vai chamar?
Quem você vai procurar?
Quando precisar de alguém
Quando precisar de companhia

Quem você vai chamar?
Quem você vai procurar?
Quando precisar de alguém
Quando precisar de companhia

Quando precisar de alguém
Quando precisar de companhia
Quando precisar de companhia
Quando precisar de companhia

E quem está certo? Me diz
Eu vou estar lá, bem pertinho
É o seu medo, me conta
Se tudo isso acabar, seja minha lembrança

Quem você vai chamar?
Quem você vai procurar?
Quando precisar de alguém
Quando precisar de companhia

Quem você vai chamar?
Quem você vai procurar?
Quando precisar de alguém
Quando precisar de companhia

Quando precisar de alguém
Quando precisar de companhia
Quando precisar de companhia
Quando precisar de companhia"""

CURIOSIDADES_WHO = [
    "🎬 <b>TRILHA DE GHOSTBUSTERS (2016) & ESTILO DO TÍTULO:</b> A música foi escrita para o filme <i>Ghostbusters</i>, de 2016, e recebeu o título de “WHo”, com algumas letras maiúsculas e outras minúsculas. Essa forma de escrever segue o mesmo estilo que ZAYN vinha usando nos títulos de suas músicas alguns meses antes, no álbum <i>Mind of Mine</i>, lançado em março de 2016.",
    "👻 <b>REFERÊNCIA COM NOVO SENTIDO:</b> Aqui, ZAYN faz uma referência à famosa música-tema do <i>Ghostbusters</i> original, composta e interpretada por Ray Parker Jr., mas dá a ela um sentido um pouco diferente. Em vez de simplesmente repetir a ideia da canção original, ele pergunta à pessoa para quem canta quem ela vai procurar quando estiver em apuros ou se sentir sozinha. Ao longo dos versos, ele tenta mostrar que essa pessoa deveria procurá-lo, deixando claro que está disposto a aparecer e ajudá-la quando ela mais precisar."
]

PSICOLOGIA_WHO = """🧠 <b>ANÁLISE PSICOLÓGICA — WHO</b><br><br>
A música “WHo” trabalha uma ideia psicológica bastante interessante: a necessidade de ter alguém em quem confiar quando a vida se torna difícil. Mais do que perguntar quem a outra pessoa vai procurar nos momentos de desespero, o narrador tenta se apresentar como essa figura de segurança. Ele não oferece apenas companhia; promete proteção, proximidade e disponibilidade emocional. Isso faz com que a canção possa ser interpretada como uma tentativa de construir um vínculo no qual uma pessoa se torna o ponto de apoio da outra."""

TRADUCAO_BORDESZ = """Limite
Limite
Limite
Limite, ah

Ela é a alma da festa
Não enfia essa faca em mim
É algo que ela sempre quis
É por uma boa causa, você tá fazendo tudo certo

E a gente vai pra onde o vento soprar
Não importa pra onde a gente vá
Assim como o oceano, você muda tudo que eu vejo
Eles não sabem o que eu sei
Nem há quanto tempo eu venho me segurando
Você causa um tumulto, tudo por minha causa

Então tira tudo
Vamos derrubar todas as nossas barreiras
Agora eu quero ver tudo, oh-oh
Não quero que essa vontade passe
Então vamos cruzar os limites que deixamos pra trás
Agora eu quero ver tudo, oh-oh

Você estava bem no limite
Me dê tudo isso, me dê você por inteiro
Não precisa se jogar de cabeça, não preciso de provas"""

TRADUCAO_TIO = """Eu sinto o gosto na sua boca e não consigo largar
Você é louca como eu, não consegue perceber?
A gente pode dar um jeito nisso, eu acredito
Você se excita comigo, é quase como se estivesse traindo

Eu só quero ficar te olhando enquanto você tira
Tira toda a maquiagem, amor, tira tudo
Eu só quero ficar te olhando enquanto você tira
Tira toda a roupa e deixa eu te ver tirando tudo"""

TRADUCAO_LIKE_I_WOULD = """Ei, tudo bem? Quanto tempo, né?
Não sou muito de ficar falando dessas coisas
Mas pensei em saber como você tá, enquanto acendo um cigarro
É meio frio da minha parte, eu sei
É meio frio da minha parte

Ele não vai te tocar como eu
Não vai te amar como eu amaria
Ele não conhece seu corpo
Não sabe te dar prazer
Não vai te amar como eu amaria
Como eu amaria"""

PSICOLOGIA_LIKE_I_WOULD = """🧠 <b>ANÁLISE COMPORTAMENTAL — LIKE I WOULD</b><br><br>
“Like I Would” apresenta uma situação emocional bastante específica: alguém que, mesmo depois do término de um relacionamento, continua se percebendo como insubstituível na vida da outra pessoa."""

CURIOSIDADES_TIO = [
    "💋 <b>O SIGNIFICADO DE TIO:</b> 'TiO' é abreviação de <i>'Take It Off'</i> ('Tire Tudo'), o pedido central que dá o tom sensual e direto da faixa no álbum <i>Mind of Mine</i>.",
    "🎭 <b>DESPIR AS MÁSCARAS:</b> A letra fala tanto de tirar a roupa quanto de tirar a maquiagem e as defesas."
]

PSICOLOGIA_TIO = """🧠 <b>ANÁLISE PSICOLÓGICA DE “TiO”, DO ZAYN</b><br><br>
“TiO” pode ser interpretada, à primeira vista, como uma música essencialmente sobre desejo sexual e atração física, mas também dialoga com a ideia de tirar camadas e máscaras."""

CURIOSIDADES_BORDESZ = [
    "🚧 <b>O SIGNIFICADO DE BORDERSZ:</b> O título estilizado <i>'BoRdErSz'</i> remete diretamente a fronteiras e limites no álbum <i>Mind of Mine</i>.",
    "🌊 <b>MARÉ ALTA E TUMULTO:</b> A letra brinca com imagens de movimento e transformação."
]

PSICOLOGIA_BORDESZ = """🧠 <b>ANÁLISE COMPORTAMENTAL — A PSICOLOGIA POR TRÁS DE “BoRdErSz”, DE ZAYN</b><br><br>
A letra apresenta uma dinâmica psicológica de alguém que se encontra diante de seus próprios limites e decide, pouco a pouco, atravessá-los."""

TRADUCAO_CRUEL = """O rádio do carro grita, entre ruídos e lágrimas
Notícias de mortes na TV, e então aparece você
É tudo tão absurdo, tão louco, que eu não consigo me concentrar
Só consigo enxergar sua silhueta, ah

O sol nasce em Hollywood, estamos há dias sem dormir
Um desastre perfeito: eu e você"""

CURIOSIDADES_CRUEL = [
    "📰 <b>NOTICIÁRIO VIOLENTO E REFÚGIO:</b> Em meio a um mundo 'absurdo' e 'louco', a garota distrai o narrador e o lembra de que ainda existem coisas boas.",
    "📹 <b>CCTV E GRAVAÇÃO EM LOOP:</b> Simboliza as lembranças passando sem parar na mente."
]

PSICOLOGIA_CRUEL = """🧠 <b>ANÁLISE PSICOLÓGICA — CRUEL</b><br><br>
“Cruel” apresenta um contraste psicológico entre a brutalidade do mundo exterior e a experiência de intimidade vivida pelo narrador."""

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
Eu amo acordar ao seu lado""",
        "curiosidades_lista": [
            "✨ <b>O GRANDE LANÇAMENTO:</b> “PILLOWTALK” marcou o debut solo de Zayn Malik logo após sua saída do One Direction!"
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — PILLOWTALK</b><br><br>A letra descreve um relacionamento intenso marcado por dualidades como luz e escuridão, dor e prazer.""",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    },
    "it's you": {
        "artista": "zayn",
        "letra_limpa": """Ela tem, ela tem, ela tem
Os motivos dela para falar comigo
Ela não, ela não, ela não
Se importa nem um pouco com o que eu preciso

É você, é você, é você
É você, é você, é você""",
        "curiosidades_lista": [
            "💔 <b>A DOR DE COTOVELO:</b> Mesmo machucado, ele confessa que ela é a única que ele quer."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — IT'S YOU</b><br><br>Apresenta apego, ambivalência e dificuldade de aceitar a realidade de uma relação que machuca.""",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    },
    "befour": {
        "artista": "zayn",
        "letra_limpa": """Eu já passei por isso antes
Mas nunca desse jeito

Entorpecido no alto de um telhado
Coloco fogo em tudo
Só pra provar pra mim mesmo
Que estou vivendo no limite""",
        "curiosidades_lista": [
            "🏆 <b>O SIGNIFICADO DE BEFOUR:</b> Trocadilho com 'Before' e o número '4', marcando sua nova fase solo."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — BEFOUR</b><br><br>Explora identidade, autonomia e a necessidade de recuperar o controle das próprias escolhas.""",
        "link_clipe": "https://www.youtube.com/watch?v=_EaPxw5exts"
    },
    "love like this": {
        "artista": "zayn",
        "letra_limpa": """Ah, eu adoro quando você mostra
Quando você mostra que está do meu lado

Acho que isso é um amor assim
Normalmente, eu nunca me entregaria desse jeito
Mas quero apostar todas as minhas fichas""",
        "curiosidades_lista": [
            "🃏 <b>APOSTANDO TUDO:</b> Ele confessa que não se entrega fácil, mas decide ir all-in."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL:</b><br><br>Foco na disposição ao risco emocional e na quebra de defesas de apego.",
        "link_clipe": "https://www.youtube.com/watch?v=918oGJFtjjw"
    },
    "she": {
        "artista": "zayn",
        "letra_limpa": """Ela coloca um pouco de si em cada drinque
Ela dança até quando está chovendo

Ela quer alguém que a ame e a abrace
Ela quer alguém que saiba amá-la de verdade""",
        "curiosidades_lista": [
            "🌧️ <b>DANÇANDO NA CHUVA:</b> Transmite ousadia e rebeldia em meio ao temporal."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — SHE</b><br><br>Retrata uma dinâmica entre busca por liberdade, regulação emocional e necessidade de acolhimento.""",
        "link_clipe": "https://www.youtube.com/watch?v=4MZjcAAn380"
    },
    "drunk": {
        "artista": "zayn",
        "letra_limpa": """Noites que viram madrugada, olhos vermelhos
Amnésia no gelo

Bêbados durante todo o verão
Passamos o verão inteiro bêbados""",
        "curiosidades_lista": [
            "🍷 <b>DUAS FORMAS DE EMBRIAGUEZ:</b> Mistura a euforia das noites com a intensidade da paixão."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — DRUNK</b><br><br>Explora sistema de recompensa, euforia e perda de controle emocional.""",
        "link_clipe": "https://www.youtube.com/watch?v=mpmpfKyM1i4"
    },
    "rear view": {
        "artista": "zayn",
        "letra_limpa": """Desde que você
Olhe nos meus olhos
Eu vou aonde você estiver
E vou seguir seus passos

Nunca duvidei de mim mesmo
Mas duvidei de você
Cansei de me olhar
Pelo retrovisor""",
        "curiosidades_lista": [
            "🪞 <b>REFLEXO NO ESPELHO:</b> Remete a olhar para o passado enquanto tenta seguir em frente."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — REAR VIEW</b><br><br>Trabalha ruminação, autoconceito e a exaustão de olhar pelo retrovisor.""",
        "link_clipe": "https://www.youtube.com/watch?v=xV3QUVbOhnI"
    },
    "wrong (feat. kehlani)": {
        "artista": "zayn",
        "letra_limpa": """Você está procurando meu amor no lugar errado
Não pense que só porque está comigo, isso é de verdade""",
        "curiosidades_lista": [
            "🔥 <b>PARCERIA COM KEHLANI:</b> Fala sobre expectativas desalinhadas entre intimidade e compromisso."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — WRONG</b><br><br>Aborda indisponibilidade emocional, dissonância cognitiva e limites na intimidade.""",
        "link_clipe": "https://www.youtube.com/watch?v=gT_WbE9D-4w"
    },
    "fool for you": {
        "artista": "zayn",
        "letra_limpa": """Esse amor tá marcado
Eu preciso de você e odeio isso

Porque eu sou um bobo por você
E por tudo que você faz""",
        "curiosidades_lista": [
            "🎸 <b>INFLUÊNCIA CLÁSSICA:</b> Destaca-se pela sonoridade mais acústica e orgânica em <i>Mind of Mine</i>."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — FOOL FOR YOU</b><br><br>Retrata a contradição entre perceber o risco e ainda assim se entregar.""",
        "link_clipe": "https://www.youtube.com/watch?v=yM2Gaxg1O28"
    },
    "bordersz": {
        "artista": "zayn",
        "letra_limpa": TRADUCAO_BORDESZ,
        "curiosidades_lista": CURIOSIDADES_BORDESZ,
        "psicologia": PSICOLOGIA_BORDESZ,
        "link_clipe": "https://www.youtube.com/watch?v=918oGJFtjjw"
    },
    "borderz": {
        "artista": "zayn",
        "letra_limpa": TRADUCAO_BORDESZ,
        "curiosidades_lista": CURIOSIDADES_BORDESZ,
        "psicologia": PSICOLOGIA_BORDESZ,
        "link_clipe": "https://www.youtube.com/watch?v=918oGJFtjjw"
    },
    "tio": {
        "artista": "zayn",
        "letra_limpa": TRADUCAO_TIO,
        "curiosidades_lista": CURIOSIDADES_TIO,
        "psicologia": PSICOLOGIA_TIO,
        "link_clipe": None
    },
    "like i would": {
        "artista": "zayn",
        "letra_limpa": TRADUCAO_LIKE_I_WOULD,
        "curiosidades_lista": [
            "🔥 <b>LIGAÇÃO DA MADRUGADA:</b> Captura aquele impulso noturno e a comparação após um término."
        ],
        "psicologia": PSICOLOGIA_LIKE_I_WOULD,
        "link_clipe": None
    },
    "who": {
        "artista": "zayn",
        "letra_limpa": TRADUCAO_WHO,
        "curiosidades_lista": CURIOSIDADES_WHO,
        "psicologia": PSICOLOGIA_WHO,
        "link_clipe": None
    },
    "cruel": {
        "artista": "snakehips",
        "letra_limpa": TRADUCAO_CRUEL,
        "curiosidades_lista": CURIOSIDADES_CRUEL,
        "psicologia": PSICOLOGIA_CRUEL,
        "link_clipe": None
    },
    "back to life": {
        "artista": "zayn",
        "letra_limpa": """Oh, oh
Oh, oh

E se eu mudasse de ideia?
E se eu dissesse que acabou?
Estou voando há tanto tempo
Que já nem lembro como era estar sóbrio

Sinceramente, ela é a única que cuida de mim
Me dá fôlego quando fica difícil respirar
Esteja eu certo ou errado
Ela está sempre do meu lado
Sei que ela vai me trazer de volta à vida""",
        "curiosidades_lista": [
            "🥺 <b>ANSIEDADE E CUIDADO:</b> Em “Back To Life”, ZAYN fala sobre ter alguém que ajuda a enfrentar momentos difíceis.",
            "🇵🇰 <b>RAÍZES:</b> Traz influências melódicas ligadas à sua herança cultural e à ideia de reerguer-se."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — BACK TO LIFE</b><br><br>Explora a necessidade de apoio emocional e o papel de alguém que ajuda a recuperar o fôlego.""",
        "link_clipe": None
    },
    "common": {
        "artista": "zayn",
        "letra_limpa": """Sempre olhando por trás das minhas barreiras
Sempre me senti isolado, oh-oh-oh
Não sei por que eu era tão fechado
Mas vou encontrar um jeito de deixar você entrar

Quando me deito na sua cama, preciso de você junto ao meu peito
Para me aquecer o tempo todo, para tirar meu fôlego
Isso está escrito nos seus lábios: não existe nada de comum entre nós""",
        "curiosidades_lista": [
            "💘 <b>UMA CONEXÃO FORA DO COMUM:</b> Em “Common” (do álbum <i>Icarus Falls</i>), ZAYN fala sobre baixar as barreiras e viver algo especial."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — COMMON</b><br><br>Fala sobre deixar as defesas emocionais de lado e buscar intimidade genuína.""",
        "link_clipe": None
    },
    "drop dead": {
        "artista": "zayn",
        "letra_limpa": """Eu sei que o bar fecha às onze
Mas espero que você nunca termine essa cerveja
Você sabe cantar de cor “Just Like Heaven”

Uma noite, estava entediada na cama
E fui fuçar sua vida na internet
É minha intuição feminina
Porque eu sempre imaginei nós dois exatamente assim""",
        "curiosidades_lista": [
            "💗 <b>COMEÇO DE PAIXÃO:</b> Retrata o encantamento do início, a vontade de prolongar o encontro e a imaginação acelerando."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — DROP DEAD</b><br><br>Mostra a mistura de empolgação, antecipação e idealização no começo de uma paixão.""",
        "link_clipe": None
    },
    "i don't wanna live forever": {
        "artista": "zayn",
        "letra_limpa": """Fico de olhos bem abertos, sem conseguir dormir
Atrás destas quatro paredes, esperando que você ligue
É uma existência cruel
Como se não houvesse motivo algum para continuar esperando

Não quero viver para sempre
Porque sei que estaria vivendo em vão
Só quero continuar chamando pelo seu nome
Até você voltar para casa""",
        "curiosidades_lista": [
            "🎬 <b>TRILHA E DUETO:</b> Faixa intensa sobre saudade, espera e a sensação de vazio diante da ausência."
        ],
        "psicologia": """🧠 <b>PAPO PSICOLÓGICO — I DON'T WANNA LIVE FOREVER</b><br><br>Aborda a saudade, a espera ansiosa e o impacto emocional da ausência.""",
        "link_clipe": None
    },
    "let me": {
        "artista": "zayn",
        "letra_limpa": """Meu bem, o que a gente vive na cama tem significado
Sei que, dessa vez, você vai ficar até amanhecer
Dias de preguiça debaixo das cobertas e sorvete de baunilha
Quero mais do que apenas uma noite juntos, quero você só pra mim

Deixa eu ser o homem da sua vida
Pra que eu possa te amar
E, se você me deixar ser esse homem,
Vou cuidar de você""",
        "curiosidades_lista": [
            "💫 <b>MAIS QUE UMA NOITE:</b> Mostra o desejo de exclusividade, cuidado e parceria contínua."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — LET ME</b><br><br>Explora a transição do desejo imediato para a vontade de construir algo duradouro.""",
        "link_clipe": None
    },
    "natural": {
        "artista": "zayn",
        "letra_limpa": """É como respirar, como falar
Quando a gente se toca, é como uma força da natureza
Não é só um sentimento, vamos acreditar
O nascimento do amor, como uma força da natureza

Parece tão natural, tão natural
Quando a gente se entrega
Como uma força da natureza""",
        "curiosidades_lista": [
            "💗 <b>ESPONTANEIDADE:</b> Retrata uma conexão sentida como fluida, sem esforço e intensa."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — NATURAL</b><br><br>Fala sobre espontaneidade e a sensação de encaixe natural entre duas pessoas.""",
        "link_clipe": None
    },
    "stupid song": {
        "artista": "zayn",
        "letra_limpa": """Nova York nunca pareceu tão triste e cinzenta
Meus amigos estão fumando uns baseados no banheiro
Eles dizem que o amor de verdade é uma prisão que faz você se sentir livre

Você é uma faísca no escuro e minhas roupas estão pegando fogo
Sou um carro disparado pela avenida, sem freios
E eu quero você mais do que qualquer música boba conseguiria expressar""",
        "curiosidades_lista": [
            "💘 <b>QUANDO A PAIXÃO TOMA CONTA:</b> Explora o lado intenso e inquieto de estar apaixonada."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — STUPID SONG</b><br><br>Aborda pensamentos recorrentes e a intensidade do desejo e da paixão.""",
        "link_clipe": None
    }
}


def normalizar_chave_faixa(texto):
    if not texto:
        return ""
    return (
        texto.lower()
        .replace("’", "'")
        .replace("‘", "'")
        .replace("´", "'")
        .replace("`", "'")
        .strip()
    )


def encontrar_chave_manual(titulo_faixa):
    titulo = normalizar_chave_faixa(titulo_faixa)
    if titulo in MUSICAS_MANUAIS:
        return titulo

    titulo_limpo = titulo.split("(")[0].split(" - ")[0].strip()
    if titulo_limpo in MUSICAS_MANUAIS:
        return titulo_limpo

    for chave in MUSICAS_MANUAIS:
        if chave in titulo:
            return chave

    return None


def get_lyrics(t, a):
    if encontrar_chave_manual(t):
        return None
    try:
        url = f"https://lrclib.net/api/get?artist_name={a}&track_name={t}"
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            return r.json().get("plainLyrics")
    except Exception:
        pass
    return None


def criar_oauth():
    return SpotifyOAuth(
        client_id=ID,
        client_secret=SEC,
        redirect_uri=URI,
        scope=SCOPES,
        open_browser=False,
    )


def obter_cliente_spotify_usuario():
    sid = session.get("sid")
    if not sid or sid not in TOKENS_POR_SESSAO:
        return None

    token_info = TOKENS_POR_SESSAO[sid]
    auth_manager = criar_oauth()

    if auth_manager.is_token_expired(token_info):
        try:
            token_info = auth_manager.refresh_access_token(token_info["refresh_token"])
            TOKENS_POR_SESSAO[sid] = token_info
        except Exception:
            TOKENS_POR_SESSAO.pop(sid, None)
            return None

    return spotipy.Spotify(auth=token_info["access_token"])


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
        .site-header h1 {
            font-family: 'VT323', monospace;
            font-size: 90px;
            color: #B85D81;
            text-shadow: 4px 4px 0px #FFFDF9;
            letter-spacing: 6px;
        }
        .marquee-bar {
            background: #F9E4EC;
            border: 3.5px solid #2c2c2c;
            border-radius: 35px;
            padding: 18px 30px;
            font-size: 26px;
            color: #B85D81;
            font-weight: bold;
            margin-bottom: 40px;
            box-shadow: 7px 7px 0px #2c2c2c;
        }
        .auth-box {
            background: #FFFDF9;
            border: 4px solid #2c2c2c;
            border-radius: 32px;
            padding: 60px 40px;
            text-align: center;
            box-shadow: 12px 12px 0px #2c2c2c;
            max-width: 900px;
            margin: 40px auto;
        }
        .auth-box p {
            font-size: 26px;
            line-height: 1.7;
            margin-bottom: 35px;
        }
        .spotify-btn {
            display: inline-block;
            background: #4A7C59;
            color: #FFFDF9;
            font-size: 28px;
            font-weight: bold;
            text-decoration: none;
            padding: 18px 36px;
            border: 4px solid #2c2c2c;
            border-radius: 20px;
            box-shadow: 7px 7px 0px #2c2c2c;
        }
        .spotify-btn:hover { transform: translate(-2px, -2px); }
        .player-card {
            background: #F9E4EC;
            border: 4px solid #2c2c2c;
            border-radius: 32px;
            padding: 40px;
            display: flex;
            align-items: center;
            gap: 45px;
            margin-bottom: 45px;
            box-shadow: 12px 12px 0px #2c2c2c;
        }
        .album-art {
            width: 250px;
            height: 250px;
            border-radius: 22px;
            border: 3.5px solid #2c2c2c;
            object-fit: cover;
            background: #FFFDF9;
        }
        .track-info { flex: 1; }
        .badge {
            display: inline-block;
            background: #4A7C59;
            color: #FFFDF9;
            font-size: 22px;
            padding: 10px 25px;
            border-radius: 20px;
            margin-bottom: 18px;
            font-weight: bold;
        }
        .track-title {
            font-size: 50px;
            font-weight: 700;
            color: #2c2c2c;
            margin-bottom: 18px;
        }
        .clipe-btn {
            display: inline-block;
            color: #B85D81;
            font-weight: bold;
            text-decoration: none;
            font-size: 24px;
            margin-bottom: 25px;
            background: #FFFDF9;
            padding: 12px 28px;
            border: 3.5px solid #2c2c2c;
            border-radius: 16px;
        }
        .progress-wrapper {
            display: flex;
            align-items: center;
            gap: 28px;
            font-size: 24px;
            font-weight: bold;
        }
        .progress-bg {
            flex: 1;
            height: 26px;
            background: #FFFDF9;
            border: 3.5px solid #2c2c2c;
            border-radius: 18px;
            overflow: hidden;
        }
        .progress-fill {
            height: 100%;
            background: #4A7C59;
            width: 0%;
            transition: width 0.5s linear;
        }
        .main-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 45px;
        }
        .column-side { display: flex; flex-direction: column; gap: 45px; }
        .window-box-tall {
            background: #FFFDF9;
            border: 4px solid #2c2c2c;
            border-radius: 32px;
            overflow: hidden;
            box-shadow: 12px 12px 0px #2c2c2c;
            display: flex;
            flex-direction: column;
            height: 1850px;
        }
        .window-box {
            background: #FFFDF9;
            border: 4px solid #2c2c2c;
            border-radius: 32px;
            overflow: hidden;
            box-shadow: 12px 12px 0px #2c2c2c;
            display: flex;
            flex-direction: column;
            height: 900px;
        }
        .window-header {
            padding: 22px 32px;
            font-weight: bold;
            font-size: 26px;
            border-bottom: 4px solid #2c2c2c;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header-green { background: #EBF5EE; color: #4A7C59; }
        .header-pink { background: #F9E4EC; color: #B85D81; }
        .header-red { background: #FDEDEC; color: #C0392B; }
        .window-dots span {
            display: inline-block;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            border: 3.5px solid #2c2c2c;
            margin-left: 12px;
            background: #FFFDF9;
        }
        .window-content {
            padding: 45px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 2.1;
            font-size: 28px;
            font-weight: 700;
            color: #222222;
            flex: 1;
        }
        .gossip-card {
            background: #FFFDF9;
            border: 3.5px solid #2c2c2c;
            border-radius: 22px;
            padding: 32px;
            margin-bottom: 26px;
            box-shadow: 7px 7px 0px #F9E4EC;
            font-size: 28px;
            line-height: 2.0;
            color: #333;
            position: relative;
        }
        .gossip-card::before {
            content: "♥";
            position: absolute;
            top: 14px;
            right: 22px;
            color: #B85D81;
            font-size: 24px;
        }
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

        {% if not logado %}
        <div class="auth-box">
            <p>Conecte a sua conta do Spotify para acompanhar a música que está tocando agora, ver a tradução, curiosidades e análise psicológica em tempo real.</p>
            <a href="/login" class="spotify-btn">♪ Entrar com o Spotify</a>
        </div>
        {% else %}
        <div class="player-card">
            <img id="album-img" class="album-art" src="https://via.placeholder.com/250/FFFDF9/B85D81?text=Play" alt="Capa">
            <div class="track-info">
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
                        <div class="window-dots"><span></span><span></span><span></span></div>
                    </div>
                    <div class="window-content" id="lyrics-box">Dê o play em uma música para ler a tradução aqui...</div>
                </div>
            </div>

            <div class="column-side">
                <div class="window-box">
                    <div class="window-header header-pink">
                        <span>[ gossip girl / bastidores & curiosidades ]</span>
                        <div class="window-dots"><span></span><span></span><span></span></div>
                    </div>
                    <div class="window-content" id="gossip-box">Os segredos e bastidores da faixa vão aparecer aqui em formato de revistinha! ✨</div>
                </div>

                <div class="window-box">
                    <div class="window-header header-red">
                        <span>[ psicologia ]</span>
                        <div class="window-dots"><span></span><span></span><span></span></div>
                    </div>
                    <div class="window-content" id="psych-box">A análise psicológica da faixa vai aparecer aqui... 🧠</div>
                </div>
            </div>
        </div>
        {% endif %}
    </div>

    {% if logado %}
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
                if (res.status === 401) {
                    window.location.href = '/';
                    return;
                }
                const data = await res.json();

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
    {% endif %}
</body>
</html>
"""


@app.route("/")
def index():
    sp = obter_cliente_spotify_usuario()
    return render_template_string(HTML_TEMPLATE, logado=bool(sp))


@app.route("/login")
def login():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    auth_manager = criar_oauth()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())

    error = request.args.get("error")
    if error:
        return f"Erro ao autorizar no Spotify: {error}", 400

    code = request.args.get("code")
    if not code:
        return "Código de autorização não recebido.", 400

    auth_manager = criar_oauth()
    token_info = auth_manager.get_access_token(code, as_dict=True)
    TOKENS_POR_SESSAO[session["sid"]] = token_info
    return redirect("/")


@app.route("/api/now-playing")
def now_playing():
    sp = obter_cliente_spotify_usuario()
    if not sp:
        return jsonify({"playing": False, "logged_out": True}), 401

    sid = session.get("sid")
    try:
        cur = sp.current_user_playing_track()
        if cur and cur.get("is_playing") and cur.get("item"):
            tr = cur["item"]
            tn = tr["name"]
            ar = tr["artists"][0]["name"]
            tid = tr["id"]
            img = tr["album"]["images"][0]["url"]
            p = cur.get("progress_ms", 0)
            dur = tr.get("duration_ms", 1)

            if sid:
                ULTIMA_MUSICA_POR_SESSAO[sid] = tid

            key = encontrar_chave_manual(tn)
            if key:
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
    except Exception:
        pass
    return jsonify({"playing": False})


if __name__ == "__main__":
    print("\n✨ Seu site está no ar! Abra no navegador: http://127.0.0.1:5000 ✨\n")
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))