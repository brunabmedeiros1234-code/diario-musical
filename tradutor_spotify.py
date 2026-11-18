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
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — PILLOWTALK</b><br><br>
<b>1. Dualidades extremas e funcionamento psíquico</b><br>
A letra apresentada descreve um relacionamento profundamente intenso, marcado por dualidades extremas: luz e escuridão, dor e prazer, amor e conflito ("transando e brigando", "minha inimiga, minha aliada"). Na psicologia — especialmente na Psicanálise, na Teoria do Apego e na Psicologia Analítica (Junguiana) —, esse tipo de dinâmica não é visto apenas como "dramático", mas como um reflexo de padrões profundos de funcionamento psíquico, regulação emocional e busca por conexão.<br><br>
<b>2. A Teoria do Apego e a regulação emocional</b><br>
Pela Teoria do Apego (John Bowlby), relacionamentos que oscilam violentamente entre a fusão total ("Só nós dois, nossos corpos juntos", "te abraçar bem perto") e o conflito ("briga", "zona de guerra") costumam apontar para um padrão de apego ansioso-ambivalente. A necessidade constante de estar colado ao outro ("na cama o dia inteiro", "hoje e sempre") pode mascarar um medo profundo de abandono ou rejeição. O outro funciona como um regulador externo da própria autoestima e segurança emocional. Quando a vulnerabilidade pura gera medo, a briga surge como um atalho para sentir intensidade. Em dinâmicas disfuncionais, a pessoa prefere o conflito a se sentir ignorada ou desconectada. A oscilação entre "prisioneiros e livres" mostra a dificuldade de manter a autonomia sem perder o vínculo.<br><br>
<b>3. A Tensão dos Opostos: O Arquétipo da Sombra e o Perigo</b><br>
Sob a ótica de Carl Jung, a paixão intensa e caótica muitas vezes não é apenas sobre o outro, mas sobre o que o outro desperta em nós. "Minha inimiga, minha aliada": Jung falava sobre a Sombra — partes de nós mesmos que reprimimos ou não aceitamos. Em relacionamentos intensos, o parceiro frequentemente atua como um espelho para os nossos impulsos mais inconscientes (a raiva, a vulnerabilidade, a impulsividade). O Fascínio pelo Perigo ("Comportamento inconsequente"): A zona de fronteira entre o "puro" e o "sujo e intenso" revela a atração pelo lado instintivo da psique. Para algumas pessoas, a estabilidade parece "vazia" ou entediante porque o sistema nervoso foi condicionado a associar o amor à adrenalina e ao sofrimento.<br><br>
<b>4. O Ciclo de Recompensa Intermitente e a dependência química</b><br>
Do ponto de vista da Psicologia Cognitivo-Comportamental (PCC) e da neurobiologia das relações, o ciclo de "paraíso e zona de guerra" gera uma forte dependência no cérebro. Quando um casal briga intensamente e depois faz as pazes de forma apaixonada, o cérebro recebe uma descarga massiva de dopamina e ocitocina no momento da reconciliação. Esse contraste faz com que os momentos de pico pareçam divinos ("nosso paraíso"), tornando o indivíduo tolerante aos momentos de dor ("vejo a dor, vejo o prazer"). A Dor Compartilhada ("Onde as lágrimas encontram espaço"): A música mostra que o parceiro é o único refúgio seguro para as vulnerabilidades, criando uma codependência onde o mundo exterior é visto como ameaçador.""",
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
É você, é você, é você

Eu não vou, eu não vou, eu não vou
Esconder as cicatrizes, vou deixá-las sangrar
Para que o meu silêncio, para que o meu silêncio não
Seja confundido com paz

Eu estou errado por querer que nós dois dêem certo?
Me conte suas mentiras, porque eu simplesmente não consigo encarar a verdade

É você, é você, é você
É você, é você, é você

Será que isso pode ser uma lição que eu nunca precisei aprender?
Eu enxerguei tudo como uma bênção, mas agora isso virou uma maldição
Eu não sei por quê, eu não sei por quê

É você, é você
É você, é você, é você""",
        "curiosidades_lista": [
            "💔 <b>DR DRAMA NA ÁREA:</b> Zayn percebeu que a cremosa só age por interesse próprio e tem planos próprios. Ele sabe que está rolando mentira purinha, mas fica totalmente sem entender tanta frieza e insensibilidade.",
            "🗣️ <b>BATE-BOCA DE CASAL?:</b> Sim! Outra teoria babadeira é que a letra retrata uma discussão onde he explica que outra garota está dando em cima dele por conveniência. O boy fica frustrado porque o namoro está afundando!",
            "🥀 <b>A DOR DE COTOVELO:</b> Mesmo machucado e sabendo que ela some sem dar satisfação, he confessa que ela é a única que he quer. É aquela conexão tóxica que não importa se sobrevive ou não, continua grudada!",
            "👑 <b>SUBVERTENDO O CLICHÊ:</b> Sabe o famoso 'não é você, sou eu' dos términos? Zayn joga a real total e diz: A CULPA É SUA SIM ('It's you')! No fim, a repetição mostra toda a fossa de continuar desejando quem só pisa na bola.",
            "😱 <b>ALERTA DE COINCIDÊNCIA?:</b> Fãs notaram que a repetição lembra o hit 'Gotta Be You' do 1D. Será que foi indireta?",
            "🩸 <b>DEIXANDO AS CICATRIZES SANGRAR:</b> Em vez de fingir ser o forte, he prefere escancarar as feridas. O silêncio dele NUNCA é paz!",
            "🚪 <b>O FANTASMA DO 1D:</b> Falando em silêncio, lembra o climão da saída dele do One Direction! He confessou que já queria vazar desde o primeiro ano.",
            "🎶 <b>TOQUE ESPECIAL:</b> Na reta final, vocais no estilo <i>raga</i> dão um toque melancólico e super diferentão! 🖤✨"
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — IT'S YOU</b><br><br>
Se a gente analisar “It’s You” pela ótica da Psicologia, sem transformar a letra em um diagnóstico do ZAYN, ela apresenta uma dinâmica emocional bien interessante: apego, ambivalência, dificuldade de aceitar a realidade do relacionamento e sofrimento diante de uma relação que machuca, mas da qual a pessoa ainda não consegue se desligar.<br><br>
<b>1. Assimetria e falta de validação emocional</b><br>
Logo no início aparece uma percepção de assimetria na relação. O eu lírico sente que a outra pessoa se aproxima por razões próprias e que suas necessidades não são consideradas: “Ela não se importa nem um pouco com o que eu preciso.”<br><br>
<b>2. Conflito entre razão e emoção</b><br>
“Minha cabeça não consegue entender”<br>
Aqui aparece um conflito entre razão e emoção. He percebe que alguma coisa está errada, mas não consegue organizar racionalmente aquilo que está sentindo. Entender cognitivamente uma situação não significa conseguir aceitá-la emocionalmente.<br><br>
<b>3. Evitação emocional e negação</b><br>
“Me conte suas mentiras, porque eu simplesmente não consigo encarar a verdade”<br>
A verdade provavelmente seria dolorosa demais para ser encarada naquele momento. Então, paradoxalmente, he prefere ouvir uma mentira que preserve algum tipo de esperança.""",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    },
    "befour": {
        "artista": "zayn",
        "letra_limpa": """Eu já passei por isso trước
Mas nunca desse jeito

Eu não bebo só pra ficar bêbado
Eu sei aproveitar o momento
Se tem algo que eu quero
Vou atrás, mesmo que dê errado
Vou ficar na minha
Cansei de ficar remoendo isso
E não tenho mais vontade de brigar por isso

Entorpecido no alto de um telhado
Coloco fogo em tudo
Só pra provar pra mim mesmo
Que estou vivendo no limite
Entorpecido no alto de um telhado
Coloco fogo em tudo
Só pra provar pra mim mesmo
Que estou vivendo no limite

Então fala o que quiser, fala mesmo
Diz tudo o que você tem pra dizer
Fala o que quiser, não precisa esconder
O triste é que você não tem coragem de dizer isso na minha cara

Eu já passei por isso trước
Mas não assim, não assim

Está na hora de seguir em frente
Já se passaram tantas horas
Meu coração continua batendo
Você não tem mais como me controlar
Você fica aí, sem dizer o que pensa
Então me desculpa se eu também ficar calado
Não consigo mais entrar no seu ritmo""",
        "curiosidades_lista": [
            "🏆 <b>O SIGNIFICADO DE BEFOUR:</b> O título é um trocadilho genial! Significa 'Before' (antes), fazendo alusão à época anterior à sua fama mundial e ao One Direction, mas também carrega o número '4' (four), marcando sua nova fase.",
            "🔓 <b>LIVRE DAS AMARRAS:</b> Tudo o que Zayn havia feito <i>antes</i> estava ligado aos outros quatro integrantes do One Direction. Pela primeira vez, he teve total liberdade para decidir os rumos do próprio trabalho e produzir a música que realmente queria."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — BEFOUR</b><br><br>Autonomia, identidade e a quebra de amarras externas sob a ótica da autodeterminação.",
        "link_clipe": "https://www.youtube.com/watch?v=_EaPxw5exts"
    },
    "love like this": {
        "artista": "zayn",
        "letra_limpa": """Ah, eu adoro quando você mostra, quando você mostra  
Quando você mostra que está do meu lado  

Se alguém tentar falar, tentar falar  
Tentar falar mal de you, eu acabo com eles  

O jeito que você chega neles com a roupa e o olhar  
Com os quadris e o cabelo desse jeito  
Me deixa completamente no clima, no clima  

Eu não quero perder tempo  
Porque você é a minha coroa  
Eu só quero aproveitar o seu tempo e  
Está tudo em jogo, mas eu preferiria estar morto  
Se isso significasse viver uma vida sem você, amor  

Acho que isso é um amor assim  
Normalmente, eu nunca me entregaria desse jeito  
Mas quero apostar todas as minhas fichas  
Porque eu não posso voltar atrás  
Te dou tudo e você pode sair por aí desse jeito  
Mas preciso correr esse risco porque não volto atrás""",
        "curiosidades_lista": [
            "🚀 <b>O GRANDE RETORNO:</b> Depois de sumir e deixar a gente sofrendo, Zayn voltou com tudo na Mercury Records!",
            "🃏 <b>PAIXONADO E JOGADO AOS PÉS:</b> He confessa que nunca se entrega fácil, mas por quem mexe com a cabeça dele, o boy bota a mão no fogo e vai all-in sem olhar pra trás! 💋"
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — LOVE LIKE THIS</b><br><br>Disposição ao risco emocional e a quebra de defesas de apego após um histórico de cautela.",
        "link_clipe": "https://www.youtube.com/watch?v=918oGJFtjjw"
    },
    "she": {
        "artista": "zayn",
        "letra_limpa": """Ela coloca um pouco de si em cada drinque
Ela sempre sabe onde a galera está
Ela leva o cigarro à boca
Eu apago, porque ela gosta assim
Ela dança até quando está chovendo
Ei, quando é que vai começar, amor?
Ela olha pra mim como se estivesse esperando
E faz o tempo passar mais devagar quando a levam até a mesa

Luzes brilhantes, mas ela vai se apagando
Parece bom, ela é meio louca
Luzes brilhantes, mas ela vai se apagando
Parece bom, ela é meio louca

Ela quer alguém que a ame e a abrace
Ela quer alguém que saiba amá-la de verdade
Ela quer alguém que a ame e a beije
Ela quer alguém que saiba amá-la de verdade""",
        "curiosidades_lista": [
            "🌙 <b>A DONA DA NOITE E DOS DRINQUES:</b> A misteriosa garota de <i>'She'</i> vive até altas horas da madrugada. Há um trocadilho genial na letra com a palavra <i>'spirit'</i>: em inglês, ela serve tanto para se referir a bebidas destiladas quanto àquela dose de coragem da saideira antes de dormir!"
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — SHE</b><br><br>Busca por afeto, comportamentos de risco, ambivalência emocional e a relação entre liberdade e autodestruição.",
        "link_clipe": "https://www.youtube.com/watch?v=4MZjcAAn380"
    },
    "drunk": {
        "artista": "zayn",
        "letra_limpa": """Noites que viram madrugada, olhos vermelhos
Amnésia no gelo
Madrugadas, olhos vermelhos
Amnésia, eu preciso de você

Agora, não consigo nem enxergar direito
É verdade, fico bêbado quando estou com você
Fico numa euforia, como se tivesse tomado alguma coisa
Quando estou com você, parece que entro em outra realidade""",
        "curiosidades_lista": [
            "🍷 <b>AS DUAS FORMAS DE EMBRIAGUEZ:</b> Zayn apresenta, logo no início da música, a ideia central de duas formas de embriaguez: a causada pelo álcool e pelas drogas e aquela provocada pela paixão."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — DRUNK</b><br><br>A confusão entre a intoxicação por substâncias e a intensidade emocional de estar apaixonado.",
        "link_clipe": "https://www.youtube.com/watch?v=mpmpfKyM1i4"
    },
    "rear view": {
        "artista": "zayn",
        "letra_limpa": """Será que seu coração pode ser meu
Enquanto você procura?
Porque eu não tenho tempo
Pra te ajudar a encontrar as palavras
Melodias e lembranças
Histórias que parecem absurdas
Não vou mentir pra você

Desde que você
Olhe nos meus olhos
Eu vou aonde você estiver
E vou seguir seus passos

Ouvi falar de tudo o que você fez
E de todas as batalhas que enfrentou
Ouvi falar de todo amor que você perdeu
Tudo acabou antes mesmo de começar

Nunca duvidei de mim mesmo
Mas duvidei de você
Cansei de me olhar
Pelo retrovisor""",
        "curiosidades_lista": [
            "🪞 <b>UMA CONVERSA COM O PRÓPRIO REFLEXO:</b> Em seu livro autobiográfico, Zayn explicou que 'Rear View' foi construída como uma espécie de reflexão diante do espelho."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — REAR VIEW</b><br><br>Autoconhecimento, conflitos internos, ruminação e a exaustão de olhar para o próprio passado.",
        "link_clipe": "https://www.youtube.com/watch?v=xV3QUVbOhnI"
    },
    "wrong (feat. kehlani)": {
        "artista": "zayn",
        "letra_limpa": """Ah, não estamos na mesma sintonia
Me mostra tudo sob a mesma luz
Parece certo quando a gente se solta
Roupa no chão, porque ela é tão suave
Essa não é uma disputa justa
Quero deixar tudo bem claro
Vou te deixar mais molhada do que nunca

Você está procurando meu amor no lugar errado
Não pense que só porque está comigo, isso é de verdade
Você está procurando meu amor no lugar errado""",
        "curiosidades_lista": [
            "🔥 <b>A QUÍMICA DE MILHÕES:</b> 'wRoNg' traz uma parceria impecável com a cantora Kehlani, unindo vocais R&B super suaves a uma letra crua sobre desejo noturno e expectativas desalinhadas."
        ],
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL — WRONG</b><br><br>Indisponibilidade emocional, intimidade física versus afetiva e o conflito de expectativas.",
        "link_clipe": "https://www.youtube.com/watch?v=gT_WbE9D-4w"
    },
    "fool for you": {
        "artista": "zayn",
        "letra_limpa": """Esse amor tá marcado
Eu preciso de você e odeio isso
Você fica entre um sonho e uma cena de filme
De certa forma, você sabe o que eu quero dizer

Quando a escuridão vira neblina
Eu simplesmente não consigo resistir

Porque eu sou um bobo por você
E por tudo que você faz
Eu sou um bobo por você
E por tudo, por tudo que você faz""",
        "curiosidades_lista": [
            "🎸 <b>A INFLUÊNCIA CLÁSSICA DOS BEATLES:</b> Em sua autobiografia, Zayn contou que estava ouvindo muito Beatles durante a produção de <i>Mind of Mine</i>."
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