import glob
import json
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
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

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


def _registrar_entrada_json(chave, info):
    if not isinstance(info, dict):
        return
    chave_limpa = normalizar_chave_faixa(chave)
    if not chave_limpa:
        return
    MUSICAS_MANUAIS[chave_limpa] = {
        "artista": info.get("artista", ""),
        "letra_limpa": info.get("letra_limpa", ""),
        "curiosidades_lista": info.get("curiosidades_lista", []),
        "psicologia": info.get("psicologia", ""),
        "link_clipe": info.get("link_clipe"),
    }


def carregar_musicas_extras():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_extras = os.path.join(base_dir, "musicas_extras")
    arquivo_raiz = os.path.join(base_dir, "musicas_extra.json")

    arquivos_para_ler = []
    if os.path.isdir(pasta_extras):
        arquivos_para_ler.extend(sorted(glob.glob(os.path.join(pasta_extras, "*.json"))))
    if os.path.exists(arquivo_raiz):
        arquivos_para_ler.append(arquivo_raiz)

    for caminho in arquivos_para_ler:
        try:
            with open(caminho, "r", encoding="utf-8") as f:
                dados = json.load(f)
            if not isinstance(dados, dict):
                continue
            if "letra_limpa" in dados or "curiosidades_lista" in dados or "psicologia" in dados:
                chaves = dados.get("chaves") or [
                    os.path.splitext(os.path.basename(caminho))[0].replace("_", " ")
                ]
                for ch in chaves:
                    _registrar_entrada_json(ch, dados)
            else:
                for chave, info in dados.items():
                    _registrar_entrada_json(chave, info)
        except Exception as e:
            print(f"[AVISO] Falha ao carregar JSON '{caminho}': {e}")


