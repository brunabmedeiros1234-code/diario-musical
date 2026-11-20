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
    <title>~* xoxo My Music Diary *~ • Revista Teen 2013–2014</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Caveat:wght@600;700&family=Playfair+Display:ital,wght@0,700;0,800;1,700;1,800&family=Quicksand:wght@500;600;700&family=Space+Mono:wght@400;700&family=VT323&display=swap" rel="stylesheet">
    <style>
        :root {
            --rosa: #FF7EB6;
            --rosa-forte: #D62872;
            --rosa-claro: #FFE6F1;
            --verde: #7CE0A8;
            --verde-escuro: #1F6E43;
            --amarelo: #FFE66D;
            --amarelo-claro: #FFF8C9;
            --lilas: #D8B4FE;
            --creme: #FFFDF9;
            --tinta: #141414;
            --sombra: 7px 7px 0px #141414;
            --sombra-alta: 11px 11px 0px #141414;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            width: 100%;
            min-height: 100vh;
            background-color: #DFF5E9;
            background-image:
                radial-gradient(#8ED0AC 2.4px, transparent 2.4px),
                radial-gradient(#F8A5C8 1.9px, transparent 1.9px);
            background-size: 30px 30px, 60px 60px;
            background-position: 0 0, 15px 15px;
            font-family: 'Quicksand', sans-serif;
            color: var(--tinta);
            padding: 18px 24px 80px;
            font-size: 18px;
        }

        .pagina-cheia {
            width: 100%;
            max-width: 100%;
        }

        /* CAPA DE REVISTA TEEN 2013-2014 EXPRESSIVA E COLORIDA */
        .capa-revista {
            width: 100%;
            background: linear-gradient(125deg, #FFB8D8 0%, #FFF2F8 36%, #FFF8C9 72%, #C9F5DC 100%);
            border: 4px solid var(--tinta);
            border-radius: 26px;
            padding: 20px 28px 18px;
            box-shadow: var(--sombra-alta);
            margin-bottom: 18px;
        }

        .faixa-selos {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 10px;
            padding-bottom: 12px;
            margin-bottom: 14px;
            border-bottom: 3px dashed var(--tinta);
        }
        .grupo-selos {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }
        .selo {
            display: inline-block;
            font-family: 'Space Mono', monospace;
            font-size: 12.5px;
            font-weight: 700;
            text-transform: uppercase;
            padding: 5px 12px;
            border: 2.5px solid var(--tinta);
            border-radius: 999px;
            box-shadow: 3px 3px 0px var(--tinta);
            background: var(--creme);
        }
        .selo-rosa { background: var(--rosa); color: var(--tinta); transform: rotate(-2deg); }
        .selo-amarelo { background: var(--amarelo); color: var(--tinta); transform: rotate(1.5deg); }
        .selo-verde { background: var(--verde); color: var(--tinta); transform: rotate(-1deg); }
        .selo-lilas { background: var(--lilas); color: var(--tinta); transform: rotate(2deg); }

        .capa-grade {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            gap: 22px;
        }
        .chamada-lateral {
            border: 3px solid var(--tinta);
            border-radius: 18px;
            padding: 14px 18px;
            box-shadow: 5px 5px 0px var(--tinta);
        }
        .chamada-lateral.esq {
            background: var(--rosa-claro);
            transform: rotate(-1.5deg);
        }
        .chamada-lateral.dir {
            background: var(--amarelo-claro);
            transform: rotate(1.5deg);
        }
        .chamada-rotulo {
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            color: var(--rosa-forte);
            text-transform: uppercase;
            margin-bottom: 4px;
        }
        .chamada-texto {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: 20px;
            line-height: 1.25;
        }

        .titulo-central {
            text-align: center;
        }
        .sobre-titulo {
            font-family: 'Caveat', cursive;
            font-size: 28px;
            font-weight: 700;
            color: var(--rosa-forte);
        }
        .titulo-principal {
            font-family: 'VT323', monospace;
            font-size: clamp(56px, 7.2vw, 96px);
            line-height: 0.94;
            color: var(--rosa-forte);
            text-shadow: 3px 3px 0px var(--amarelo), 6px 6px 0px var(--tinta);
            letter-spacing: 3px;
        }
        .sub-revista {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 700;
            font-size: 20px;
            color: var(--tinta);
            margin-top: 4px;
        }

        .barra-secoes {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            gap: 10px;
            margin-top: 16px;
            padding-top: 14px;
            border-top: 3px solid var(--tinta);
        }
        .btn-secao {
            flex: 1 1 130px;
            background: var(--creme);
            color: var(--tinta);
            border: 3px solid var(--tinta);
            border-radius: 15px;
            padding: 10px 12px;
            font-family: 'Space Mono', monospace;
            font-size: 13px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 4px 4px 0px var(--tinta);
            text-align: center;
        }
        .btn-secao:hover { background: var(--amarelo-claro); transform: translate(-1px, -1px); }
        .btn-secao.ativa { background: var(--rosa); box-shadow: 2px 2px 0px var(--tinta); }

        .letreiro-topo {
            width: 100%;
            background: var(--amarelo);
            border: 3.5px solid var(--tinta);
            border-radius: 999px;
            padding: 10px 22px;
            margin-bottom: 20px;
            box-shadow: var(--sombra);
            font-family: 'Space Mono', monospace;
            font-size: 14.5px;
            font-weight: 700;
            color: var(--tinta);
        }

        .secao-portal { display: none; width: 100%; }
        .secao-portal.ativa { display: block; }

        .caixa-login {
            width: 100%;
            background: var(--creme);
            border: 4px solid var(--tinta);
            border-radius: 26px;
            padding: 32px 28px;
            text-align: center;
            box-shadow: var(--sombra-alta);
            margin-bottom: 22px;
        }
        .caixa-login p {
            font-size: 20px;
            font-weight: 600;
            margin: 12px auto 20px;
            max-width: 960px;
        }
        .botao-spotify {
            display: inline-block;
            background: var(--verde-escuro);
            color: #FFFFFF;
            text-decoration: none;
            font-family: 'Space Mono', monospace;
            font-size: 19px;
            font-weight: 700;
            padding: 14px 28px;
            border: 3.5px solid var(--tinta);
            border-radius: 18px;
            box-shadow: var(--sombra);
        }

        /* PLAYER ESTILO BLOG ANTIGO OCUPANDO A LARGURA TODA */
        .player-blog {
            width: 100%;
            background: linear-gradient(95deg, #FFD4E8 0%, #FFFDF9 50%, #FFF2A6 100%);
            border: 4px solid var(--tinta);
            border-radius: 26px;
            padding: 22px 28px;
            box-shadow: var(--sombra-alta);
            margin-bottom: 20px;
            display: grid;
            grid-template-columns: 200px 1fr auto;
            gap: 26px;
            align-items: center;
        }
        .polaroid {
            background: #FFFFFF;
            border: 3px solid var(--tinta);
            border-radius: 14px;
            padding: 10px 10px 22px;
            box-shadow: 5px 5px 0px var(--tinta);
            transform: rotate(-2.5deg);
            text-align: center;
        }
        .polaroid img {
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
            border: 2.5px solid var(--tinta);
            border-radius: 10px;
            background: var(--creme);
        }
        .polaroid-legenda {
            font-family: 'Caveat', cursive;
            font-size: 22px;
            font-weight: 700;
            margin-top: 6px;
        }
        .badge-ao-vivo {
            display: inline-block;
            background: var(--verde-escuro);
            color: #FFFFFF;
            font-family: 'Space Mono', monospace;
            font-size: 13.5px;
            font-weight: 700;
            padding: 6px 14px;
            border-radius: 999px;
            border: 2.5px solid var(--tinta);
            margin-bottom: 10px;
        }
        .nome-faixa-player {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: clamp(28px, 3.8vw, 46px);
            line-height: 1.15;
            margin-bottom: 6px;
        }
        .artista-faixa-player {
            font-family: 'Space Mono', monospace;
            font-size: 16.5px;
            font-weight: 700;
            color: var(--rosa-forte);
            margin-bottom: 14px;
        }
        .controles-player {
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin-bottom: 14px;
        }
        .btn-acao {
            display: inline-block;
            font-family: 'Space Mono', monospace;
            font-size: 13.5px;
            font-weight: 700;
            padding: 9px 15px;
            border: 2.5px solid var(--tinta);
            border-radius: 13px;
            box-shadow: 3px 3px 0px var(--tinta);
            background: var(--amarelo);
            color: var(--tinta);
            text-decoration: none;
            cursor: pointer;
        }
        .btn-acao.verde { background: var(--verde); }
        .btn-acao.rosa { background: var(--rosa); }
        .btn-acao.branco { background: var(--creme); }

        .linha-progresso {
            display: flex;
            align-items: center;
            gap: 14px;
            font-family: 'Space Mono', monospace;
            font-size: 15px;
            font-weight: 700;
        }
        .trilho-progresso {
            flex: 1;
            height: 20px;
            background: #FFFFFF;
            border: 3px solid var(--tinta);
            border-radius: 999px;
            overflow: hidden;
        }
        .preenchimento-progresso {
            height: 100%;
            width: 0%;
            background: repeating-linear-gradient(-45deg, var(--rosa-forte), var(--rosa-forte) 10px, var(--rosa) 10px, var(--rosa) 20px);
            transition: width 0.45s linear;
        }

        .mini-colagem-lateral {
            display: flex;
            flex-direction: column;
            gap: 10px;
            width: 245px;
        }
        .adesivo-bloco {
            background: var(--creme);
            border: 3px solid var(--tinta);
            border-radius: 16px;
            padding: 11px 14px;
            box-shadow: 4px 4px 0px var(--tinta);
            font-weight: 700;
            font-size: 13.5px;
        }
        .adesivo-bloco.rot1 { transform: rotate(2deg); background: var(--amarelo); }
        .adesivo-bloco.rot2 { transform: rotate(-1.5deg); background: var(--verde); }
        .adesivo-bloco.rot3 { transform: rotate(1deg); background: var(--lilas); }

        .barra-musicas {
            width: 100%;
            background: var(--creme);
            border: 3.5px solid var(--tinta);
            border-radius: 22px;
            padding: 16px 22px;
            box-shadow: var(--sombra);
            margin-bottom: 20px;
        }
        .lista-chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }
        .chip-musica {
            font-family: 'Space Mono', monospace;
            font-size: 13px;
            font-weight: 700;
            padding: 7px 14px;
            border: 2.5px solid var(--tinta);
            border-radius: 12px;
            background: var(--rosa-claro);
            color: var(--tinta);
            cursor: pointer;
            box-shadow: 3px 3px 0px var(--tinta);
        }
        .chip-musica.ativa { background: var(--amarelo); }

        /* 3 ABAS PRINCIPAIS COM CORES VIVAS DE REVISTA */
        .abas-materia {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 16px;
            margin-bottom: 20px;
            width: 100%;
        }
        .aba-btn {
            background: var(--creme);
            border: 3.5px solid var(--tinta);
            border-radius: 20px;
            padding: 16px 20px;
            box-shadow: var(--sombra);
            cursor: pointer;
            text-align: left;
        }
        .aba-btn:hover { transform: translate(-2px, -2px); }
        .aba-rotulo {
            display: block;
            font-family: 'Space Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            color: var(--rosa-forte);
            margin-bottom: 4px;
        }
        .aba-titulo {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: 24px;
        }
        .aba-btn.ativa[data-aba="aba-01"] { background: var(--verde); box-shadow: 3px 3px 0px var(--tinta); transform: translate(2px, 2px); }
        .aba-btn.ativa[data-aba="aba-02"] { background: var(--rosa); box-shadow: 3px 3px 0px var(--tinta); transform: translate(2px, 2px); }
        .aba-btn.ativa[data-aba="aba-03"] { background: var(--amarelo); box-shadow: 3px 3px 0px var(--tinta); transform: translate(2px, 2px); }

        .conteudo-aba { display: none; width: 100%; }
        .conteudo-aba.ativa { display: block; }

        .caixa-revista {
            width: 100%;
            background: var(--creme);
            border: 4px solid var(--tinta);
            border-radius: 26px;
            padding: 26px 30px;
            box-shadow: var(--sombra-alta);
            margin-bottom: 22px;
        }
        .caixa-verde { background: #E9FBF0; }
        .caixa-rosa { background: #FFF0F7; }
        .caixa-amarela { background: #FFFBE0; }

        .cabecalho-caixa {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-between;
            align-items: center;
            gap: 12px;
            padding-bottom: 14px;
            margin-bottom: 20px;
            border-bottom: 3px solid var(--tinta);
        }
        .titulo-caixa {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: 30px;
        }

        .duas-colunas {
            display: grid;
            grid-template-columns: 1.55fr 1fr;
            gap: 26px;
            align-items: start;
        }

        /* LETRA E TRADUÇÃO: SEM NEGRITO NO TEXTO INTEIRO, BEM RESPIRO ENTRE ESTROFES */
        .folha-letra {
            background: #FFFFFF;
            border: 3px solid var(--tinta);
            border-radius: 20px;
            padding: 28px 32px;
            font-family: 'Quicksand', sans-serif;
            font-size: 22px;
            font-weight: 500;
            line-height: 2.05;
            color: var(--tinta);
            white-space: pre-line;
            box-shadow: 6px 6px 0px var(--verde);
        }

        .cartao-curiosidade {
            background: #FFFFFF;
            border: 3px solid var(--tinta);
            border-radius: 20px;
            padding: 22px 26px;
            margin-bottom: 16px;
            box-shadow: 6px 6px 0px var(--rosa);
            font-size: 20px;
            font-weight: 500;
            line-height: 1.85;
        }

        .coluna-psico {
            background: #FFFFFF;
            border: 3px solid var(--tinta);
            border-radius: 20px;
            padding: 28px 32px;
            box-shadow: 6px 6px 0px var(--amarelo);
            font-size: 20px;
            font-weight: 500;
            line-height: 1.9;
        }
        .coluna-psico p { margin-bottom: 16px; }

        .grade-colagem {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 16px;
        }
        .recorte-foto {
            background: #FFFFFF;
            border: 3px solid var(--tinta);
            border-radius: 18px;
            padding: 14px;
            box-shadow: 5px 5px 0px var(--tinta);
            text-align: center;
        }
        .recorte-foto.esq { transform: rotate(-1.8deg); }
        .recorte-foto.dir { transform: rotate(1.8deg); }
        .area-ilustracao {
            border: 2.5px dashed var(--tinta);
            border-radius: 14px;
            padding: 18px 12px;
            background: linear-gradient(135deg, #FFE4F0, #FFF6C2, #D5F7E3);
            min-height: 165px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .disco-cd {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            border: 3px solid var(--tinta);
            background: conic-gradient(var(--rosa), var(--amarelo), var(--verde), var(--lilas), var(--rosa));
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 8px;
        }
        .miolo-cd {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #FFFFFF;
            border: 2.5px solid var(--tinta);
        }
        .legenda-scrap {
            font-family: 'Caveat', cursive;
            font-size: 24px;
            font-weight: 700;
            margin-top: 8px;
        }

        /* QUADROS COLORIDOS ESPALHADOS PELA LARGURA DA REVISTA */
        .grade-quadros {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 22px;
            margin-top: 20px;
            width: 100%;
        }
        .quadro {
            border: 3.5px solid var(--tinta);
            border-radius: 22px;
            padding: 22px 24px;
            box-shadow: var(--sombra);
            background: var(--creme);
        }
        .quadro-rosa { background: #FFDDF0; border-radius: 26px 26px 26px 6px; }
        .quadro-amarelo { background: #FFF4B8; border-radius: 22px; }
        .quadro-verde { background: #DDF8E8; border: 3.5px dashed var(--tinta); }
        .quadro-lilas { background: #F1E2FF; border-radius: 8px 26px 20px 26px; }
        .quadro-destaque-largo {
            grid-column: 1 / -1;
            background: linear-gradient(95deg, #FFD4E8, #FFF8C9, #D7F8E5);
            border: 4px solid var(--tinta);
            border-radius: 26px;
            padding: 26px 30px;
            box-shadow: var(--sombra-alta);
            text-align: center;
        }
        .titulo-quadro {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: 24px;
            margin-bottom: 10px;
        }
        .frase-marcante {
            font-family: 'Playfair Display', serif;
            font-style: italic;
            font-weight: 800;
            font-size: clamp(24px, 3.4vw, 36px);
            margin: 10px 0;
        }
        .lista-situacoes {
            list-style: none;
            margin-top: 8px;
        }
        .lista-situacoes li {
            padding: 7px 0;
            border-bottom: 1.5px dotted var(--tinta);
            font-weight: 600;
            font-size: 17px;
        }
        .lista-situacoes li:last-child { border-bottom: none; }

        .grade-recs {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 14px;
            margin-top: 12px;
        }
        .card-rec {
            background: #FFFFFF;
            border: 2.5px solid var(--tinta);
            border-radius: 16px;
            padding: 14px;
            box-shadow: 3px 3px 0px var(--tinta);
            cursor: pointer;
        }
        .card-rec:hover { background: var(--amarelo-claro); }

        .grade-catalogo {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
            gap: 16px;
            margin-top: 14px;
        }
        .card-cat {
            background: #FFFFFF;
            border: 3px solid var(--tinta);
            border-radius: 18px;
            padding: 16px;
            box-shadow: 4px 4px 0px var(--tinta);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            gap: 10px;
        }
        .opcao-teste {
            display: block;
            width: 100%;
            text-align: left;
            background: #FFFFFF;
            border: 2.5px solid var(--tinta);
            border-radius: 14px;
            padding: 13px 16px;
            margin-bottom: 10px;
            font-family: 'Quicksand', sans-serif;
            font-size: 17px;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 3px 3px 0px var(--tinta);
        }
        .opcao-teste:hover { background: var(--rosa-claro); }

        textarea.campo-caderno {
            width: 100%;
            min-height: 90px;
            border: 2.5px solid var(--tinta);
            border-radius: 14px;
            padding: 12px;
            font-family: 'Quicksand', sans-serif;
            font-size: 17px;
            font-weight: 600;
            background: #FFFFFF;
            margin-top: 10px;
        }
        .nota-salva {
            background: #FFFFFF;
            border: 2.5px solid var(--tinta);
            border-radius: 12px;
            padding: 10px 14px;
            margin-top: 8px;
            font-weight: 600;
        }

        @media (max-width: 960px) {
            body { padding: 14px 12px 70px; }
            .capa-grade, .player-blog, .duas-colunas, .abas-materia, .grade-quadros, .grade-recs, .grade-colagem {
                grid-template-columns: 1fr;
            }
            .mini-colagem-lateral { width: 100%; }
            .polaroid { max-width: 220px; margin: 0 auto; }
        }
    </style>
</head>
<body>
    <div class="pagina-cheia">
        <header class="capa-revista">
            <div class="faixa-selos">
                <div class="grupo-selos">
                    <span class="selo selo-rosa">★ OMG!</span>
                    <span class="selo selo-amarelo">HOT NEWS</span>
                    <span class="selo selo-verde">NEW MUSIC</span>
                    <span class="selo selo-lilas">CRUSH ALERT</span>
                    <span class="selo selo-rosa">GIRL TALK</span>
                </div>
                <span class="selo selo-amarelo">MUSIC DIARY • 2013–2014</span>
            </div>

            <div class="capa-grade">
                <div class="chamada-lateral esq">
                    <div class="chamada-rotulo">EXCLUSIVE • ENCARTE</div>
                    <div class="chamada-texto">Letras traduzidas, bastidores secretos &amp; o que ninguém te contou</div>
                </div>

                <div class="titulo-central">
                    <div class="sobre-titulo">revista &amp; diário musical adolescente</div>
                    <h1 class="titulo-principal">~* xoxo My Music Diary *~</h1>
                    <div class="sub-revista">edição especial de som, sentimentos &amp; mente</div>
                </div>

                <div class="chamada-lateral dir">
                    <div class="chamada-rotulo">ON REPEAT • PLAY NOW</div>
                    <div class="chamada-texto">Coluna de psicologia, testes e o seu Spotify em tempo real</div>
                </div>
            </div>

            <nav class="barra-secoes" aria-label="Seções da revista">
                <button type="button" class="btn-secao ativa" data-sec="sec-home" onclick="abrirSecao('sec-home', this)">🏠 HOME</button>
                <button type="button" class="btn-secao" data-sec="sec-musicas" onclick="abrirSecao('sec-musicas', this)">🎵 MÚSICAS</button>
                <button type="button" class="btn-secao" data-sec="sec-artistas" onclick="abrirSecao('sec-artistas', this)">🎤 ARTISTAS</button>
                <button type="button" class="btn-secao" data-sec="sec-albuns" onclick="abrirSecao('sec-albuns', this)">💿 ÁLBUNS</button>
                <button type="button" class="btn-secao" data-sec="sec-playlists" onclick="abrirSecao('sec-playlists', this)">🎧 PLAYLISTS</button>
                <button type="button" class="btn-secao" data-sec="sec-testes" onclick="abrirSecao('sec-testes', this)">💌 TESTES</button>
                <button type="button" class="btn-secao" data-sec="sec-sobre" onclick="abrirSecao('sec-sobre', this)">📖 SOBRE A REVISTA</button>
            </nav>
        </header>

        <div class="letreiro-topo">
            <marquee scrollamount="5">★ XOXO • A sua revista musical estilo 2013–2014 ★ Folheie Letra &amp; Tradução, Curiosidades e Análise Psicológica ★ ON REPEAT ★ PLAY NOW ★</marquee>
        </div>

        <section id="sec-home" class="secao-portal ativa">
            {% if not logado %}
            <div class="caixa-login">
                <span class="selo selo-rosa">PLAY NOW • SPOTIFY</span>
                <h2 class="titulo-caixa" style="margin-top:10px;">Conecte sua conta do Spotify para abrir o diário ao vivo</h2>
                <p>Entre com o seu Spotify para acompanhar o que está tocando agora com letra, tradução, curiosidades, análise psicológica e quadros da revista. Você também pode clicar em qualquer faixa cadastrada no diário logo abaixo.</p>
                <a href="/login" class="botao-spotify">♪ Entrar com o Spotify</a>
            </div>
            {% else %}
            <div class="player-blog">
                <div class="polaroid">
                    <img id="album-img" src="" alt="Capa da música" style="display:none;">
                    <div id="album-placeholder" class="area-ilustracao" style="min-height:155px; padding:10px;">
                        <div class="disco-cd"><div class="miolo-cd"></div></div>
                        <div style="font-weight:700; font-size:14px;">Capa ao dar play</div>
                    </div>
                    <div class="polaroid-legenda" id="polaroid-legenda">xoxo • no repeat</div>
                </div>

                <div>
                    <span class="badge-ao-vivo" id="status-badge">● AGUARDANDO PLAY</span>
                    <div class="nome-faixa-player" id="track-title">Dê o play em uma música no Spotify</div>
                    <div class="artista-faixa-player" id="track-artist">ou escolha uma música do diário logo abaixo</div>

                    <div class="controles-player">
                        <button type="button" class="btn-acao" id="btn-pausa-tela" onclick="alternarPausaTela()">❚❚ Pausar / Retomar</button>
                        <a id="spotify-link" href="https://open.spotify.com" target="_blank" rel="noopener" class="btn-acao verde">♪ Ouvir no Spotify</a>
                        <span id="clipe-container"></span>
                    </div>

                    <div class="linha-progresso">
                        <span id="time-current">0:00</span>
                        <div class="trilho-progresso">
                            <div class="preenchimento-progresso" id="progress-bar"></div>
                        </div>
                        <span id="time-total">0:00</span>
                    </div>
                </div>

                <div class="mini-colagem-lateral">
                    <div class="adesivo-bloco rot1">♥ XOXO • DIÁRIO TEEN</div>
                    <div class="adesivo-bloco rot2">🎧 ON REPEAT • 2013–2014</div>
                    <div class="adesivo-bloco rot3">✂️ LETRA • BASTIDORES • MENTE</div>
                </div>
            </div>
            {% endif %}

            <div class="barra-musicas">
                <strong style="font-family:'Playfair Display', serif; font-style:italic; font-size:22px;">✂ Músicas cadastradas no diário (clique para abrir a matéria):</strong>
                <div class="lista-chips" id="chips-musicas"></div>
            </div>

            <div class="abas-materia">
                <button type="button" class="aba-btn ativa" data-aba="aba-01" onclick="abrirAbaMateria('aba-01', this)">
                    <span class="aba-rotulo">PÁGINA 01 • ENCARTE</span>
                    <span class="aba-titulo">♪ Letra e Tradução</span>
                </button>
                <button type="button" class="aba-btn" data-aba="aba-02" onclick="abrirAbaMateria('aba-02', this)">
                    <span class="aba-rotulo">PÁGINA 02 • BASTIDORES</span>
                    <span class="aba-titulo">✨ Curiosidades e Bastidores</span>
                </button>
                <button type="button" class="aba-btn" data-aba="aba-03" onclick="abrirAbaMateria('aba-03', this)">
                    <span class="aba-rotulo">PÁGINA 03 • COLUNA</span>
                    <span class="aba-titulo">🧠 Análise Psicológica</span>
                </button>
            </div>

            <div id="aba-01" class="conteudo-aba ativa">
                <div class="caixa-revista caixa-verde">
                    <div class="cabecalho-caixa">
                        <h2 class="titulo-caixa">♪ Página 01 — Letra e Tradução</h2>
                        <span class="selo selo-verde">ESTROFES &amp; TRADUÇÃO</span>
                    </div>
                    <div class="duas-colunas">
                        <div>
                            <div class="controles-player" style="margin-bottom:14px;">
                                <button type="button" class="btn-acao" id="btn-modo-pt" onclick="mudarModoLetra('pt', this)">Tradução (PT-BR)</button>
                                <button type="button" class="btn-acao branco" id="btn-modo-orig" onclick="mudarModoLetra('orig', this)">Referência Original</button>
                            </div>
                            <div id="lyrics-box" class="folha-letra">Escolha uma faixa ou dê o play no Spotify para ler aqui.</div>
                        </div>

                        <div class="grade-colagem">
                            <div class="recorte-foto esq">
                                <div class="area-ilustracao">
                                    <span class="selo selo-amarelo" style="margin-bottom:8px;">CD &amp; ENCARTE</span>
                                    <div class="disco-cd"><div class="miolo-cd"></div></div>
                                    <div style="font-weight:700;" id="nome-cd-colagem">Faixa em destaque</div>
                                </div>
                                <div class="legenda-scrap">versos que marcam o caderno</div>
                            </div>
                            <div class="recorte-foto dir">
                                <div class="area-ilustracao">
                                    <span class="selo selo-rosa" style="margin-bottom:8px;">FONES ON</span>
                                    <div style="font-size:40px; margin-bottom:6px;">🎧</div>
                                    <div style="font-weight:700;">Modo Revista</div>
                                </div>
                                <div class="legenda-scrap">leia acompanhando o som</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="aba-02" class="conteudo-aba">
                <div class="caixa-revista caixa-rosa">
                    <div class="cabecalho-caixa">
                        <h2 class="titulo-caixa">✨ Página 02 — Curiosidades e Bastidores</h2>
                        <span class="selo selo-rosa">EXCLUSIVE • XOXO</span>
                    </div>
                    <div class="duas-colunas">
                        <div id="gossip-box">As curiosidades e bastidores aparecem aqui.</div>
                        <div class="grade-colagem">
                            <div class="recorte-foto dir">
                                <div class="area-ilustracao">
                                    <span class="selo selo-lilas" style="margin-bottom:8px;">RECORTE</span>
                                    <div style="font-size:36px; margin-bottom:6px;">✂️📰</div>
                                    <div style="font-weight:700;">Bastidores da Faixa</div>
                                </div>
                                <div class="legenda-scrap">detalhes de estúdio e história</div>
                            </div>
                            <div class="recorte-foto esq">
                                <div class="area-ilustracao">
                                    <span class="selo selo-verde" style="margin-bottom:8px;">POLAROID</span>
                                    <div style="font-size:36px; margin-bottom:6px;">📷✨</div>
                                    <div style="font-weight:700;">Clima &amp; Referências</div>
                                </div>
                                <div class="legenda-scrap">tudo que passa despercebido</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div id="aba-03" class="conteudo-aba">
                <div class="caixa-revista caixa-amarela">
                    <div class="cabecalho-caixa">
                        <h2 class="titulo-caixa">🧠 Página 03 — Análise Psicológica</h2>
                        <span class="selo selo-amarelo">COLUNA ESPECIAL</span>
                    </div>
                    <div id="psych-box" class="coluna-psico">A análise psicológica aparece aqui.</div>
                </div>
            </div>

            <div class="grade-quadros">
                <article class="quadro quadro-rosa">
                    <div class="titulo-quadro">💗 AFINAL, SOBRE O QUE É ESSA MÚSICA?</div>
                    <p id="q-sobre" style="font-weight:600;"></p>
                </article>

                <article class="quadro quadro-lilas">
                    <div class="titulo-quadro">👀 VOCÊ PERCEBEU?</div>
                    <p id="q-percebeu" style="font-weight:600;"></p>
                </article>

                <article class="quadro quadro-amarelo">
                    <div class="titulo-quadro">🎀 VIBE CHECK</div>
                    <p id="q-vibe" style="font-weight:600;"></p>
                    <div class="lista-chips" id="q-vibe-selos"></div>
                </article>

                <article class="quadro quadro-verde">
                    <div class="titulo-quadro">💌 ESSA MÚSICA É PRA VOCÊ SE...</div>
                    <ul class="lista-situacoes" id="q-pra-voce"></ul>
                </article>

                <article class="quadro quadro-lilas">
                    <div class="titulo-quadro">📼 VOLTANDO NO TEMPO</div>
                    <p id="q-epoca" style="font-weight:600;"></p>
                </article>

                <article class="quadro quadro-amarelo">
                    <div class="titulo-quadro">⭐ NOTA DA REDAÇÃO</div>
                    <div class="selo selo-rosa" style="margin-bottom:10px;">★★★★★ DESTAQUE DO DIÁRIO</div>
                    <p id="q-nota" style="font-weight:600;"></p>
                </article>

                <article class="quadro-destaque-largo">
                    <span class="selo selo-amarelo">💭 A FRASE QUE FICA</span>
                    <div class="frase-marcante" id="q-frase"></div>
                    <p id="q-frase-legenda" style="font-weight:600;"></p>
                </article>

                <article class="quadro quadro-rosa" style="grid-column: 1 / -1;">
                    <div class="titulo-quadro">🎧 SE VOCÊ GOSTOU DESSA...</div>
                    <p style="font-weight:600;">Outras matérias do diário para continuar lendo:</p>
                    <div class="grade-recs" id="q-recs"></div>
                </article>

                <article class="quadro quadro-verde" style="grid-column: 1 / -1;">
                    <div class="titulo-quadro">💬 E VOCÊ?</div>
                    <p style="font-weight:600;">Deixe o seu comentário ou o que essa música significa pra você:</p>
                    <textarea id="input-comentario" class="campo-caderno" placeholder="Escreva aqui como numa página de diário..."></textarea>
                    <div style="margin-top:10px;">
                        <button type="button" class="btn-acao" onclick="adicionarComentario()">♥ Guardar no caderno</button>
                    </div>
                    <div id="lista-comentarios"></div>
                </article>
            </div>
        </section>

        <section id="sec-musicas" class="secao-portal">
            <div class="caixa-revista">
                <div class="cabecalho-caixa">
                    <h2 class="titulo-caixa">🎵 Todas as Músicas do Diário</h2>
                    <span class="selo selo-rosa">MÚSICAS</span>
                </div>
                <div class="grade-catalogo" id="cat-musicas"></div>
            </div>
        </section>

        <section id="sec-artistas" class="secao-portal">
            <div class="caixa-revista caixa-rosa">
                <div class="cabecalho-caixa">
                    <h2 class="titulo-caixa">🎤 Artistas</h2>
                    <span class="selo selo-amarelo">ARTISTAS</span>
                </div>
                <div class="grade-catalogo" id="cat-artistas"></div>
            </div>
        </section>

        <section id="sec-albuns" class="secao-portal">
            <div class="caixa-revista caixa-verde">
                <div class="cabecalho-caixa">
                    <h2 class="titulo-caixa">💿 Álbuns &amp; Eras</h2>
                    <span class="selo selo-verde">ÁLBUNS</span>
                </div>
                <div class="grade-catalogo" id="cat-albuns"></div>
            </div>
        </section>

        <section id="sec-playlists" class="secao-portal">
            <div class="caixa-revista caixa-amarela">
                <div class="cabecalho-caixa">
                    <h2 class="titulo-caixa">🎧 Playlists Temáticas</h2>
                    <span class="selo selo-rosa">PLAYLISTS</span>
                </div>
                <div class="grade-catalogo" id="cat-playlists"></div>
            </div>
        </section>

        <section id="sec-testes" class="secao-portal">
            <div class="caixa-revista">
                <div class="cabecalho-caixa">
                    <h2 class="titulo-caixa">💌 Testes da Revista</h2>
                    <span class="selo selo-lilas">GIRL TALK</span>
                </div>
                <p style="font-weight:700; margin-bottom:12px;">Qual é o seu mood de hoje na revista?</p>
                <button type="button" class="opcao-teste" onclick="resultadoTeste('a')">A) Intensidade máxima, sem meio-termo</button>
                <button type="button" class="opcao-teste" onclick="resultadoTeste('b')">B) Madrugada, saudade e pensamentos profundos</button>
                <button type="button" class="opcao-teste" onclick="resultadoTeste('c')">C) Conexão, entrega e romance no ar</button>
                <div id="caixa-resultado-teste" class="cartao-curiosidade" style="display:none; margin-top:12px;"></div>
            </div>
        </section>

        <section id="sec-sobre" class="secao-portal">
            <div class="caixa-revista caixa-rosa">
                <div class="cabecalho-caixa">
                    <h2 class="titulo-caixa">📖 Sobre a Revista</h2>
                    <span class="selo selo-amarelo">XOXO MY MUSIC DIARY</span>
                </div>
                <p style="font-size:19px; font-weight:600; margin-bottom:12px;">XOXO My Music Diary une a nostalgia das revistas adolescentes brasileiras de 2013–2014, o clima de blogs e diário pessoal e a análise de letras, bastidores e psicologia das músicas.</p>
                <p style="font-size:18px; font-weight:500;">Todos os seus textos originais e arquivos JSON em <code>musicas_extras/</code> continuam preservados.</p>
            </div>
        </section>
    </div>

    <script>
        const CATALOGO = {{ catalogo_json | safe }};
        const CHAVES = Object.keys(CATALOGO);

        let idFaixaAtual = null;
        let chaveSelecionada = CHAVES[0] || null;
        let letraPt = "";
        let letraOrig = "";
        let modoLetra = "pt";
        let pausadoNaTela = false;

        function normalizar(t) {
            return (t || "").toLowerCase().replace(/[’‘´`]/g, "'").trim();
        }

        function acharChave(titulo) {
            const n = normalizar(titulo);
            if (!n) return null;
            if (CATALOGO[n]) return n;
            const curto = n.split("(")[0].split(" - ")[0].trim();
            if (CATALOGO[curto]) return curto;
            for (const c of CHAVES) {
                if (n.includes(c)) return c;
            }
            return null;
        }

        function abrirSecao(idSec, btn) {
            document.querySelectorAll('.secao-portal').forEach(s => s.classList.remove('ativa'));
            document.querySelectorAll('.btn-secao').forEach(b => b.classList.remove('ativa'));
            const el = document.getElementById(idSec);
            if (el) el.classList.add('ativa');
            if (btn) btn.classList.add('ativa');
        }

        function abrirAbaMateria(idAba, btn) {
            document.querySelectorAll('.conteudo-aba').forEach(c => c.classList.remove('ativa'));
            document.querySelectorAll('.aba-btn').forEach(b => b.classList.remove('ativa'));
            const el = document.getElementById(idAba);
            if (el) el.classList.add('ativa');
            if (btn) btn.classList.add('ativa');
        }

        function mudarModoLetra(modo, btn) {
            modoLetra = modo;
            document.querySelectorAll('[id^="btn-modo-"]').forEach(b => b.classList.remove('ativa'));
            if (btn) btn.classList.add('ativa');
            renderizarLetra();
        }

        function renderizarLetra() {
            const box = document.getElementById('lyrics-box');
            if (!box) return;
            box.textContent = modoLetra === 'pt'
                ? (letraPt || "Tradução não disponível para esta faixa.")
                : (letraOrig || letraPt || "Letra original não disponível.");
        }

        function formatarTempo(ms) {
            const s = Math.max(0, Math.floor((ms || 0) / 1000));
            const m = Math.floor(s / 60);
            const r = s % 60;
            return m + ":" + (r < 10 ? "0" : "") + r;
        }

        function alternarPausaTela() {
            pausadoNaTela = !pausadoNaTela;
            const badge = document.getElementById('status-badge');
            if (badge && pausadoNaTela) badge.textContent = "❚❚ PAUSADO NA TELA";
        }

        function aplicarMateria(titulo, artista, info) {
            letraPt = (info && info.letra_limpa) ? info.letra_limpa : "Letra não encontrada para esta faixa.";
            letraOrig = (info && info.letra_original) ? info.letra_original : "";
            renderizarLetra();

            const gossip = document.getElementById('gossip-box');
            if (gossip) {
                const lista = (info && Array.isArray(info.curiosidades_lista) && info.curiosidades_lista.length)
                    ? info.curiosidades_lista
                    : [`<b>BASTIDORES:</b><br>Faixa <b>${titulo}</b> de <b>${artista}</b> no diário.`];
                gossip.innerHTML = lista.map(item => `<div class="cartao-curiosidade">${item}</div>`).join("");
            }

            const psych = document.getElementById('psych-box');
            if (psych) {
                const raw = (info && info.psicologia)
                    ? info.psicologia
                    : `<b>ANÁLISE PSICOLÓGICA — ${titulo.toUpperCase()}</b><br><br>Observe os sentimentos e emoções despertados por esta música.`;
                const partes = raw.split(/<br\s*\/?>\s*<br\s*\/?>|
\s*
/).filter(p => p.trim());
                psych.innerHTML = partes.map(p => `<p>${p.trim()}</p>`).join("");
            }

            const cdNome = document.getElementById('nome-cd-colagem');
            if (cdNome) cdNome.textContent = `${titulo} — ${artista}`;

            const clipeSpan = document.getElementById('clipe-container');
            if (clipeSpan) {
                clipeSpan.innerHTML = (info && info.link_clipe)
                    ? `<a href="${info.link_clipe}" target="_blank" rel="noopener" class="btn-acao branco">▶ Ver Clipe</a>`
                    : "";
            }

            const listaCur = (info && Array.isArray(info.curiosidades_lista)) ? info.curiosidades_lista : [];
            const txtPsico = (info && info.psicologia) ? info.psicologia.replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim() : "";

            document.getElementById('q-sobre').textContent = listaCur[0]
                ? listaCur[0].replace(/<[^>]+>/g, "")
                : `“${titulo}” (${artista}) traz uma história envolvente que conecta letra, ritmo e emoção.`;

            document.getElementById('q-percebeu').textContent = listaCur[1]
                ? listaCur[1].replace(/<[^>]+>/g, "")
                : `Repare em como os versos e o clima de “${titulo}” ganham força ao longo da faixa.`;

            document.getElementById('q-vibe').textContent = txtPsico
                ? txtPsico.slice(0, 180) + (txtPsico.length > 180 ? "..." : "")
                : `Atmosfera marcante de ${artista} para ouvir no repeat.`;

            document.getElementById('q-vibe-selos').innerHTML = [
                `<span class="selo selo-rosa">♪ ${artista}</span>`,
                `<span class="selo selo-amarelo">♥ 2013–2014</span>`,
                `<span class="selo selo-verde">ON REPEAT</span>`
            ].join("");

            document.getElementById('q-pra-voce').innerHTML = [
                "<li>★ Você quer trilha sonora cheia de personalidade pro seu momento.</li>",
                "<li>★ Gosta de letras com emoção, drama e identificação.</li>",
                "<li>★ Curte descobrir bastidores e o lado psicológico das músicas.</li>"
            ].join("");

            document.getElementById('q-epoca').textContent = `No espírito das revistas teen de 2013–2014 e dos blogs musicais, “${titulo}” (${artista}) ganha destaque pela força da letra e pela atmosfera.`;
            document.getElementById('q-nota').textContent = `Destaque da redação para “${titulo}” (${artista}) pela intensidade e identidade da faixa.`;

            const linhas = letraPt.split(/
?
/).map(l => l.trim()).filter(Boolean);
            document.getElementById('q-frase').textContent = linhas.length
                ? "“" + linhas.slice(0, 2).join(" / ").slice(0, 130) + "”"
                : "“Cada verso tem uma história pra contar.”";
            document.getElementById('q-frase-legenda').textContent = `${titulo} — ${artista}`;

            const outras = CHAVES.filter(c => c !== normalizar(titulo)).slice(0, 3);
            document.getElementById('q-recs').innerHTML = outras.map(c => {
                const d = CATALOGO[c];
                return `<div class="card-rec" onclick="escolherMusica('${c.replace(/'/g, "\'")}')">
                    <div style="font-size:12px; font-weight:700; color:#D62872;">${d.artista || "Artista"}</div>
                    <div style="font-family:'Playfair Display', serif; font-style:italic; font-weight:800; font-size:20px;">${c}</div>
                </div>`;
            }).join("");
        }

        function escolherMusica(chave) {
            const d = CATALOGO[chave];
            if (!d) return;
            chaveSelecionada = chave;
            document.querySelectorAll('.chip-musica').forEach(ch => ch.classList.toggle('ativa', ch.dataset.k === chave));
            const tEl = document.getElementById('track-title');
            const aEl = document.getElementById('track-artist');
            const leg = document.getElementById('polaroid-legenda');
            if (tEl) tEl.textContent = chave;
            if (aEl) aEl.textContent = d.artista || "Artista";
            if (leg) leg.textContent = chave;
            aplicarMateria(chave, d.artista || "Artista", d);
            abrirSecao('sec-home', document.querySelector('.btn-secao[data-sec="sec-home"]'));
        }

        function montarListas() {
            const chips = document.getElementById('chips-musicas');
            const catM = document.getElementById('cat-musicas');
            const catA = document.getElementById('cat-artistas');
            const catAl = document.getElementById('cat-albuns');
            const catP = document.getElementById('cat-playlists');

            if (chips) {
                chips.innerHTML = CHAVES.map((c, i) =>
                    `<button type="button" class="chip-musica ${i === 0 ? 'ativa' : ''}" data-k="${c.replace(/"/g, '&quot;')}" onclick="escolherMusica('${c.replace(/'/g, "\'")}')">${c}</button>`
                ).join("");
            }

            if (catM) {
                catM.innerHTML = CHAVES.map(c => {
                    const d = CATALOGO[c];
                    return `<div class="card-cat">
                        <div>
                            <div style="font-size:12px; font-weight:700; color:#D62872;">${d.artista || "Artista"}</div>
                            <div style="font-family:'Playfair Display', serif; font-style:italic; font-weight:800; font-size:22px;">${c}</div>
                        </div>
                        <button type="button" class="btn-acao" onclick="escolherMusica('${c.replace(/'/g, "\'")}')">Abrir matéria →</button>
                    </div>`;
                }).join("");
            }

            const artistas = [...new Set(CHAVES.map(c => (CATALOGO[c].artista || "").trim()).filter(Boolean))];
            if (catA) {
                catA.innerHTML = artistas.map(art => {
                    const primeira = CHAVES.find(c => (CATALOGO[c].artista || "").trim() === art);
                    return `<div class="card-cat">
                        <div>
                            <div style="font-size:12px; font-weight:700; color:#1F6E43;">ARTISTA</div>
                            <div style="font-family:'Playfair Display', serif; font-style:italic; font-weight:800; font-size:22px;">${art}</div>
                        </div>
                        <button type="button" class="btn-acao verde" onclick="escolherMusica('${primeira.replace(/'/g, "\'")}')">Ver faixa →</button>
                    </div>`;
                }).join("");
            }

            if (catAl) {
                catAl.innerHTML = [
                    { t: "Mind of Mine & Eras Solo", k: "pillowtalk" },
                    { t: "Icarus Falls & Baladas", k: "common" },
                    { t: "Trilhas & Bastidores", k: "who" }
                ].filter(x => CATALOGO[x.k]).map(x =>
                    `<div class="card-cat">
                        <div style="font-family:'Playfair Display', serif; font-style:italic; font-weight:800; font-size:22px;">${x.t}</div>
                        <button type="button" class="btn-acao" onclick="escolherMusica('${x.k}')">Abrir encarte →</button>
                    </div>`
                ).join("");
            }

            if (catP) {
                catP.innerHTML = [
                    { t: "Noite & Intensidade", k: "bordersz" },
                    { t: "Saudade & Madrugada", k: "it's you" },
                    { t: "Conexão & Entrega", k: "natural" }
                ].filter(x => CATALOGO[x.k]).map(x =>
                    `<div class="card-cat">
                        <div style="font-family:'Playfair Display', serif; font-style:italic; font-weight:800; font-size:22px;">${x.t}</div>
                        <button type="button" class="btn-acao" onclick="escolherMusica('${x.k}')">Abrir playlist →</button>
                    </div>`
                ).join("");
            }

            if (chaveSelecionada && CATALOGO[chaveSelecionada]) {
                escolherMusica(chaveSelecionada);
            }
        }

        function resultadoTeste(op) {
            const box = document.getElementById('caixa-resultado-teste');
            if (!box) return;
            box.style.display = 'block';
            if (op === 'a') box.textContent = "Seu mood hoje pede intensidade! Veja a matéria de bordersz ou befour.";
            else if (op === 'b') box.textContent = "Seu mood hoje pede reflexão e madrugada! Veja it's you ou like i would.";
            else box.textContent = "Seu mood hoje pede conexão! Veja natural ou common.";
        }

        function adicionarComentario() {
            const inp = document.getElementById('input-comentario');
            const list = document.getElementById('lista-comentarios');
            if (!inp || !list) return;
            const txt = inp.value.trim();
            if (!txt) return;
            const d = document.createElement('div');
            d.className = 'nota-salva';
            d.textContent = "♥ " + txt;
            list.prepend(d);
            inp.value = "";
        }

        async function atualizarPlayer() {
            const badge = document.getElementById('status-badge');
            if (!badge) return;
            try {
                const res = await fetch('/api/now-playing');
                if (res.status === 401) {
                    window.location.href = '/';
                    return;
                }
                const data = await res.json();
                if (data.playing) {
                    badge.textContent = pausadoNaTela ? "❚❚ PAUSADO NA TELA" : "● TOCANDO AGORA NO SPOTIFY";
                    const tEl = document.getElementById('track-title');
                    const aEl = document.getElementById('track-artist');
                    const linkSp = document.getElementById('spotify-link');
                    const tc = document.getElementById('time-current');
                    const tt = document.getElementById('time-total');
                    const pb = document.getElementById('progress-bar');

                    if (tEl) tEl.textContent = data.name;
                    if (aEl) aEl.textContent = data.artist;
                    if (linkSp && data.spotify_url) linkSp.href = data.spotify_url;
                    if (tc) tc.textContent = formatarTempo(data.progress);
                    if (tt) tt.textContent = formatarTempo(data.duration);
                    if (pb && data.duration > 0) {
                        pb.style.width = Math.min(100, (data.progress / data.duration) * 100) + "%";
                    }

                    if (data.id !== idFaixaAtual) {
                        idFaixaAtual = data.id;
                        const img = document.getElementById('album-img');
                        const ph = document.getElementById('album-placeholder');
                        const leg = document.getElementById('polaroid-legenda');
                        if (img && data.image) {
                            img.src = data.image;
                            img.style.display = 'block';
                            if (ph) ph.style.display = 'none';
                        }
                        if (leg) leg.textContent = data.name;

                        const ch = acharChave(data.name);
                        const base = ch ? CATALOGO[ch] : {};
                        aplicarMateria(data.name, data.artist, {
                            ...base,
                            letra_limpa: data.lyrics || base.letra_limpa,
                            curiosidades_lista: (Array.isArray(data.gossip) && data.gossip.length) ? data.gossip : base.curiosidades_lista,
                            psicologia: data.psychology || base.psicologia,
                            link_clipe: data.clipe || base.link_clipe
                        });
                    }
                } else {
                    badge.textContent = "❚❚ SPOTIFY PAUSADO";
                }
            } catch (e) {
                console.log(e);
            }
        }

        montarListas();
        setInterval(atualizarPlayer, 1500);
        atualizarPlayer();
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