carregar_musicas_extras()


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
    token_info = session.get("spotify_token")
    if not token_info:
        return None

    auth_manager = criar_oauth()

    if auth_manager.is_token_expired(token_info):
        try:
            token_info = auth_manager.refresh_access_token(token_info["refresh_token"])
            session["spotify_token"] = token_info
            session.modified = True
        except Exception:
            session.pop("spotify_token", None)
            return None

    return spotipy.Spotify(auth=token_info["access_token"])


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>XOXO My Music Diary • Revista Teen & Diário Musical (2013–2014)</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&family=Quicksand:wght@500;600;700&family=Space+Mono:ital,wght@0,400;0,700;1,400&family=VT323&display=swap" rel="stylesheet">
    <style>
        :root {
            --pink: #F7B6CE;
            --pink-hot: #E05A8D;
            --pink-soft: #FCEAF1;
            --mint: #C8EBD6;
            --mint-deep: #3D7352;
            --yellow: #FCE883;
            --yellow-soft: #FFF8CE;
            --cream: #FFFDF8;
            --paper: #FAF5EA;
            --ink: #1C1C1C;
            --ink-soft: #3B3B3B;
            --shadow: 6px 6px 0px #1C1C1C;
            --shadow-lg: 9px 9px 0px #1C1C1C;
            --shadow-sm: 4px 4px 0px #1C1C1C;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            background-color: #E5F2EA;
            background-image:
                radial-gradient(#B5D8C3 2.2px, transparent 2.2px),
                radial-gradient(#F3C2D6 1.6px, transparent 1.6px);
            background-size: 30px 30px, 60px 60px;
            background-position: 0 0, 15px 15px;
            font-family: 'Quicksand', sans-serif;
            color: var(--ink);
            padding: 24px 18px 80px;
            min-height: 100vh;
            line-height: 1.65;
        }

        .mag-shell {
            max-width: 1240px;
            margin: 0 auto;
        }

        /* FAKE TAPE / SCRAPBOOK ACCENTS */
        .tape {
            position: absolute;
            width: 88px;
            height: 22px;
            background: rgba(252, 232, 131, 0.85);
            border: 2px solid var(--ink);
            box-shadow: 2px 2px 0px var(--ink);
            z-index: 4;
            pointer-events: none;
        }
        .tape-tl { top: -10px; left: 26px; transform: rotate(-6deg); }
        .tape-tr { top: -10px; right: 28px; transform: rotate(5deg); background: rgba(200, 235, 214, 0.9); }

        /* SELOS E ETIQUETAS DE REVISTA TEEN 2013-2014 */
        .badge-tag {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.6px;
            text-transform: uppercase;
            padding: 5px 12px;
            border: 2.5px solid var(--ink);
            border-radius: 999px;
            box-shadow: 3px 3px 0px var(--ink);
            background: var(--cream);
            color: var(--ink);
        }
        .tag-hot { background: var(--pink); transform: rotate(-2deg); }
        .tag-new { background: var(--yellow); transform: rotate(1.5deg); }
        .tag-mint { background: var(--mint); transform: rotate(-1deg); }
        .tag-crush { background: #FFD6E6; transform: rotate(2deg); }

        /* CAPA / CABEÇALHO EDITORIAL */
        .masthead {
            background: var(--cream);
            border: 3.5px solid var(--ink);
            border-radius: 26px;
            padding: 24px 28px 22px;
            box-shadow: var(--shadow-lg);
            position: relative;
            margin-bottom: 18px;
        }
        .masthead-strip {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding-bottom: 14px;
            border-bottom: 2.5px dashed var(--ink);
            margin-bottom: 16px;
        }
        .masthead-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .issue-meta {
            font-family: 'Space Mono', monospace;
            font-size: 13px;
            font-weight: 700;
            background: var(--yellow-soft);
            padding: 6px 12px;
            border: 2px solid var(--ink);
            border-radius: 12px;
        }
        .logo-block {
            text-align: center;
            padding: 6px 0 8px;
        }
        .logo-kicker {
            font-family: 'Caveat', cursive;
            font-size: 27px;
            font-weight: 700;
            color: var(--pink-hot);
            line-height: 1.1;
            transform: rotate(-1.5deg);
            display: inline-block;
        }
        .logo-main {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: clamp(40px, 7.2vw, 76px);
            line-height: 1.02;
            color: var(--pink-hot);
            text-shadow: 3px 3px 0px var(--yellow), 6px 6px 0px var(--ink);
            letter-spacing: -0.5px;
            margin: 4px 0;
        }
        .logo-tagline {
            font-family: 'VT323', monospace;
            font-size: 26px;
            letter-spacing: 2px;
            color: var(--ink);
        }

        /* NAVEGAÇÃO PORTAL TEEN */
        .portal-nav {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 10px;
            margin-top: 16px;
            padding-top: 16px;
            border-top: 2.5px solid var(--ink);
        }
        .nav-pill {
            background: var(--paper);
            color: var(--ink);
            border: 2.5px solid var(--ink);
            border-radius: 14px;
            padding: 9px 15px;
            font-family: 'Space Mono', monospace;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 3px 3px 0px var(--ink);
            transition: transform 0.1s ease, background 0.1s ease;
        }
        .nav-pill:hover {
            background: var(--yellow-soft);
            transform: translate(-1px, -1px);
        }
        .nav-pill.active {
            background: var(--pink);
            transform: translate(2px, 2px);
            box-shadow: 1px 1px 0px var(--ink);
        }

        /* MARQUEE */
        .ticker-bar {
            background: var(--pink-soft);
            border: 3px solid var(--ink);
            border-radius: 999px;
            padding: 10px 18px;
            margin-bottom: 22px;
            box-shadow: var(--shadow-sm);
            font-family: 'Space Mono', monospace;
            font-size: 14px;
            font-weight: 700;
            color: #8A2B52;
        }

        /* SEÇÕES DO PORTAL (HOME, MÚSICAS, ARTISTAS, ÁLBUNS, PLAYLISTS, TESTES, SOBRE) */
        .portal-section {
            display: none;
        }
        .portal-section.active {
            display: block;
        }

        /* TELA DE LOGIN SPOTIFY */
        .auth-card {
            background: var(--cream);
            border: 3.5px solid var(--ink);
            border-radius: 26px;
            padding: 40px 28px;
            text-align: center;
            box-shadow: var(--shadow-lg);
            max-width: 780px;
            margin: 18px auto 32px;
            position: relative;
        }
        .auth-card h2 {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: 36px;
            color: var(--pink-hot);
            margin-bottom: 12px;
        }
        .auth-card p {
            font-size: 18px;
            font-weight: 500;
            color: var(--ink-soft);
            max-width: 600px;
            margin: 0 auto 24px;
        }
        .btn-spotify {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            background: var(--mint-deep);
            color: #FFFFFF;
            text-decoration: none;
            font-family: 'Space Mono', monospace;
            font-size: 17px;
            font-weight: 700;
            padding: 14px 28px;
            border: 3px solid var(--ink);
            border-radius: 16px;
            box-shadow: var(--shadow-sm);
            transition: transform 0.12s ease;
        }
        .btn-spotify:hover { transform: translate(-2px, -2px); }

        /* PLAYER DE BLOG ANTIGO (2013-2014) */
        .retro-player {
            background: linear-gradient(135deg, var(--pink-soft) 0%, var(--cream) 55%, var(--yellow-soft) 100%);
            border: 3.5px solid var(--ink);
            border-radius: 26px;
            padding: 24px;
            box-shadow: var(--shadow-lg);
            margin-bottom: 24px;
            position: relative;
        }
        .player-top-badges {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        }
        .player-main {
            display: grid;
            grid-template-columns: 185px 1fr;
            gap: 26px;
            align-items: center;
        }
        .polaroid-frame {
            background: #FFFFFF;
            border: 3px solid var(--ink);
            border-radius: 14px;
            padding: 10px 10px 24px;
            box-shadow: 5px 5px 0px var(--ink);
            transform: rotate(-2deg);
            text-align: center;
        }
        .polaroid-frame img {
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border: 2.5px solid var(--ink);
            border-radius: 10px;
            display: block;
            background: var(--paper);
        }
        .polaroid-caption {
            font-family: 'Caveat', cursive;
            font-size: 20px;
            font-weight: 700;
            color: var(--ink);
            margin-top: 6px;
            line-height: 1.1;
        }
        .player-status-row {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 10px;
            margin-bottom: 8px;
        }
        .status-pill {
            background: var(--mint-deep);
            color: #FFFDF8;
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            padding: 5px 13px;
            border-radius: 999px;
            border: 2px solid var(--ink);
        }
        .now-track-title {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: clamp(26px, 4vw, 42px);
            line-height: 1.15;
            color: var(--ink);
            margin-bottom: 4px;
        }
        .now-track-artist {
            font-family: 'Space Mono', monospace;
            font-size: 15px;
            font-weight: 700;
            color: var(--pink-hot);
            margin-bottom: 14px;
        }
        .player-actions {
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 10px;
            margin-bottom: 14px;
        }
        .btn-mini {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            font-family: 'Space Mono', monospace;
            font-size: 13px;
            font-weight: 700;
            padding: 8px 14px;
            border: 2.5px solid var(--ink);
            border-radius: 12px;
            box-shadow: 3px 3px 0px var(--ink);
            background: var(--yellow);
            color: var(--ink);
            text-decoration: none;
            cursor: pointer;
        }
        .btn-mini:hover { transform: translate(-1px, -1px); }
        .btn-mini.secondary { background: var(--cream); }
        .btn-mini.spotify-link { background: var(--mint); }

        .scrubber-row {
            display: flex;
            align-items: center;
            gap: 12px;
            font-family: 'Space Mono', monospace;
            font-size: 13px;
            font-weight: 700;
        }
        .scrubber-track {
            flex: 1;
            height: 18px;
            background: var(--cream);
            border: 2.5px solid var(--ink);
            border-radius: 999px;
            overflow: hidden;
            position: relative;
        }
        .scrubber-fill {
            height: 100%;
            width: 0%;
            background: repeating-linear-gradient(
                -45deg,
                var(--pink-hot),
                var(--pink-hot) 10px,
                var(--pink) 10px,
                var(--pink) 20px
            );
            transition: width 0.45s linear;
        }

        /* SELETOR DE MÚSICA DO DIÁRIO PARA EXPLORAR QUALQUER FAIXA */
        .diary-switcher {
            background: var(--cream);
            border: 3px solid var(--ink);
            border-radius: 20px;
            padding: 16px 20px;
            box-shadow: var(--shadow);
            margin-bottom: 24px;
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
        }
        .diary-switcher-label {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 700;
            font-size: 20px;
        }
        .track-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .track-chip {
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            padding: 6px 12px;
            border: 2px solid var(--ink);
            border-radius: 12px;
            background: var(--paper);
            color: var(--ink);
            cursor: pointer;
            box-shadow: 2px 2px 0px var(--ink);
        }
        .track-chip.active {
            background: var(--yellow);
        }

        /* ABAS PRINCIPAIS DA MATÉRIA (PÁGINA 01, 02, 03) */
        .issue-tabs {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-bottom: 22px;
        }
        .issue-tab-btn {
            background: var(--cream);
            border: 3px solid var(--ink);
            border-radius: 18px;
            padding: 15px 16px;
            text-align: left;
            cursor: pointer;
            box-shadow: var(--shadow-sm);
            transition: transform 0.12s ease, background 0.12s ease;
        }
        .issue-tab-btn:hover { transform: translate(-2px, -2px); }
        .issue-tab-num {
            display: block;
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--pink-hot);
            margin-bottom: 3px;
        }
        .issue-tab-title {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 700;
            font-size: 22px;
            color: var(--ink);
        }
        .issue-tab-btn.active[data-page="tab-letra"] {
            background: var(--mint);
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px var(--ink);
        }
        .issue-tab-btn.active[data-page="tab-curiosidades"] {
            background: var(--pink);
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px var(--ink);
        }
        .issue-tab-btn.active[data-page="tab-psicologia"] {
            background: var(--yellow);
            transform: translate(2px, 2px);
            box-shadow: 2px 2px 0px var(--ink);
        }

        .page-panel {
            display: none;
        }
        .page-panel.active {
            display: block;
        }

        /* CAIXAS EDITORIAIS E DIAGRAMAS ASSIMÉTRICOS */
        .mag-box {
            background: var(--cream);
            border: 3.5px solid var(--ink);
            border-radius: 24px;
            padding: 24px 26px;
            box-shadow: var(--shadow);
            position: relative;
            margin-bottom: 24px;
        }
        .mag-box-pink { background: var(--pink-soft); }
        .mag-box-mint { background: #EFFAF3; }
        .mag-box-yellow { background: var(--yellow-soft); }

        .box-head {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding-bottom: 12px;
            margin-bottom: 18px;
            border-bottom: 2.5px solid var(--ink);
        }
        .box-heading {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: 28px;
            color: var(--ink);
        }

        .two-col-editorial {
            display: grid;
            grid-template-columns: 1.35fr 0.9fr;
            gap: 24px;
            align-items: start;
        }

        /* PÁGINA 01 — LETRA E TRADUÇÃO (SEM NEGRITO FORÇADO, ESTROFES CLARAS) */
        .lyrics-toolbar {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 16px;
        }
        .mode-btn {
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            padding: 7px 13px;
            border: 2.5px solid var(--ink);
            border-radius: 12px;
            background: var(--cream);
            color: var(--ink);
            cursor: pointer;
            box-shadow: 2px 2px 0px var(--ink);
        }
        .mode-btn.active { background: var(--yellow); }

        .lyrics-sheet {
            background: #FFFFFF;
            border: 2.5px solid var(--ink);
            border-radius: 18px;
            padding: 26px 28px;
            font-family: 'Quicksand', sans-serif;
            font-size: 21px;
            font-weight: 500;
            line-height: 2.05;
            color: var(--ink);
            white-space: pre-line;
        }
        .lyrics-sheet b, .lyrics-sheet strong {
            font-weight: 700;
        }

        /* PÁGINA 02 — CURIOSIDADES E BASTIDORES */
        .gossip-note {
            background: #FFFFFF;
            border: 3px solid var(--ink);
            border-radius: 18px;
            padding: 20px 22px;
            margin-bottom: 16px;
            box-shadow: 4px 4px 0px var(--pink);
            font-size: 18px;
            font-weight: 500;
            line-height: 1.8;
            color: var(--ink);
        }

        /* PÁGINA 03 — ANÁLISE PSICOLÓGICA (COLUNA EDITORIAL, SEM NEGRITO NO CORPO INTEIRO) */
        .psych-column {
            background: #FFFFFF;
            border: 3px solid var(--ink);
            border-radius: 20px;
            padding: 28px 30px;
            box-shadow: 5px 5px 0px var(--yellow);
            font-size: 19px;
            font-weight: 500;
            line-height: 1.9;
            color: var(--ink);
        }
        .psych-column p {
            margin-bottom: 16px;
        }

        /* COLAGENS, POLAROIDS, CDs, FONES E ADESIVOS (SEM IMAGENS INVENTADAS OU QUEBRADAS) */
        .collage-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 18px;
            margin-top: 8px;
        }
        .collage-card {
            background: #FFFFFF;
            border: 3px solid var(--ink);
            border-radius: 18px;
            padding: 14px;
            box-shadow: 4px 4px 0px var(--ink);
        }
        .collage-card.tilt-l { transform: rotate(-1.5deg); }
        .collage-card.tilt-r { transform: rotate(1.5deg); }

        .visual-slot {
            border: 2.5px dashed var(--ink);
            border-radius: 14px;
            min-height: 165px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
            background: linear-gradient(145deg, var(--pink-soft), var(--yellow-soft));
            position: relative;
        }
        .visual-slot img.real-media {
            width: 100%;
            max-height: 230px;
            object-fit: cover;
            border-radius: 10px;
            border: 2px solid var(--ink);
        }
        .cd-disc {
            width: 84px;
            height: 84px;
            border-radius: 50%;
            border: 3px solid var(--ink);
            background: conic-gradient(var(--pink), var(--yellow), var(--mint), var(--pink));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 10px;
            box-shadow: 3px 3px 0px var(--ink);
        }
        .cd-hole {
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: var(--cream);
            border: 2.5px solid var(--ink);
        }
        .slot-label {
            font-family: 'Space Mono', monospace;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            background: var(--cream);
            border: 2px solid var(--ink);
            border-radius: 8px;
            padding: 3px 9px;
            margin-bottom: 8px;
        }
        .slot-title {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 700;
            font-size: 19px;
            color: var(--ink);
        }
        .slot-caption {
            font-family: 'Caveat', cursive;
            font-size: 22px;
            font-weight: 700;
            color: var(--ink-soft);
            margin-top: 8px;
            line-height: 1.2;
        }

        /* QUADROS EDITORIAIS EXTRAS COM FORMATOS DIFERENTES */
        .editorial-extras-grid {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 22px;
            margin-top: 24px;
        }
        .frame-letter {
            background: var(--cream);
            border: 3px solid var(--ink);
            border-radius: 6px 24px 18px 24px;
            padding: 22px;
            box-shadow: var(--shadow);
        }
        .frame-speech {
            background: var(--pink-soft);
            border: 3px solid var(--ink);
            border-radius: 26px 26px 26px 4px;
            padding: 22px;
            box-shadow: var(--shadow);
        }
        .frame-vibe {
            background: var(--yellow-soft);
            border: 3px solid var(--ink);
            border-radius: 22px;
            padding: 22px;
            box-shadow: var(--shadow);
        }
        .frame-tape {
            background: #EFFAF3;
            border: 3px dashed var(--ink);
            border-radius: 18px;
            padding: 22px;
            box-shadow: var(--shadow-sm);
        }
        .frame-quote {
            grid-column: 1 / -1;
            background: linear-gradient(90deg, var(--pink-soft), var(--cream), var(--yellow-soft));
            border: 3.5px solid var(--ink);
            border-radius: 24px;
            padding: 26px;
            box-shadow: var(--shadow-lg);
            text-align: center;
        }
        .quote-big {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-size: clamp(24px, 3.5vw, 34px);
            font-weight: 700;
            color: var(--ink);
            margin: 10px 0;
        }
        .quadro-title {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: 22px;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .vibe-tags {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .vibe-chip {
            background: #FFFFFF;
            border: 2px solid var(--ink);
            border-radius: 999px;
            padding: 4px 12px;
            font-size: 13px;
            font-weight: 700;
        }
        .checklist-teen {
            list-style: none;
            margin-top: 8px;
        }
        .checklist-teen li {
            padding: 6px 0;
            border-bottom: 1.5px dotted var(--ink);
            font-size: 16px;
            font-weight: 600;
        }
        .checklist-teen li:last-child { border-bottom: none; }

        .rec-cards-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 12px;
        }
        .rec-mini-card {
            background: #FFFFFF;
            border: 2.5px solid var(--ink);
            border-radius: 16px;
            padding: 14px;
            box-shadow: 3px 3px 0px var(--ink);
            cursor: pointer;
        }
        .rec-mini-card:hover { background: var(--yellow-soft); }

        .rating-stars {
            font-family: 'Space Mono', monospace;
            font-size: 18px;
            font-weight: 700;
            background: #FFFFFF;
            display: inline-block;
            padding: 6px 14px;
            border: 2.5px solid var(--ink);
            border-radius: 12px;
            margin: 8px 0 12px;
        }

        .reader-box textarea {
            width: 100%;
            min-height: 92px;
            border: 2.5px solid var(--ink);
            border-radius: 14px;
            padding: 12px;
            font-family: 'Quicksand', sans-serif;
            font-size: 16px;
            font-weight: 600;
            background: #FFFFFF;
            color: var(--ink);
            margin-top: 10px;
        }
        .reader-notes-list {
            margin-top: 14px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }
        .reader-note-item {
            background: #FFFFFF;
            border: 2px solid var(--ink);
            border-radius: 12px;
            padding: 10px 14px;
            font-size: 15px;
            font-weight: 600;
        }

        /* SEÇÕES DO PORTAL (HOME, MÚSICAS, ARTISTAS, ÁLBUNS, PLAYLISTS, TESTES, SOBRE) */
        .home-grid {
            display: grid;
            grid-template-columns: 1.3fr 1fr;
            gap: 22px;
            margin-bottom: 24px;
        }
        .catalog-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
            gap: 16px;
            margin-top: 14px;
        }
        .catalog-card {
            background: #FFFFFF;
            border: 3px solid var(--ink);
            border-radius: 18px;
            padding: 16px;
            box-shadow: 4px 4px 0px var(--ink);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 10px;
        }
        .catalog-title {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 700;
            font-size: 22px;
            color: var(--ink);
        }
        .catalog-sub {
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            color: var(--pink-hot);
            text-transform: uppercase;
        }
        .quiz-option {
            display: block;
            width: 100%;
            text-align: left;
            background: #FFFFFF;
            border: 2.5px solid var(--ink);
            border-radius: 14px;
            padding: 12px 16px;
            margin-bottom: 10px;
            font-family: 'Quicksand', sans-serif;
            font-size: 16px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 3px 3px 0px var(--ink);
        }
        .quiz-option:hover { background: var(--pink-soft); }

        @media (max-width: 860px) {
            .player-main { grid-template-columns: 1fr; text-align: center; }
            .polaroid-frame { max-width: 210px; margin: 0 auto; }
            .player-status-row, .player-actions, .scrubber-row { justify-content: center; }
            .issue-tabs { grid-template-columns: 1fr; }
            .two-col-editorial, .home-grid, .collage-grid, .editorial-extras-grid, .rec-cards-row {
                grid-template-columns: 1fr;
            }
            .lyrics-sheet { font-size: 19px; padding: 20px; }
        }
    </style>
</head>
<body>
    <div class="mag-shell">
        <header class="masthead">
            <div class="tape tape-tl"></div>
            <div class="tape tape-tr"></div>
            <div class="masthead-strip">
                <div class="masthead-tags">
                    <span class="badge-tag tag-hot">★ HOT NEWS</span>
                    <span class="badge-tag tag-new">NEW MUSIC</span>
                    <span class="badge-tag tag-crush">CRUSH ALERT</span>
                    <span class="badge-tag tag-mint">GIRL TALK</span>
                </div>
                <div class="issue-meta">EDIÇÃO 2013–2014 • MUSIC DIARY</div>
            </div>

            <div class="logo-block">
                <div class="logo-kicker">diário secreto, letras, bastidores &amp; mente em 2013–2014</div>
                <h1 class="logo-main">XOXO My Music Diary</h1>
                <div class="logo-tagline">~* ON REPEAT • PLAY NOW • EXCLUSIVE • XOXO *~</div>
            </div>

            <nav class="portal-nav" aria-label="Navegação da revista">
                <button type="button" class="nav-pill active" data-sec="sec-home" onclick="irSecao('sec-home', this)">🏠 HOME</button>
                <button type="button" class="nav-pill" data-sec="sec-musicas" onclick="irSecao('sec-musicas', this)">🎵 MÚSICAS</button>
                <button type="button" class="nav-pill" data-sec="sec-artistas" onclick="irSecao('sec-artistas', this)">🎤 ARTISTAS</button>
                <button type="button" class="nav-pill" data-sec="sec-albuns" onclick="irSecao('sec-albuns', this)">💿 ÁLBUNS</button>
                <button type="button" class="nav-pill" data-sec="sec-playlists" onclick="irSecao('sec-playlists', this)">🎧 PLAYLISTS</button>
                <button type="button" class="nav-pill" data-sec="sec-testes" onclick="irSecao('sec-testes', this)">💌 TESTES</button>
                <button type="button" class="nav-pill" data-sec="sec-sobre" onclick="irSecao('sec-sobre', this)">📖 SOBRE A REVISTA</button>
            </nav>
        </header>

        <div class="ticker-bar">
            <marquee scrollamount="5">★ OMG! A sua revista musical de 2013–2014 está no ar ★ Folheie Letra &amp; Tradução, Curiosidades e Análise Psicológica ★ XOXO MUSIC DIARY ★ ON REPEAT ★</marquee>
        </div>

        <!-- SEÇÃO PRINCIPAL: HOME (PLAYER + MATÉRIA COMPLETA + VITRINE DA REVISTA) -->
        <section id="sec-home" class="portal-section active">
            {% if not logado %}
            <div class="auth-card">
                <span class="badge-tag tag-hot" style="margin-bottom:12px;">PLAY NOW • SPOTIFY</span>
                <h2>Conecte seu Spotify para abrir o diário ao vivo</h2>
                <p>Entre com a sua conta do Spotify para acompanhar o som do momento com letra, tradução, curiosidades, análise psicológica e quadros de revista teen. Você também pode explorar as matérias cadastradas no catálogo abaixo.</p>
                <a href="/login" class="btn-spotify">♪ Entrar com o Spotify</a>
            </div>
            {% else %}
            <div class="retro-player">
                <div class="player-top-badges">
                    <span class="badge-tag tag-new">ON REPEAT • PLAYER DO DIÁRIO</span>
                    <span class="badge-tag tag-mint" id="spotify-account-tag">SESSÃO ISOLADA ATIVA</span>
                </div>
                <div class="player-main">
                    <div class="polaroid-frame">
                        <img id="album-img" src="" alt="Capa da faixa atual" style="display:none;">
                        <div id="album-placeholder-slot" class="visual-slot" style="min-height:145px; padding:10px;">
                            <div class="cd-disc"><div class="cd-hole"></div></div>
                            <div class="slot-title" style="font-size:15px;">Capa ao dar play</div>
                        </div>
                        <div class="polaroid-caption" id="polaroid-caption">xoxo • agora no som</div>
                    </div>

                    <div>
                        <div class="player-status-row">
                            <span class="status-pill" id="status-badge">● AGUARDANDO PLAY</span>
                            <span class="badge-tag tag-crush" id="source-badge">DIÁRIO / SPOTIFY</span>
                        </div>
                        <div class="now-track-title" id="track-title">Dê o play em uma música no Spotify</div>
                        <div class="now-track-artist" id="track-artist">ou escolha uma faixa do diário logo abaixo</div>

                        <div class="player-actions">
                            <button type="button" class="btn-mini" id="btn-toggle-play" onclick="alternarEstadoVisualPlayer()">❚❚ Pausar / Retomar</button>
                            <a id="spotify-open-link" href="https://open.spotify.com" target="_blank" rel="noopener" class="btn-mini spotify-link">♪ Ouvir no Spotify</a>
                            <span id="clipe-container"></span>
                        </div>

                        <div class="scrubber-row">
                            <span id="time-current">0:00</span>
                            <div class="scrubber-track">
                                <div class="scrubber-fill" id="progress-bar"></div>
                            </div>
                            <span id="time-total">0:00</span>
                        </div>
                    </div>
                </div>
            </div>
            {% endif %}

            <!-- SELETOR RÁPIDO DAS MÚSICAS DO DIÁRIO -->
            <div class="diary-switcher">
                <span class="diary-switcher-label">✂ Matérias no arquivo do diário:</span>
                <div class="track-chips" id="track-chips-container"></div>
            </div>

            <!-- 3 PÁGINAS PRINCIPAIS DA MATÉRIA -->
            <div class="issue-tabs" role="tablist">
                <button type="button" class="issue-tab-btn active" data-page="tab-letra" onclick="abrirPaginaMateria('tab-letra', this)">
                    <span class="issue-tab-num">PÁGINA 01 • ENCARTE</span>
                    <span class="issue-tab-title">♪ Letra e Tradução</span>
                </button>
                <button type="button" class="issue-tab-btn" data-page="tab-curiosidades" onclick="abrirPaginaMateria('tab-curiosidades', this)">
                    <span class="issue-tab-num">PÁGINA 02 • BASTIDORES</span>
                    <span class="issue-tab-title">✨ Curiosidades e Bastidores</span>
                </button>
                <button type="button" class="issue-tab-btn" data-page="tab-psicologia" onclick="abrirPaginaMateria('tab-psicologia', this)">
                    <span class="issue-tab-num">PÁGINA 03 • COLUNA</span>
                    <span class="issue-tab-title">🧠 Análise Psicológica</span>
                </button>
            </div>

            <!-- PÁGINA 01: LETRA E TRADUÇÃO -->
            <div id="tab-letra" class="page-panel active">
                <div class="mag-box mag-box-mint">
                    <div class="box-head">
                        <h2 class="box-heading">♪ Página 01 — Letra e Tradução</h2>
                        <span class="badge-tag tag-mint">ESTROFES &amp; LEITURA</span>
                    </div>
                    <div class="two-col-editorial">
                        <div>
                            <div class="lyrics-toolbar">
                                <button type="button" class="mode-btn active" id="btn-mode-pt" onclick="setLyricsMode('pt', this)">Tradução (PT-BR)</button>
                                <button type="button" class="mode-btn" id="btn-mode-orig" onclick="setLyricsMode('orig', this)">Referência Original</button>
                            </div>
                            <div id="lyrics-box" class="lyrics-sheet">Selecione uma música ou dê o play no Spotify para ler a tradução aqui.</div>
                        </div>
                        <div class="collage-grid">
                            <div class="collage-card tilt-l">
                                <div class="visual-slot">
                                    <span class="slot-label">ENCARTE • CD</span>
                                    <div class="cd-disc"><div class="cd-hole"></div></div>
                                    <div class="slot-title" id="collage-cd-title">Faixa em destaque</div>
                                    <div class="slot-caption">anote seus versos favoritos no caderno!</div>
                                </div>
                            </div>
                            <div class="collage-card tilt-r">
                                <div class="visual-slot">
                                    <span class="slot-label">FONES • ON REPEAT</span>
                                    <div style="font-size:38px; margin-bottom:6px;">🎧</div>
                                    <div class="slot-title">Modo Imersão</div>
                                    <div class="slot-caption">cada estrofe guarda uma cena inteira</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PÁGINA 02: CURIOSIDADES E BASTIDORES -->
            <div id="tab-curiosidades" class="page-panel">
                <div class="mag-box mag-box-pink">
                    <div class="box-head">
                        <h2 class="box-heading">✨ Página 02 — Curiosidades e Bastidores</h2>
                        <span class="badge-tag tag-hot">EXCLUSIVE • XOXO</span>
                    </div>
                    <div class="two-col-editorial">
                        <div id="gossip-box">As curiosidades e bastidores da faixa aparecem aqui.</div>
                        <div class="collage-grid">
                            <div class="collage-card tilt-r">
                                <div class="visual-slot">
                                    <span class="slot-label">RECORTE DE REVISTA</span>
                                    <div style="font-size:34px; margin-bottom:6px;">✂️📰</div>
                                    <div class="slot-title">Bastidores &amp; Referências</div>
                                    <div class="slot-caption">detalhes que só quem presta atenção nota!</div>
                                </div>
                            </div>
                            <div class="collage-card tilt-l">
                                <div class="visual-slot">
                                    <span class="slot-label">POLAROID • ESTÚDIO</span>
                                    <div style="font-size:34px; margin-bottom:6px;">📷✨</div>
                                    <div class="slot-title">Clima da Era</div>
                                    <div class="slot-caption">memórias de estúdio e estética pop</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- PÁGINA 03: ANÁLISE PSICOLÓGICA -->
            <div id="tab-psicologia" class="page-panel">
                <div class="mag-box mag-box-yellow">
                    <div class="box-head">
                        <h2 class="box-heading">🧠 Página 03 — Análise Psicológica</h2>
                        <span class="badge-tag tag-new">COLUNA DE MENTE</span>
                    </div>
                    <div id="psych-box" class="psych-column">A análise psicológica da faixa aparece aqui.</div>
                </div>
            </div>

            <!-- QUADROS EDITORIAIS EXTRAS COM IDENTIDADE VISUAL PRÓPRIA -->
            <div class="editorial-extras-grid">
                <article class="frame-speech">
                    <div class="quadro-title">💗 AFINAL, SOBRE O QUE É ESSA MÚSICA?</div>
                    <p id="quadro-sobre" style="font-size:17px; font-weight:600;"></p>
                </article>

                <article class="frame-letter">
                    <div class="quadro-title">👀 VOCÊ PERCEBEU?</div>
                    <p id="quadro-percebeu" style="font-size:17px; font-weight:600;"></p>
                </article>

                <article class="frame-vibe">
                    <div class="quadro-title">🎀 VIBE CHECK</div>
                    <p id="quadro-vibe-desc" style="font-size:16px; font-weight:600;"></p>
                    <div class="vibe-tags" id="quadro-vibe-tags"></div>
                </article>

                <article class="frame-tape">
                    <div class="quadro-title">💌 ESSA MÚSICA É PRA VOCÊ SE...</div>
                    <ul class="checklist-teen" id="quadro-pra-voce"></ul>
                </article>

                <article class="frame-letter">
                    <div class="quadro-title">📼 VOLTANDO NO TEMPO</div>
                    <p id="quadro-epoca" style="font-size:17px; font-weight:600;"></p>
                </article>

                <article class="frame-vibe">
                    <div class="quadro-title">⭐ NOTA DA REDAÇÃO</div>
                    <div class="rating-stars" id="quadro-nota-estrelas">★★★★★</div>
                    <p id="quadro-nota-texto" style="font-size:16px; font-weight:600;"></p>
                </article>

                <article class="frame-quote">
                    <span class="badge-tag tag-crush">💭 A FRASE QUE FICA</span>
                    <div class="quote-big" id="quadro-frase"></div>
                    <p id="quadro-frase-nota" style="font-size:16px; font-weight:600; max-width:780px; margin:0 auto;"></p>
                </article>

                <article class="frame-speech" style="grid-column: 1 / -1;">
                    <div class="quadro-title">🎧 SE VOCÊ GOSTOU DESSA...</div>
                    <p style="font-size:16px; font-weight:600;">Clique em outra faixa do diário para continuar a maratona:</p>
                    <div class="rec-cards-row" id="quadro-recomendacoes"></div>
                </article>

                <article class="frame-tape reader-box" style="grid-column: 1 / -1;">
                    <div class="quadro-title">💬 E VOCÊ?</div>
                    <p style="font-size:16px; font-weight:600;">Qual trecho bateu mais forte hoje? Escreva seu comentário no caderno da revista:</p>
                    <textarea id="reader-comment-input" placeholder="Escreva o que essa música fez você sentir..."></textarea>
                    <div style="margin-top:10px;">
                        <button type="button" class="btn-mini" onclick="salvarComentarioLeitora()">♥ Guardar no caderno</button>
                    </div>
                    <div class="reader-notes-list" id="reader-comments-list"></div>
                </article>
            </div>

            <!-- VITRINE HOME: ÚLTIMAS MÚSICAS, ARTISTAS, PLAYLISTS E TESTES -->
            <div class="home-grid" style="margin-top:26px;">
                <div class="mag-box">
                    <div class="box-head">
                        <h2 class="box-heading">★ Últimas Músicas &amp; Matérias</h2>
                        <span class="badge-tag tag-hot">ARQUIVO</span>
                    </div>
                    <div id="home-latest-list" style="display:flex; flex-direction:column; gap:10px;"></div>
                </div>

                <div class="mag-box mag-box-pink">
                    <div class="box-head">
                        <h2 class="box-heading">🎧 Playlists &amp; Clima</h2>
                        <span class="badge-tag tag-new">2013–2014</span>
                    </div>
                    <p style="font-size:16px; font-weight:600; margin-bottom:12px;">Escolha um mood para filtrar as músicas da revista:</p>
                    <div class="vibe-tags">
                        <button type="button" class="vibe-chip" onclick="irSecaoPorNome('sec-musicas')">Todas as músicas</button>
                        <button type="button" class="vibe-chip" onclick="irSecaoPorNome('sec-playlists')">Madrugada &amp; Intensidade</button>
                        <button type="button" class="vibe-chip" onclick="irSecaoPorNome('sec-testes')">Teste: Qual faixa é a sua cara?</button>
                    </div>
                </div>
            </div>
        </section>

        <!-- SEÇÃO MÚSICAS -->
        <section id="sec-musicas" class="portal-section">
            <div class="mag-box">
                <div class="box-head">
                    <h2 class="box-heading">🎵 Todas as Músicas do Diário</h2>
                    <span class="badge-tag tag-hot">CATÁLOGO</span>
                </div>
                <p style="font-size:17px; font-weight:600;">Clique em qualquer música para abrir a matéria completa com Letra &amp; Tradução, Curiosidades e Análise Psicológica.</p>
                <div class="catalog-grid" id="grid-musicas"></div>
            </div>
        </section>

        <!-- SEÇÃO ARTISTAS -->
        <section id="sec-artistas" class="portal-section">
            <div class="mag-box mag-box-pink">
                <div class="box-head">
                    <h2 class="box-heading">🎤 Artistas em Destaque</h2>
                    <span class="badge-tag tag-crush">SPOTLIGHT</span>
                </div>
                <div class="catalog-grid" id="grid-artistas"></div>
            </div>
        </section>

        <!-- SEÇÃO ÁLBUNS -->
        <section id="sec-albuns" class="portal-section">
            <div class="mag-box mag-box-mint">
                <div class="box-head">
                    <h2 class="box-heading">💿 Eras &amp; Álbuns</h2>
                    <span class="badge-tag tag-mint">ENCARTES</span>
                </div>
                <div class="catalog-grid" id="grid-albuns"></div>
            </div>
        </section>

        <!-- SEÇÃO PLAYLISTS -->
        <section id="sec-playlists" class="portal-section">
            <div class="mag-box mag-box-yellow">
                <div class="box-head">
                    <h2 class="box-heading">🎧 Playlists Temáticas da Redação</h2>
                    <span class="badge-tag tag-new">ON REPEAT</span>
                </div>
                <div class="catalog-grid" id="grid-playlists"></div>
            </div>
        </section>

        <!-- SEÇÃO TESTES -->
        <section id="sec-testes" class="portal-section">
            <div class="mag-box">
                <div class="box-head">
                    <h2 class="box-heading">💌 Teste da Revista: Qual é o seu Mood Musical?</h2>
                    <span class="badge-tag tag-hot">GIRL TALK</span>
                </div>
                <p style="font-size:17px; font-weight:600; margin-bottom:14px;">Responda como numa página clássica de revista teen para descobrir uma indicação do diário:</p>
                <button type="button" class="quiz-option" onclick="mostrarResultadoTeste('intensidade')">A) Tô vivendo tudo no limite, sem meio-termo e com o coração acelerado.</button>
                <button type="button" class="quiz-option" onclick="mostrarResultadoTeste('saudade')">B) Tô naquela saudade de madrugada pensando no que ficou pra trás.</button>
                <button type="button" class="quiz-option" onclick="mostrarResultadoTeste('entrega')">C) Tô pronta pra baixar a guarda e me entregar de verdade.</button>
                <div id="quiz-resultado" class="gossip-note" style="display:none; margin-top:14px;"></div>
            </div>
        </section>

        <!-- SEÇÃO SOBRE A REVISTA -->
        <section id="sec-sobre" class="portal-section">
            <div class="mag-box mag-box-pink">
                <div class="box-head">
                    <h2 class="box-heading">📖 Sobre a XOXO My Music Diary</h2>
                    <span class="badge-tag tag-hot">XOXO</span>
                </div>
                <p style="font-size:18px; font-weight:600; margin-bottom:14px;">A XOXO My Music Diary reúne a nostalgia das revistas adolescentes de 2013–2014, o clima afetivo dos blogs e do Tumblr e um olhar cuidadoso sobre letras, bastidores e psicologia das canções.</p>
                <p style="font-size:17px; font-weight:500;">Cada música cadastrada no código ou nos arquivos JSON da pasta <code>musicas_extras/</code> preserva integralmente seus textos originais de tradução, curiosidades e análise psicológica.</p>
            </div>
        </section>
    </div>

    <script>
        const CATALOGO_MANUAL = {{ catalogo_json | safe }};
        const CHAVES_CATALOGO = Object.keys(CATALOGO_MANUAL);

        let currentTrackId = null;
        let selectedManualKey = CHAVES_CATALOGO[0] || null;
        let currentLyricsPt = "";
        let currentLyricsOrig = "";
        let lyricsMode = "pt";
        let visualPaused = false;

        function normalizarChave(txt) {
            if (!txt) return "";
            return txt.toLowerCase().replace(/[’‘´`]/g, "'").trim();
        }

        function encontrarChaveCatalogo(titulo) {
            const norm = normalizarChave(titulo);
            if (!norm) return null;
            if (CATALOGO_MANUAL[norm]) return norm;
            const limpo = norm.split("(")[0].split(" - ")[0].trim();
            if (CATALOGO_MANUAL[limpo]) return limpo;
            for (const ch of CHAVES_CATALOGO) {
                if (norm.includes(ch)) return ch;
            }
            return null;
        }

        function irSecao(secId, btn) {
            document.querySelectorAll('.portal-section').forEach(s => s.classList.remove('active'));
            document.querySelectorAll('.nav-pill').forEach(b => b.classList.remove('active'));
            const alvo = document.getElementById(secId);
            if (alvo) alvo.classList.add('active');
            if (btn) btn.classList.add('active');
        }

        function irSecaoPorNome(secId) {
            const btn = document.querySelector(`.nav-pill[data-sec="${secId}"]`);
            irSecao(secId, btn);
        }

        function abrirPaginaMateria(pageId, btn) {
            document.querySelectorAll('.page-panel').forEach(p => p.classList.remove('active'));
            document.querySelectorAll('.issue-tab-btn').forEach(b => b.classList.remove('active'));
            const alvo = document.getElementById(pageId);
            if (alvo) alvo.classList.add('active');
            if (btn) btn.classList.add('active');
        }

        function setLyricsMode(mode, btn) {
            lyricsMode = mode;
            document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
            if (btn) btn.classList.add('active');
            renderLyricsSheet();
        }

        function renderLyricsSheet() {
            const box = document.getElementById('lyrics-box');
            if (!box) return;
            if (lyricsMode === 'pt') {
                box.textContent = currentLyricsPt || "Tradução não cadastrada para esta faixa.";
            } else {
                box.textContent = currentLyricsOrig || currentLyricsPt || "Letra original não disponível.";
            }
        }

        function formatTime(ms) {
            const totalSec = Math.max(0, Math.floor((ms || 0) / 1000));
            const min = Math.floor(totalSec / 60);
            const sec = totalSec % 60;
            return min + ":" + (sec < 10 ? "0" : "") + sec;
        }

        function alternarEstadoVisualPlayer() {
            visualPaused = !visualPaused;
            const badge = document.getElementById('status-badge');
            if (badge && visualPaused) {
                badge.textContent = "❚❚ PAUSADO NA TELA";
            }
        }

        function extrairTrechoDestaque(texto) {
            if (!texto) return "“Cada verso guarda um sentimento que a gente nem sempre sabe dizer em voz alta.”";
            const limpo = texto.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
            const linhas = texto.split(/\r?\n/).map(l => l.trim()).filter(Boolean);
            if (linhas.length > 0) {
                const amostra = linhas.slice(0, 2).join(" / ");
                return "“" + amostra.slice(0, 130) + (amostra.length > 130 ? "..." : "") + "”";
            }
            return "“" + limpo.slice(0, 120) + "...”";
        }

        function renderQuadrosEditoriais(titulo, artista, dadosFaixa) {
            const letra = (dadosFaixa && dadosFaixa.letra_limpa) ? dadosFaixa.letra_limpa : "";
            const curiosidades = (dadosFaixa && Array.isArray(dadosFaixa.curiosidades_lista)) ? dadosFaixa.curiosidades_lista : [];
            const psicologia = (dadosFaixa && dadosFaixa.psicologia) ? dadosFaixa.psicologia.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim() : "";

            const sobreEl = document.getElementById('quadro-sobre');
            if (sobreEl) {
                sobreEl.textContent = curiosidades.length > 0
                    ? curiosidades[0].replace(/<[^>]+>/g, "")
                    : `“${titulo}” (${artista}) traz uma narrativa marcante que mistura emoção, atmosfera sonora e identificação imediata.`;
            }

            const percEl = document.getElementById('quadro-percebeu');
            if (percEl) {
                percEl.textContent = curiosidades.length > 1
                    ? curiosidades[1].replace(/<[^>]+>/g, "")
                    : (curiosidades.length === 1
                        ? `Repare na construção da letra e nos contrastes de ritmo de “${titulo}” — cada repetição reforça o estado emocional da cena.`
                        : `Observe como o refrão e os arranjos de “${titulo}” intensificam a mensagem principal ao longo da faixa.`);
            }

            const vibeDesc = document.getElementById('quadro-vibe-desc');
            const vibeTags = document.getElementById('quadro-vibe-tags');
            if (vibeDesc) {
                vibeDesc.textContent = psicologia
                    ? psicologia.slice(0, 190) + (psicologia.length > 190 ? "..." : "")
                    : `Atmosfera envolvente de ${artista}, ideal para ouvir com calma ou no repeat.`;
            }
            if (vibeTags) {
                vibeTags.innerHTML = [
                    `<span class="vibe-chip">♪ ${artista}</span>`,
                    `<span class="vibe-chip">♥ Mood 2013–2014</span>`,
                    `<span class="vibe-chip">✨ On Repeat</span>`
                ].join("");
            }

            const praVoce = document.getElementById('quadro-pra-voce');
            if (praVoce) {
                praVoce.innerHTML = [
                    `<li>★ Você precisa de trilha sonora pra organizar o que tá sentindo agora.</li>`,
                    `<li>★ Gosta de letras que falam de vínculos, escolhas e intensidade.</li>`,
                    `<li>★ Curte descobrir bastidores e o lado psicológico por trás do som.</li>`
                ].join("");
            }

            const epocaEl = document.getElementById('quadro-epoca');
            if (epocaEl) {
                epocaEl.textContent = `No universo musical e de blogs/revistas teen que inspiram o diário, “${titulo}” (${artista}) ganha espaço especial pela força da interpretação e pela conexão com o público.`;
            }

            const notaTexto = document.getElementById('quadro-nota-texto');
            if (notaTexto) {
                notaTexto.textContent = `Letra, atmosfera e entrega emocional de “${titulo}” rendem destaque na redação do XOXO My Music Diary.`;
            }

            const fraseEl = document.getElementById('quadro-frase');
            const fraseNota = document.getElementById('quadro-frase-nota');
            if (fraseEl) fraseEl.textContent = extrairTrechoDestaque(letra);
            if (fraseNota) fraseNota.textContent = `Trecho em destaque de “${titulo}” — ${artista}.`;

            const recRow = document.getElementById('quadro-recomendacoes');
            if (recRow) {
                const outras = CHAVES_CATALOGO.filter(k => k !== normalizarChave(titulo)).slice(0, 3);
                recRow.innerHTML = outras.map(k => {
                    const item = CATALOGO_MANUAL[k];
                    return `<div class="rec-mini-card" onclick="selecionarMusicaDoCatalogo('${k.replace(/'/g, "\\'")}')">
                        <div class="catalog-sub">${item.artista || "Artista"}</div>
                        <div class="catalog-title" style="font-size:18px;">${k}</div>
                    </div>`;
                }).join("");
            }
        }

        function aplicarConteudoMateria(titulo, artista, dados) {
            currentLyricsPt = (dados && dados.letra_limpa) ? dados.letra_limpa : "Letra não encontrada para esta faixa.";
            currentLyricsOrig = (dados && dados.letra_original) ? dados.letra_original : "";
            renderLyricsSheet();

            const gossipBox = document.getElementById('gossip-box');
            if (gossipBox) {
                const lista = (dados && Array.isArray(dados.curiosidades_lista) && dados.curiosidades_lista.length > 0)
                    ? dados.curiosidades_lista
                    : [`<b>BASTIDORES DO DIÁRIO:</b><br>Faixa <b>${titulo}</b> de <b>${artista}</b> em destaque no player.`];
                gossipBox.innerHTML = lista.map(txt => `<div class="gossip-note">${txt}</div>`).join("");
            }

            const psychBox = document.getElementById('psych-box');
            if (psychBox) {
                const textoPsico = (dados && dados.psicologia)
                    ? dados.psicologia
                    : `<b>ANÁLISE PSICOLÓGICA — ${titulo.toUpperCase()}</b><br><br>Observe as emoções, memórias e reações despertadas por esta canção durante a escuta.`;
                const blocos = textoPsico.split(/<br\s*\/?>\s*<br\s*\/?>|\n\s*\n/).filter(b => b.trim());
                psychBox.innerHTML = blocos.map(b => `<p>${b.trim()}</p>`).join("");
            }

            const cdTitle = document.getElementById('collage-cd-title');
            if (cdTitle) cdTitle.textContent = `${titulo} — ${artista}`;

            const clipeSpan = document.getElementById('clipe-container');
            if (clipeSpan) {
                const linkClipe = dados && dados.link_clipe;
                clipeSpan.innerHTML = linkClipe
                    ? `<a href="${linkClipe}" target="_blank" rel="noopener" class="btn-mini secondary">▶ Clipe Oficial</a>`
                    : "";
            }

            renderQuadrosEditoriais(titulo, artista, dados);
        }

        function selecionarMusicaDoCatalogo(chave) {
            const dados = CATALOGO_MANUAL[chave];
            if (!dados) return;
            selectedManualKey = chave;
            document.querySelectorAll('.track-chip').forEach(c => {
                c.classList.toggle('active', c.dataset.key === chave);
            });
            const titleEl = document.getElementById('track-title');
            const artistEl = document.getElementById('track-artist');
            const srcBadge = document.getElementById('source-badge');
            const capEl = document.getElementById('polaroid-caption');
            if (titleEl) titleEl.textContent = chave;
            if (artistEl) artistEl.textContent = dados.artista || "Artista do Diário";
            if (srcBadge) srcBadge.textContent = "MATÉRIA DO DIÁRIO";
            if (capEl) capEl.textContent = chave;
            aplicarConteudoMateria(chave, dados.artista || "Artista", dados);
            irSecaoPorNome('sec-home');
        }

        function montarCatalogoVisual() {
            const chipsContainer = document.getElementById('track-chips-container');
            const gridMusicas = document.getElementById('grid-musicas');
            const latestHome = document.getElementById('home-latest-list');
            const gridArtistas = document.getElementById('grid-artistas');
            const gridAlbuns = document.getElementById('grid-albuns');
            const gridPlaylists = document.getElementById('grid-playlists');

            if (chipsContainer) {
                chipsContainer.innerHTML = CHAVES_CATALOGO.slice(0, 12).map((ch, idx) =>
                    `<button type="button" class="track-chip ${idx === 0 ? 'active' : ''}" data-key="${ch.replace(/"/g, '&quot;')}" onclick="selecionarMusicaDoCatalogo('${ch.replace(/'/g, "\\'")}')">${ch}</button>`
                ).join("");
            }

            if (gridMusicas) {
                gridMusicas.innerHTML = CHAVES_CATALOGO.map(ch => {
                    const info = CATALOGO_MANUAL[ch];
                    return `<div class="catalog-card">
                        <div>
                            <div class="catalog-sub">${info.artista || "Artista"}</div>
                            <div class="catalog-title">${ch}</div>
                        </div>
                        <button type="button" class="btn-mini" onclick="selecionarMusicaDoCatalogo('${ch.replace(/'/g, "\\'")}')">Abrir matéria →</button>
                    </div>`;
                }).join("");
            }

            if (latestHome) {
                latestHome.innerHTML = CHAVES_CATALOGO.slice(0, 6).map(ch => {
                    const info = CATALOGO_MANUAL[ch];
                    return `<div class="reader-note-item" style="display:flex; justify-content:space-between; align-items:center; gap:10px;">
                        <span><b>${ch}</b> — ${info.artista || ""}</span>
                        <button type="button" class="btn-mini secondary" onclick="selecionarMusicaDoCatalogo('${ch.replace(/'/g, "\\'")}')">Ler</button>
                    </div>`;
                }).join("");
            }

            const artistasUnicos = [...new Set(CHAVES_CATALOGO.map(ch => (CATALOGO_MANUAL[ch].artista || "").trim()).filter(Boolean))];
            if (gridArtistas) {
                gridArtistas.innerHTML = artistasUnicos.map(art => {
                    const faixasArt = CHAVES_CATALOGO.filter(ch => (CATALOGO_MANUAL[ch].artista || "").trim() === art);
                    return `<div class="catalog-card">
                        <div>
                            <div class="catalog-sub">ARTISTA • ${faixasArt.length} FAIXA(S)</div>
                            <div class="catalog-title">${art}</div>
                        </div>
                        <button type="button" class="btn-mini" onclick="selecionarMusicaDoCatalogo('${faixasArt[0].replace(/'/g, "\\'")}')">Ver faixa em destaque</button>
                    </div>`;
                }).join("");
            }

            if (gridAlbuns) {
                gridAlbuns.innerHTML = [
                    { nome: "Mind of Mine & Eras Solo", sub: "ENCARTE ESPECIAL", faixa: "pillowtalk" },
                    { nome: "Icarus Falls & Baladas", sub: "EDIÇÃO DO DIÁRIO", faixa: "common" },
                    { nome: "Trilhas & Bastidores", sub: "COLEÇÃO 2013–2014", faixa: "who" }
                ].filter(a => CATALOGO_MANUAL[a.faixa]).map(a =>
                    `<div class="catalog-card">
                        <div>
                            <div class="catalog-sub">${a.sub}</div>
                            <div class="catalog-title">${a.nome}</div>
                        </div>
                        <button type="button" class="btn-mini" onclick="selecionarMusicaDoCatalogo('${a.faixa}')">Explorar álbum</button>
                    </div>`
                ).join("");
            }

            if (gridPlaylists) {
                gridPlaylists.innerHTML = [
                    { nome: "Noite & Intensidade", sub: "PLAYLIST DA REDAÇÃO", faixa: "bordersz" },
                    { nome: "Saudade & Madrugada", sub: "DIÁRIO DE BORDO", faixa: "it's you" },
                    { nome: "Entrega & Descoberta", sub: "ON REPEAT", faixa: "natural" }
                ].filter(p => CATALOGO_MANUAL[p.faixa]).map(p =>
                    `<div class="catalog-card">
                        <div>
                            <div class="catalog-sub">${p.sub}</div>
                            <div class="catalog-title">${p.nome}</div>
                        </div>
                        <button type="button" class="btn-mini" onclick="selecionarMusicaDoCatalogo('${p.faixa}')">Ouvir / Ler matéria</button>
                    </div>`
                ).join("");
            }

            if (selectedManualKey && CATALOGO_MANUAL[selectedManualKey]) {
                selecionarMusicaDoCatalogo(selectedManualKey);
            }
        }

        function mostrarResultadoTeste(perfil) {
            const box = document.getElementById('quiz-resultado');
            if (!box) return;
            box.style.display = 'block';
            if (perfil === 'intensidade') {
                box.innerHTML = "<b>RESULTADO DO TESTE:</b> Seu mood pede intensidade! Dê uma olhada na matéria de <b>bordersz</b> ou <b>befour</b>.";
            } else if (perfil === 'saudade') {
                box.innerHTML = "<b>RESULTADO DO TESTE:</b> Seu mood tá sensível e reflexivo! Confira as matérias de <b>it's you</b> ou <b>like i would</b>.";
            } else {
                box.innerHTML = "<b>RESULTADO DO TESTE:</b> Seu mood pede conexão e entrega! Veja a matéria de <b>natural</b> ou <b>common</b>.";
            }
        }

        function salvarComentarioLeitora() {
            const input = document.getElementById('reader-comment-input');
            const list = document.getElementById('reader-comments-list');
            if (!input || !list) return;
            const val = input.value.trim();
            if (!val) return;
            const div = document.createElement('div');
            div.className = 'reader-note-item';
            div.textContent = "♥ " + val;
            list.prepend(div);
            input.value = "";
        }

        async function atualizarSpotify() {
            const statusBadge = document.getElementById('status-badge');
            if (!statusBadge) return;
            try {
                const res = await fetch('/api/now-playing');
                if (res.status === 401) {
                    window.location.href = '/';
                    return;
                }
                const data = await res.json();
                if (data.playing) {
                    statusBadge.textContent = visualPaused ? "❚❚ PAUSADO NA TELA" : "● TOCANDO AGORA NO SPOTIFY";
                    const titleEl = document.getElementById('track-title');
                    const artistEl = document.getElementById('track-artist');
                    const srcBadge = document.getElementById('source-badge');
                    const spLink = document.getElementById('spotify-open-link');
                    const curTime = document.getElementById('time-current');
                    const totTime = document.getElementById('time-total');
                    const progBar = document.getElementById('progress-bar');

                    if (titleEl) titleEl.textContent = data.name;
                    if (artistEl) artistEl.textContent = data.artist;
                    if (srcBadge) srcBadge.textContent = "SPOTIFY AO VIVO";
                    if (spLink && data.spotify_url) spLink.href = data.spotify_url;
                    if (curTime) curTime.textContent = formatTime(data.progress);
                    if (totTime) totTime.textContent = formatTime(data.duration);
                    if (progBar && data.duration > 0) {
                        progBar.style.width = Math.min(100, (data.progress / data.duration) * 100) + "%";
                    }

                    if (data.id !== currentTrackId) {
                        currentTrackId = data.id;
                        const imgEl = document.getElementById('album-img');
                        const phSlot = document.getElementById('album-placeholder-slot');
                        const capEl = document.getElementById('polaroid-caption');
                        if (imgEl && data.image) {
                            imgEl.src = data.image;
                            imgEl.style.display = 'block';
                            if (phSlot) phSlot.style.display = 'none';
                        }
                        if (capEl) capEl.textContent = data.name;

                        const chaveMatch = encontrarChaveCatalogo(data.name);
                        const dadosEnriquecidos = chaveMatch ? {
                            ...CATALOGO_MANUAL[chaveMatch],
                            letra_limpa: data.lyrics || CATALOGO_MANUAL[chaveMatch].letra_limpa,
                            curiosidades_lista: (Array.isArray(data.gossip) && data.gossip.length) ? data.gossip : CATALOGO_MANUAL[chaveMatch].curiosidades_lista,
                            psicologia: data.psychology || CATALOGO_MANUAL[chaveMatch].psicologia,
                            link_clipe: data.clipe || CATALOGO_MANUAL[chaveMatch].link_clipe
                        } : {
                            artista: data.artist,
                            letra_limpa: data.lyrics,
                            curiosidades_lista: data.gossip,
                            psicologia: data.psychology,
                            link_clipe: data.clipe
                        };
                        aplicarConteudoMateria(data.name, data.artist, dadosEnriquecidos);
                    }
                } else {
                    statusBadge.textContent = "❚❚ SPOTIFY PAUSADO";
                }
            } catch (e) {
                console.log(e);
            }
        }

        montarCatalogoVisual();
        setInterval(atualizarSpotify, 1500);
        atualizarSpotify();
    </script>
</body>
</html>
"""


def _catalogo_serializavel():
    saida = {}
    for chave, info in MUSICAS_MANUAIS.items():
        saida[chave] = {
            "artista": info.get("artista", ""),
            "letra_limpa": info.get("letra_limpa", ""),
            "curiosidades_lista": info.get("curiosidades_lista", []),
            "psicologia": info.get("psicologia", ""),
            "link_clipe": info.get("link_clipe"),
        }
    return json.dumps(saida, ensure_ascii=False)


@app.route("/")
def index():
    sp = obter_cliente_spotify_usuario()
    return render_template_string(
        HTML_TEMPLATE,
        logado=bool(sp),
        catalogo_json=_catalogo_serializavel(),
    )


@app.route("/login")
def login():
    if "sid" not in session:
        session["sid"] = str(uuid.uuid4())
    auth_manager = criar_oauth()
    auth_url = auth_manager.get_authorize_url()
    return redirect(auth_url)


@app.route("/callback")
def callback():
    error = request.args.get("error")
    if error:
        return f"Erro ao autorizar no Spotify: {error}", 400

    code = request.args.get("code")
    if not code:
        return "Código de autorização não recebido.", 400

    auth_manager = criar_oauth()
    token_info = auth_manager.get_access_token(code, as_dict=True)
    session["spotify_token"] = token_info
    session.modified = True
    return redirect("/")


@app.route("/api/now-playing")
def now_playing():
    sp = obter_cliente_spotify_usuario()
    if not sp:
        return jsonify({"playing": False, "logged_out": True}), 401

    try:
        cur = sp.current_user_playing_track()
        if cur and cur.get("is_playing") and cur.get("item"):
            tr = cur["item"]
            tn = tr["name"]
            ar = tr["artists"][0]["name"]
            tid = tr["id"]
            imgs = tr.get("album", {}).get("images") or []
            img = imgs[0]["url"] if imgs else ""
            p = cur.get("progress_ms", 0)
            dur = tr.get("duration_ms", 1)
            sp_url = tr.get("external_urls", {}).get("spotify") or "https://open.spotify.com"

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
                "spotify_url": sp_url,
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
