import json
import os
from datetime import datetime
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, render_template_string

ID = "51ebc5fc21fa4e359bebdd37175c9f13"
SEC = "8670dd178bb0463086bdbda323dc889f"
URI = "http://127.0.0.1:8888/callback"
ARQUIVO_HISTORICO = "historico_diario_brunabmed.json"

MESES_PT = {
    "01": "Janeiro", "02": "Fevereiro", "03": "Marco", "04": "Abril",
    "05": "Maio", "06": "Junho", "07": "Julho", "08": "Agosto",
    "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"
}

app = Flask(__name__)

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=ID,
        client_secret=SEC,
        redirect_uri=URI,
        scope="user-read-playback-state user-read-currently-playing",
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
Do ponto de vista da Psicologia Cognitivo-Comportamental (PCC) e da neurobiologia das relações, o ciclo de "paraíso e zona de guerra" gera uma forte dependência no cérebro. Quando um casal briga intensamente e depois faz as pazes de forma apaixonada, o cérebro recebe uma descarga massiva de dopamina e ocitocina no momento da reconciliação. Esse contraste faz com que os momentos de pico pareçam divinos ("nosso paraíso"), tornando o indivíduo tolerante aos momentos de dor ("vejo a dor, vejo o prazer"). A Dor Compartilhada ("Onde as lágrimas encontram espaço"): A música mostra que o parceiro é o único refúgio seguro para as vulnerabilidades, criando uma codependência onde o mundo exterior é visto como ameaçador.<br><br>
<b>O TRABALHO DO PSICÓLOGO</b><br><br>
Quando a psicologia atende uma pessoa que vive (e muitas vezes sofre) em uma dinâmica tão intensa quanto a descrita na música, o trabalho clínico não visa "apagar a paixão" ou julgar a intensidade, mas sim ajudar o paciente a entender de onde vem essa necessidade de caos e como construir autonomia emocional. O processo terapêutico com alguém preso nesse ciclo de "paraíso e zona de guerra" geralmente transcorre em fases estruturadas:<br><br>
<b>Conscientização e Identificação de Padrões (O "Despertar")</b><br>
O primeiro passo na terapia é ajudar o paciente a perceber que esse ciclo não é amor romântico inevitável, mas sim um padrão repetitivo de sofrimento. O psicólogo ajuda a pessoa a mapear os altos e baixos. O paciente costuma chegar focado apenas nos momentos de pico ("o paraíso", a reconciliação intensa, o sexo), ignorando o custo emocional dos momentos de vale ("a zona de guerra", as brigas exaustivas). A pergunta terapêutica central é: "O que acontece com você nos momentos de calmaria? A paz te parece entediante?" Muitas vezes, descobre-se que a pessoa confunde tranquilidade com apatia ou abandono, porque seu sistema nervoso só sabe amar através da adrenalina.<br><br>
<b>Investigação da História de Vida e Origens do Apego</b><br>
A psicologia busca entender por que essa pessoa aprendeu que o amor precisa doer para ser real. Explorando o passado, o terapeuta investiga as primeiras referências de afeto do paciente (sua dinâmica familiar na infância). Se a criança cresceu em ambientes imprevisíveis, frios ou onde o afeto vinha acompanhado de drama, tensão e reconciliação forçada, o cérebro grava a seguinte fórmula: "Amor = Drama + Perigo + Alívio posterior". A terapia ajuda a entender se essa pessoa está buscando um parceiro ou um salvador/cuidador para curar feridas antigas de rejeição ou abandono.<br><br>
<b>Regulação Emocional e Tolerância à Calmaria</b><br>
Um dos maiores desafios no consultório é que pessoas acostumadas a relações intensas sentem uma ansiedade imensa na estabilidade. Sem o drama, o relacionamento parece "frio" ou "vazio". O psicólogo ensina técnicas de regulação do sistema nervoso. O paciente aprende a tolerar a ausência de conflito sem achar que o relacionamento está acabando. A desintoxicação da dopamina ajuda a perceber que o ciclo de "transando e brigando" funciona como um vício químico. Aprender a se relacionar sem precisar do contraste extremo exige reaprender a sentir prazer em vínculos seguros, previsíveis e maduros.<br><br>
<b>Fortalecimento do "Eu" (Individuação)</b><br>
A música reforça a fusão total: "Só nós dois, nossos corpos juntos", "ninguém além de você". Na psicologia, isso aponta para a falta de fronteiras saudáveis (codependência). Resgatando a identidade, o terapeuta encoraja o paciente a olhar para a própria vida fora da relação: Amigos próprios? Hobbies individuais? Projetos pessoais que não dependem do parceiro? A distinção entre Fusão e Intimidade ensina que intimidade verdadeira exige duas pessoas inteiras e separadas que escolhem estar juntas, e não duas metades fundidas que entram em pânico só de pensar em se distanciar ("prisioneiros e depois somos livres").<br><br>
<b>O Grande Objetivo da Terapia nesse Caso</b><br>
O trabalho do psicólogo não é dizer para a pessoa terminar o relacionamento, mas sim devolver a ela o poder de escolha. Muitas vezes, a pessoa se sente totalmente impotente frente aos impulsos da paixão ("é mais forte do que eu", "eu não consigo viver sem ele/ela"). A psicologia trabalha para transformar essa compulsão inconsciente em uma escolha consciente: “Eu escolho ficar porque quero construir algo saudável, e não porque dependo desse caos para sentir que estou viva(o)”.""",
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
        "psicologia": """Se a gente analisar “It’s You” pela ótica da Psicologia, sem transformar a letra em um diagnóstico do ZAYN, ela apresenta uma dinâmica emocional bien interessante: apego, ambivalência, dificuldade de aceitar a realidade do relacionamento e sofrimento diante de uma relação que machuca, mas da qual a pessoa ainda não consegue se desligar.<br><br>
<b>1. Assimetria e falta de validação emocional</b><br>
Logo no início aparece uma percepção de assimetria na relação. O eu lírico sente que a outra pessoa se aproxima por razões próprias e que suas necessidades não são consideradas: “Ela não se importa nem um pouco com o que eu preciso.” Psicologicamente, isso pode representar a sensação de não ser emocionalmente validado pelo parceiro. A pessoa percebe que existe uma discrepância entre aquilo que ela oferece ou espera e aquilo que recebe. Isso também pode gerar uma pergunta interna: “Se ela não se importa comigo, por que continua me procurando?” — e essa falta de coerência contribui para a confusão emocional presente na música.<br><br>
<b>2. Conflito entre razão e emoção</b><br>
“Minha cabeça não consegue entender”<br>
Aqui aparece um conflito entre razão e emoção. He percebe que alguma coisa está errada, mas não consegue organizar racionalmente aquilo que está sentindo. Isso é bastante comum em relacionamentos emocionalmente intensos: a pessoa pode reconhecer comportamentos prejudiciais e, ao mesmo tempo, continuar emocionalmente ligada. Não significa necessariamente falta de inteligência ou racionalidade. É que entender cognitivamente uma situação não significa conseguir aceitá-la emocionalmente. É possível pensar: “Eu sei que isso está me fazendo mal.” e simultaneamente sentir: “Mas eu ainda quero essa pessoa.” Essa contradição é justamente uma das forças da música.<br><br>
<b>3. Evitação emocional e negação</b><br>
“Me conte suas mentiras, porque eu simplesmente não consigo encarar a verdade”<br>
Esse talvez seja o trecho psicologicamente mais interessante. He parece demonstrar evitação emocional. A verdade provavelmente seria dolorosa demais para ser encarada naquele momento. Então, paradoxalmente, he prefere ouvir uma mentira que preserve algum tipo de esperança. Isso pode ser compreendido como um mecanismo de negação ou esquiva, dependendo do contexto. É como se a mente dissesse: “Eu sei que existe uma realidade dolorosa aqui, mas ainda não estou preparado para aceitá-la.” Isso não significa necessariamente que a pessoa seja permanentemente incapaz de lidar com a realidade. Pode representar um estágio de sofrimento em que aceitar a situação parece mais doloroso do que permanecer na esperança.<br><br>
<b>4. Fixação emocional e apego ambivalente</b><br>
“É você, é você, é você”<br>
A repetição é muito importante. Mesmo depois de falar sobre mentiras, sofrimento e indiferença, he volta para “é você”. Isso pode representar uma espécie de fixação emocional: apesar das experiências negativas, aquela pessoa continua ocupando um lugar central em sua mente. Existe uma contradição:<br>
• “Você me machuca.”<br>
• “Eu sei que existe algo errado.”<br>
• “Mesmo assim, é você que eu quero.”<br>
Na Psicologia, não seria correto automaticamente chamar isso de “dependência emocional”, porque seria necessário conhecer a história e o funcionamento da pessoa. Ma a música apresenta elementos que podem lembrar uma relação de forte dependência afetiva ou apego ambivalente.<br><br>
<b>5. A necessidade de validar a própria dor</b><br>
“Não vou esconder as cicatrizes, vou deixá-las sangrar”<br>
Aqui aparece uma mudança. Em vez de fingir que está tudo bem, he decide mostrar o sofrimento. “Meu silêncio não será confundido com paz.” Psicologicamente, isso pode representar uma necessidade de reconhecimento e validação da própria dor. He não quer que a outra pessoa interprete seu silêncio como “Ele superou.” ou “Ele não se importa.” Na verdade, o silêncio significa: “Eu estou machucado, e quero que você perceba isso.” Existe, portanto, uma tentativa de tornar o sofrimento visível.<br><br>
<b>6. Conflito entre desejo, realidade e culpa</b><br>
“Estou errado por querer que nós dois deem certo?”<br>
Essa frase mostra conflito entre desejo e realidade. He sabe que existem problemas, mas ainda deseja preservar o relacionamento. Isso é muito humano. O desejo de que uma relação funcione não desaparece necessariamente no momento em que surgem problemas. A pergunta também revela uma possível culpa: “Será que estou errado por ainda querer essa pessoa?” He parece questionar os próprios sentimentos porque a realidade da relação não corresponde ao que gostaria que ela fosse.<br><br>
<b>7. A mudança na representação psicológica</b><br>
“Eu enxerguei tudo como uma bênção, mas agora isso virou uma maldição”<br>
Aqui aparece uma mudança na representação psicológica do relacionamento. Inicialmente, aquela relação era percebida como algo positivo: bênção → amor → conexão → esperança. Depois, a experiência passa a ser: dor → confusão → sofrimento → maldição. É interessante porque a pessoa não necessariamente deixou de amar. O que mudou foi a maneira como ela interpreta aquilo que está vivendo. Isso pode acontecer quando uma relação começa de maneira muito positiva e posteriormente passa a produzir sofrimento. A pessoa pode ficar presa entre duas imagens: “Quem essa pessoa era para mim.” e “O que essa pessoa está fazendo comigo agora.”<br><br>
<b>8. O ponto central: a ambivalência</b><br>
Se eu tivesse que resumir a música psicologicamente em uma palavra, seria: ambivalência.<br>
He parece sentir simultaneamente:<br>
• amor e ressentimento;<br>
• desejo e sofrimento;<br>
• esperança e desesperança;<br>
• proximidade e necessidade de proteção;<br>
• consciência do problema e dificuldade de aceitá-lo;<br>
• vontade de ficar e percepção de que aquilo está machucando.<br>
E isso é muito diferente de simplesmente “estar apaixonado”. A música parece retratar alguém que sabe que o relacionamento está lhe causando sofrimento, mas ainda não conseguiu romper emocionalmente com ele.<br><br>
<b>9. Abordagem terapêutica</b><br>
Se fosse trabalhado em Psicologia, um psicólogo provavelmente não começaria dizendo “você tem apego ansioso” ou “você é dependente emocional”. Primeiro investigaria:<br>
• O que exatamente aconteceu nessa relação?<br>
• Quais comportamentos da outra pessoa estão causando sofrimento?<br>
• Por que he sente que precisa das “mentiras”?<br>
• O que he teme encontrar se encarar a verdade?<br>
• Por que ainda deseja permanecer?<br>
• Como he costuma reagir quando sente abandono ou rejeição?<br>
• He consegue estabelecer limites?<br>
• O relacionamento é realmente recíproco?<br>
• O que he entende como amor?<br>
• O que he está tentando preservar: a pessoa real ou a relação que gostaria que existisse?<br>
A partir daí, a terapia poderia trabalhar regulação emocional, reconhecimento das próprias necessidades, limites, padrões de relacionamento, autoestima, elaboração da perda e aceitação da realidade, caso a relação realmente tenha chegado ao fim.""",
        "link_clipe": "https://www.youtube.com/watch?v=C_3d6GntKbk"
    },
    "befour": {
        "artista": "zayn",
        "letra_limpa": """Eu já passei por isso antes
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

Eu já passei por isso antes
Mas não assim, não assim

Está na hora de seguir em frente
Já se passaram tantas horas
Meu coração continua batendo
Você não tem mais como me controlar
Você fica aí, sem dizer o que pensa
Então me desculpa se eu também ficar calado
Não consigo mais entrar no seu ritmo

Entorpecido no alto de um telhado
Coloco fogo em tudo
Só pra provar pra mim mesmo
Que estou vivendo no limite

Então fala o que quiser, fala mesmo
Diz tudo o que você tem pra dizer
Fala o que quiser, não precisa esconder
O triste é que você não tem coragem de dizer isso na minha cara

Eu já passei por isso antes
Mas não assim, não assim

Luzes piscando

Então fala o que quiser, fala mesmo
Diz tudo o que você tem pra dizer
Fala o que quiser, não precisa esconder
O triste é que você não tem coragem de dizer isso na minha cara

Então fala o que quiser, fala mesmo
Diz tudo o que você tem pra dizer
Fala o que quiser, não precisa esconder
O triste é que você não tem coragem de dizer isso na minha cara

Eu já passei por isso antes
Mas não assim, não assim
Eu já passei por isso antes

(Não assim, não assim)""",
        "curiosidades_lista": [
            "🏆 <b>O SIGNIFICADO DE BEFOUR:</b> O título é um trocadilho genial! Significa 'Before' (antes), fazendo alusão à época anterior à sua fama mundial e ao One Direction, mas também carrega o número '4' (four), marcando sua nova fase.",
            "🔓 <b>LIVRE DAS AMARRAS:</b> Tudo o que Zayn havia feito <i>antes</i> estava ligado aos outros quatro integrantes do One Direction. Pela primeira vez, he teve total liberdade para decidir os rumos do próprio trabalho e produzir a música que realmente queria.",
            "🎙️ <b>A FRUSTRAÇÃO MUSICAL:</b> Em entrevista à revista <i>The Fader</i>, Zayn revelou que no One Direction, quando sugeria um verso mais R&B com sua identidade, precisava gravá-lo dezenas de vezes até virar uma versão pop e genérica. A gerência já tinha um padrão comercial definido e he sentia que aquilo não era he.",
            "🎭 <b>A PERSONA DO 'BAD BOY':</b> He também comentou como a gravadora e a mídia tentavam retratá-lo como o misterioso ou quieto da banda — um produto comercialmente útil que não correspondia necessariamente à sua personalidade real.",
            "🎯 <b>O RECADO AOS CRÍTICOS:</b> A letra já havia sido sugerida por Zayn antes mesmo de sua saída do grupo. Nela, he manda um recado direto: as pessoas podem falar mal e espalhar rumores, mas nada disso vai impedi-lo de seguir em frente e fazer o que quer.",
            "📸 <b>BASTIDORES DO CLIPE:</b> Gravado em um bairro operário de Bradford, sua cidade natal, o clipe mostra Zayn curtindo com amigos de infância, jogando sinuca e comendo em uma lanchonete simples, celebrando suas raízes."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — BEFOUR</b><br><br>
A Psicologia pode fazer uma leitura muito interessante dessa música, principalmente porque ela parece falar de algo que vai além de simplesmente superar críticas ou deixar pessoas desagradáveis para trás. A letra apresenta alguém que já passou por situações difíceis, mas que, dessa vez, está reagindo de uma maneira diferente. Existe uma tentativa de recuperar o controle da própria vida, romper com expectativas externas e encontrar uma identidade que não dependa mais da aprovação dos outros. O ponto mais interessante é a contradição que aparece ao longo da música: o eu lírico afirma que não quer mais discutir, que não se importa com o que dizem e que está pronto para seguir em frente, mas, ao mesmo tempo, continua voltando ao assunto. He ainda precisa responder às críticas, demonstrar que não foi afetado e provar para si mesmo que está vivendo de acordo com as próprias escolhas.<br><br>
Psicologicamente, isso abre espaço para discutir mecanismos de defesa, regulação emocional, autonomia, identidade, esquiva experiencial, ruminação e até a relação entre sofrimento e comportamentos de risco.<br><br>
<b>1. Identidade, autonomia e construção do self</b><br>
"Eu já passei por isso antes / Mas nunca desse jeito"<br>
Essa abertura apresenta uma distinção importante: a pessoa reconhece que já enfrentou situações semelhantes, mas entende que a experiência atual tem algo diferente. Pela perspectiva da Psicologia, podemos relacionar isso à construção da identidade e à maneira como o indivíduo se percebe diante das experiências que vive. Na teoria do desenvolvimento psicossocial de Erik Erikson, a construção da identidade envolve a formação de um senso de continuidade e coerência sobre quem somos. Isso também passa pela capacidade de reconhecer quais escolhas, valores e comportamentos realmente representam o indivíduo, em vez de apenas corresponderem às expectativas externas. Pensando na trajetória de Zayn, essa interpretação ganha outra dimensão. Durante sua passagem pelo One Direction, he relatou que nem sempre se identificava com as músicas produzidas pelo grupo e com a imagem que era construída para he. Ao iniciar uma carreira solo, passou a ter mais liberdade para experimentar outros estilos e expressar aspectos de sua identidade artística. Assim, o trecho pode representar não apenas alguém enfrentando uma situação difícil novamente, mas alguém que, dessa vez, está tentando enfrentá-la sem abandonar a própria identidade.<br><br>
<b>2. Autonomia</b><br>
Na Teoria da Autodeterminação, desenvolvida por Edward Deci e Richard Ryan, a autonomia é uma das necessidades psicológicas básicas. Ela diz respeito à possibilidade de agir de acordo com os próprios valores e escolhas, sentindo-se autor da própria vida. Nesse sentido, a música pode ser interpretada como uma tentativa de recuperar essa autonomia depois de um período em que o indivíduo sentia que outras pessoas tinham influência excessiva sobre suas decisões.<br><br>
<b>3. Regulação emocional, evitação e tentativa de não sentir</b><br>
"Eu não bebo só pra ficar bêbado / Eu sei aproveitar o momento / Se tem algo que eu quero / Vou atrás, mesmo que dê errado / Vou ficar na minha / Cansei de ficar remoendo isso / E não tenho mais vontade de brigar por isso"<br>
Aqui aparece uma mudança na maneira de lidar com os conflitos. O eu lírico demonstra cansaço de discutir, justificar suas escolhas e permanecer preso a situações que parecem não levar a lugar nenhum. He decide se afastar desse ciclo e direcionar sua atenção para aquilo que deseja. Isso pode ser relacionado à regulação emocional, que corresponde aos processos pelas quais as pessoas influenciam quais emoções sentem, quando as sentem e como as expressam. Entretanto, existe uma diferença entre regular as emoções e simplesmente evitar entrar em contato com elas. A regulação emocional envolve reconhecer o que se está sentindo e encontrar maneiras de lidar com essas emoções. Já a esquiva experiencial, conceito bastante discutido na Terapia de Aceitação e Compromisso (ACT), acontece quando a pessoa tenta evitar, controlar ou eliminar experiências internas desagradáveis, mesmo quando essa tentativa acaba limitando sua vida. Por exemplo, decidir não discutir mais com alguém pode representar um limite saudável. Mas, se a pessoa deixa de conversar porque não consegue suportar o desconforto de expressar o que sente, o afastamento também pode funcionar como uma forma de esquiva. A letra deixa essa possibilidade em aberto: o eu lírico pode estar aprendendo a não desperdiçar energia com conflitos improdutivos, mas também pode estar tentando se afastar de sentimentos que ainda não conseguiu elaborar.<br><br>
<b>4. Entorpecimento emocional e comportamentos de risco</b><br>
"Entorpecido no alto de um telhado / Coloco fogo em tudo / Só pra provar pra mim mesmo / Que estou vivendo no limite"<br>
Este é um dos trechos psicologicamente mais interessantes da música. A imagem de alguém entorpecido, em um lugar alto e colocando fogo em tudo pode ser interpretada como uma representação de alguém que está emocionalmente anestesiado, mas que procura experiências intensas para voltar a sentir alguma coisa. O conceito de entorpecimento emocional diz respeito à dificuldade de acessar, reconhecer ou experimentar determinadas emoções. Em algumas situações, a pessoa pode sentir que está emocionalmente desligada, como se nada tivesse intensidade suficiente para despertar uma reação. Isso não significa necessariamente ausência de sentimentos. Às vezes, o entorpecimento pode funcionar como uma maneira de se proteger de emoções difíceis, como frustração, tristeza, raiva ou decepção. Existe também uma possível relação com os comportamentos de risco. Quando o indivíduo sente que perdeu o controle sobre determinados aspectos da própria vida, pode procurar situações intensas para experimentar uma sensação de liberdade, autonomia ou domínio. A busca por experiências extremas pode funcionar como uma tentativa de romper com a sensação de vazio ou de recuperar a percepção de que ainda está vivo e no controle. Podemos relacionar esse comportamento ao conceito de sensation seeking, estudado pelo psicólogo Marvin Zuckerman. He se refere à busca por experiências novas, variadas e intensas, mesmo quando envolvem riscos. É importante destacar que a letra não permite concluir que o personagem esteja necessariamente apresentando esse padrão psicológico; trata-se de uma possibilidade interpretativa. Outro ponto importante é a expressão "só pra provar pra mim mesmo". Ela sugere que o indivíduo não está tentando demonstrar algo apenas para os outros, mas também para si próprio. Isso abre uma discussão sobre a necessidade de reafirmar a própria existência, identidade e capacidade de escolha depois de um período em que se sentiu limitado.<br><br>
<b>5. Mecanismos de defesa e necessidade de demonstrar indiferença</b><br>
"Então fala o que quiser, fala mesmo / Diz tudo o que você tem pra dizer / Fala o que quiser, não precisa esconder / O triste é que você não tem coragem de dizer isso na minha cara"<br>
Aqui podemos observar uma postura bastante defensiva. O eu lírico parece tentar transmitir a mensagem de que as opiniões alheias não o afetam mais. He desafia as outras pessoas a falarem abertamente, como se estivesse acima das críticas. Entretanto, existe uma contradição: se he realmente não se importasse com o que dizem, por que dedicaria tanto espaço a essas críticas? Isso não significa que esteja mentindo quando afirma não se importar. Uma pessoa pode decidir conscientemente que não quer mais dar importância às opiniões externas e, ainda assim, continuar emocionalmente afetada por ellas. Podemos relacionar isso aos mecanismos de defesa, conceito desenvolvido pela tradição psicanalítica. Um mecanismo particularmente interessante nessa situação é a formação reativa, que acontece quando uma pessoa manifesta uma atitude ou comportamento que se opõe a um sentimento ou impulso que considera difícil de aceitar. Por exemplo, alguém que se sente profundamente atingido por uma crítica pode demonstrar uma indiferença exagerada como forma de proteção. Não significa que toda demonstração de indiferença seja formação reativa. Para fazer essa interpretação, seria necessário conhecer melhor os sentimentos e os comportamentos da pessoa. Também podemos pensar na racionalização, quando alguém constrói explicações que tornam determinada situação emocionalmente mais aceitável. Nesse contexto, afirmar que as críticas não merecem atenção poderia ajudar a pessoa a lidar com o desconforto de ter sido julgada ou rejeitada. Outro aspecto é a necessidade de confrontar aqueles que falam pelas costas. Isso pode indicar que o problema não está somente na crítica, mas também na maneira como ela acontece. O indivíduo parece se incomodar com a falta de sinceridade e com a impossibilidade de resolver o conflito diretamente.<br><br>
<b>6. Reatância psicológica: a necessidade de recuperar a liberdade</b><br>
"Está na hora de seguir em frente / Já se passaram tantas horas / Meu coração continua batendo / Você não tem mais como me controlar"<br>
Esse trecho pode ser relacionado a um conceito muito interessante: a reatância psicológica. Desenvolvida por Jack Brehm, a teoria da reatância psicológica explica como as pessoas podem reagir quando percebem que sua liberdade de escolha está sendo ameaçada ou restrita. Quando alguém sente que outra pessoa está tentando controlar suas decisões, pode desenvolver uma resistência ainda maior àquela influência, justamente para recuperar a liberdade que acredita estar perdendo. Por exemplo, uma pessoa que passou muito tempo sendo pressionada a agir de determinada maneira pode começar a rejeitar até mesmo algumas sugestões que, em outras circunstâncias, aceitaria naturalmente. A necessidade de demonstrar que ninguém mais tem controle sobre suas escolhas pode se tornar uma forma de reafirmar a própria autonomia. No contexto da música, isso combina com a trajetória artística de Zayn e com os relatos que deu sobre sua insatisfação com o controle exercido sobre sua imagem e sua produção musical durante o One Direction. A frase "meu coração continua batendo" também merece atenção. Ela pode ser interpretada como uma afirmação de resistência: apesar do que aconteceu, o indivíduo continua ali, seguindo sua vida. É quase como se dissesse: você pode ter me afetado, mas não conseguiu acabar comigo.<br><br>
<b>7. O silêncio como proteção e afastamento emocional</b><br>
"Você fica aí, sem dizer o que pensa / Então me desculpa se eu também ficar calado / Não consigo mais entrar no seu ritmo"<br>
Aqui a música apresenta uma questão importante sobre relacionamentos e comunicação. O eu lírico demonstra perceber uma falta de comunicação da outra pessoa. Em resposta, decide também permanecer em silêncio. Psicologicamente, podemos pensar em duas possibilidades diferentes. A primeira é o estabelecimento de limites emocionais: quando alguém percebe que está tentando manter uma comunicação que não é correspondida, pode decidir parar de insistir. Nesse caso, o silêncio representa uma maneira de preservar a própria saúde emocional e deixar de assumir sozinho a responsabilidade pelo relacionamento. A segunda possibilidade é o afastamento emocional como estratégia de proteção: a pessoa pode evitar conversar porque não quer se expor novamente, correr o risco de ser rejeitada ou entrar em contato com sentimentos desagradáveis. Também podemos relacionar este comportamento à comunicação passivo-agressiva, dependendo da intenção envolvida. Isso aconteceria, por exemplo, se o silêncio fosse utilizado para punir a outra pessoa, provocar culpa ou demonstrar insatisfação sem expressá-la diretamente (embora não seja possível afirmar apenas pela letra). A frase "não consigo mais entrar no seu ritmo" é especialmente significativa porque sugere que o indivíduo está cansado de adaptar seu comportamento às atitudes de outra pessoa. He não quer mais acompanhar uma dinâmica na qual sente que suas necessidades não são consideradas.<br><br>
<b>8. Ruminação, ressentimento e dificuldade de encerrar um conflito</b><br>
Existe algo que chama atenção quando comparamos dois momentos da música:<br>
"Cansei de ficar remoendo isso / E não tenho mais vontade de brigar por isso"<br>
E, posteriormente:<br>
"Então fala o que quiser, fala mesmo / Diz tudo o que você tem pra dizer"<br>
Apesar de afirmar que está cansado de pensar sobre o assunto, o eu lírico continua retomando o conflito ao longo da música. Isso permite discutir a diferença entre superar uma situação e simplesmente decidir que não quer mais lidar com ela. Na Psicologia, a ruminação é um processo de pensamento repetitivo, geralmente voltado para experiências negativas, suas causas e consequências. A pessoa pode passar muito tempo revivendo uma discussão, imaginando o que deveria ter dito ou tentando compreender por que foi tratada de determinada maneira. O problema é que este processo nem sempre leva a uma solução; muitas vezes, mantém o indivíduo emocionalmente conectado àquilo que deseja deixar para trás. O ressentimento também pode estar presente, envolvendo a permanência de sentimentos negativos relacionados a uma experiência percebida como injusta, ofensiva ou dolorosa. Assim, existe uma possível contradição no personagem: he quer seguir em frente, mas ainda parece precisar de algum tipo de reconhecimento sobre o que aconteceu. Talvez não queira mais discutir, mas ainda queira que a outra pessoa reconheça que errou. Talvez não queira mais explicações, mas ainda se incomode com a maneira como foi tratado. Isso mostra que o encerramento de um conflito não depende necessariamente de deixar de sentir alguma coisa. Às vezes, a pessoa consegue interromper o contato e seguir com a vida mesmo sem ter elaborado completamente o que aconteceu.<br><br>
<b>9. Resiliência ou tentativa de provar que está tudo bem?</b><br>
Um aspecto que atravessa praticamente toda a música é a tentativa de demonstrar força. O eu lírico afirma que já passou por situações difíceis, que não pretende mais discutir, que ninguém pode controlá-lo e que está pronto para seguir em frente. Isso pode ser relacionado à resiliência, entendida como a capacidade de enfrentar adversidades, adaptar-se e continuar se desenvolvendo diante de experiências difíceis. Entretanto, existe uma diferença entre ser resiliente e sentir a necessidade constante de demonstrar que nada consegue nos atingir. A resiliência não exige ausência de sofrimento. Uma pessoa resiliente também pode sentir tristeza, raiva, medo, insegurança e frustração. O que caracteriza este processo é a possibilidade de reconhecer estas experiências e encontrar maneiras de lidar com elas.<br><br>
<b>O TRABALHO DO PSICÓLOGO</b><br><br>
Se essa música fosse utilizada como ponto de partida para compreender uma pessoa que estivesse passando por algo semelhante, o trabalho psicológico não seria simplesmente ensiná-la a ignorar as críticas ou a se afastar de quem a incomoda. Seria importante compreender o que está por trás dessa necessidade de romper com determinadas relações, recuperar o controle e demonstrar independência. Algumas questões poderiam orientar a investigação clínica:<br><br>
• <b>Por que preciso provar que não me importo?</b> Necessidade de validação, insegurança e mecanismos de defesa.<br>
• <b>Por que continuo pensando em algo que digo querer esquecer?</b> Ruminação, ressentimento e dificuldade de elaboração emocional.<br>
• <b>Estou me afastando porque quero ou porque tenho medo de me machucar?</b> Esquiva experiencial e autoproteção.<br>
• <b>Consigo expressar o que sinto sem precisar me defender?</b> Regulação emocional e assertividade.<br>
• <b>Minhas escolhas realmente representam quem sou?</b> Identidade, autonomia e autodeterminação.<br>
• <b>Preciso fazer coisas extremas para sentir que estou vivo?</b> Comportamentos de risco e estratégias de enfrentamento.<br><br>
Na música, podemos interpretar que o personagem está tentando construir uma nova relação consigo mesmo. He não quer mais se definir pelo que aconteceu, nem permitir que as atitudes de outras pessoas determinem suas escolhas. Mas ainda parece existir uma necessidade de provar que conseguiu superar tudo. Essa distinção é importante: não precisar mais da aprovação dos outros é diferente de precisar demonstrar aos outros que você não precisa da aprovação deles. A segunda situação ainda mantém a pessoa, de certa maneira, vinculada à opinião alheia.""",
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
        "psicologia": "🧠 <b>ANÁLISE COMPORTAMENTAL:</b><br><br>Em Love Like This, o foco está na disposição ao risco emocional e na quebra de defesas de apego. A decisão de 'apostar todas as fichas' e vulnerabilizar-se após um histórico de cautela reflete o processo terapêutico de superação de barreiras defensivas.",
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
Ela quer alguém que saiba amá-la de verdade

Ela grita que me ama
Segura minhas mãos para que eu não vá embora
Porque ela não quer ficar sozinha
Ela diz: "Só quero que você me abrace"

Luzes brilhantes, mas ela vai se apagando
Parece bom, ela é meio louca
Luzes brilhantes, mas ela vai se apagando
Parece bom, ela é meio louca

Ela quer alguém que a ame e a abrace
Ela quer alguém que saiba amá-la de verdade
Ela quer alguém que a ame e a beije
Ela quer alguém que saiba amá-la de verdade

Do jeito certo
Do jeito certo

Do jeito certo, do jeito, do jeito certo
Do jeito certo, do jeito certo
Do jeito certo, do jeito, do jeito certo
Do jeito certo, do jeito certo
Do jeito certo, do jeito, do jeito certo
Do jeito certo, do jeito certo
Do jeito certo, do jeito, do jeito certo
Do jeito certo

Ela quer alguém que a ame e a abrace
Ela quer alguém que saiba amá-la de verdade
Ela quer alguém que a ame e a abrace
Ela quer alguém que saiba amá-la de verdade
Ela quer alguém que a ame e a beije
Ela quer alguém que saiba amá-la de verdade""",
        "curiosidades_lista": [
            "🌙 <b>A DONA DA NOITE E DOS DRINQUES:</b> A misteriosa garota de <i>'She'</i> vive até altas horas da madrugada. Há um trocadilho genial na letra com a palavra <i>'spirit'</i>: em inglês, ela serve tanto para se referir a bebidas destiladas quanto àquela dose de coragem da saideira antes de dormir!",
            "🚬 <b>O JOGO DO CIGARRO E DA IRONIA:</b> Ela tem o hábito constante de fumar, e parece adorar quando Zayn tenta fazê-la parar — talvez justamente pela ironia de continuar fumando mesmo assim, debochando dos hábitos e sabendo que o próprio Zayn também fuma.",
            "🌧️ <b>DANÇANDO NA CHUVA E NA REBELDIA:</b> Quando o verso diz <i>'Ela sempre dança quando está chovendo'</i>, a música transmite aquela aura de pura ousadia. Enquanto todo mundo corre para se proteger do temporal, ela faz questão de desafiar a tempestade. Tudo nela transborda esse toque rebelde, deixando Zayn dividido sem saber se consegue acompanhar o ritmo eletrizante dela ou se ela é realmente a pessoa certa para sua vida."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — SHE</b><br><br>
A psicologia poderia analisar a história de “She”, do Zayn, a partir de alguns temas interessantes: busca por afeto, comportamentos de risco, dificuldade de estabelecer vínculos, ambivalência emocional e a relação entre liberdade e autodestruição.<br><br>
O ponto principal é que a mulher retratada parece viver entre dois movimentos: de um lado, busca prazer, diversão e liberdade; de outro, demonstra sinais de vulnerabilidade e uma possível necessidade de acolhimento. O narrador, por sua vez, parece atraído por ela, mas não sabe se consegue acompanhá-la ou se essa relação seria saudável.<br><br>
<b>1. Busca por prazer e regulação emocional</b><br>
O consumo frequente de álcool, o cigarro e as festas podem ser analisados pela perspectiva da regulação emocional.<br>
Na psicologia, regulação emocional é o conjunto de processos pelos quais uma pessoa tenta administrar suas emoções. Algumas pessoas recorrem a atividades prazerosas para aliviar sentimentos desagradáveis, como tristeza, ansiedade, solidão ou frustração.<br>
Nesse contexto, beber e fumar podem funcionar como estratégias de enfrentamento (coping).<br>
Por exemplo:<br>
- Beber para diminuir a ansiedade ou se sentir mais à vontade.<br>
- Sair constantemente para evitar ficar sozinha com os próprios pensamentos.<br>
- Fumar como uma forma de aliviar momentaneamente a tensão.<br>
Isso não significa que toda pessoa que bebe ou fuma esteja tentando fugir de algum sofrimento. O comportamento, isoladamente, não permite chegar a essa conclusão. A questão psicológica seria entender qual função esses hábitos desempenham na vida dela.<br><br>
<b>2. Esquiva experiencial: fugir do que se sente</b><br>
Um conceito particularmente interessante para interpretar esta personagem é a esquiva experiencial, trabalhada na Terapia de Aceitação e Compromisso (ACT).<br>
Ela acontece quando alguém tenta evitar, controlar ou eliminar experiências internas desagradáveis, como pensamentos, lembranças e emoções.<br>
Imagine uma pessoa que não consegue lidar com a própria tristeza. Em vez de entrar em contato com este sentimento, ela procura constantemente alguma distração: festas, bebidas, cigarro, relacionamentos ou situações intensas.<br>
O alívio pode acontecer, mas costuma ser temporário. Quando a distração termina, aquilo que estava sendo evitado pode continuar presente.<br>
A personagem poderia representar este movimento: está sempre envolvida em alguma atividade, mas isso não necessariamente significa que esteja emocionalmente bem.<br>
A diferença importante: gostar de festas e de experiências intensas não é, por si só, uma forma de esquiva. É necessário observar se estas atividades estão sendo usadas rigidamente para não entrar em contato com emoções difíceis.<br><br>
<b>3. Comportamentos de risco e busca por sensações</b><br>
Outro conceito que combina com a narrativa é a busca por sensações (sensation seeking), estudado pelo psicólogo Marvin Zuckerman.<br>
Esse conceito descreve a tendência de algumas pessoas a procurar experiências novas, intensas e estimulantes, mesmo quando envolvem algum grau de risco.<br>
Isso pode aparecer em comportamentos como:<br>
- Procurar festas e ambientes movimentados.<br>
- Gostar de situações imprevisíveis.<br>
- Experimentar atividades intensas.<br>
- Ter maior disposição para assumir riscos.<br>
A imagem da mulher dançando enquanto chove pode ser interpretada simbolicamente dessa maneira. Enquanto outras pessoas procuram abrigo, ela permanece na chuva, como se não se importasse com as convenções ou com os riscos.<br>
Entretanto, existe uma distinção importante: buscar experiências intensas não é necessariamente uma forma de autodestruição. Pode representar espontaneidade, personalidade e desejo de liberdade.<br><br>
<b>4. Ambivalência emocional: querer proximidade e, ao mesmo tempo, manter distância</b><br>
A narrativa também permite pensar em uma possível ambivalência emocional.<br>
A mulher parece gostar de receber a atenção do narrador quando he tenta fazê-la parar de fumar. Isso pode sugerir que ela aprecia ser cuidada, mesmo sem necessariamente demonstrar disposição para mudar seus comportamentos.<br>
Aqui podemos pensar em dois desejos que coexistem:<br>
- Autonomia: querer viver conforme as próprias vontades, sem que outra pessoa determine suas escolhas.<br>
- Vínculo: querer receber atenção, cuidado e demonstrações de afeto.<br>
Essas necessidades não são contraditórias. Uma pessoa pode desejar independência e, ao mesmo tempo, querer ser amada e acolhida.<br>
A questão é como ela administra estas duas necessidades dentro de um relacionamento.<br><br>
<b>5. O papel do narrador: atração, cuidado e impotência</b><br>
Também seria interessante analisar o comportamento de Zayn na história.<br>
He parece interessado nessa mulher, mas existe uma percepção de que ela possui hábitos e um estilo de vida que talvez sejam incompatíveis com aquilo que he deseja para si.<br>
Quando tenta fazê-la parar de fumar, por exemplo, podemos pensar na tentativa de exercer influência sobre o comportamento de alguém de quem gostamos.<br>
Entretanto, existe uma diferença entre cuidar de alguém e assumir a responsabilidade por mudar essa pessoa.<br>
Na psicologia, isso pode ser relacionado aos limites interpessoais.<br>
Uma pessoa pode:<br>
- Demonstrar preocupação.<br>
- Expressar o que a incomoda.<br>
- Oferecer apoio.<br>
- Estabelecer limites sobre aquilo que aceita em uma relação.<br>
Mas não pode assumir o controle das escolhas do outro.<br>
O narrador parece estar diante dessa dificuldade: gostar de alguém não significa necessariamente conseguir construir uma relação com essa pessoa.<br><br>
<b>6. Idealização e incompatibilidade afetiva</b><br>
Outro aspecto possível é a idealização.<br>
Quando estamos atraídos por alguém, podemos dar destaque às características que nos encantam e minimizar aquelas que nos incomodam.<br>
A intensidade, a espontaneidade e a imprevisibilidade da mulher podem ser justamente o que atrai o narrador. Ao mesmo tempo, estas características podem fazê-lo questionar se conseguiria acompanhar seu estilo de vida.<br>
Cria-se uma tensão entre desejo e compatibilidade.<br>
Na psicologia dos relacionamentos, atração e compatibilidade são dimensões diferentes. Sentir uma forte atração por alguém não significa que exista compatibilidade de valores, expectativas, hábitos e necessidades emocionais.<br>
É possível gostar muito de uma pessoa e ainda perceber que a relação pode não funcionar.<br><br>
<b>7. Como a psicoterapia trabalharia essa situação?</b><br>
Se a mulher fosse uma paciente, o psicólogo não começaria dizendo que ela precisa parar de beber, fumar ou sair tanto. Primeiro, procuraria compreender sua história e o significado desses comportamentos.<br>
Algumas abordagens poderiam trabalhar assim:<br>
- <b>Terapia Cognitivo-Comportamental (TCC):</b> Investigaria pensamentos, emoções e situações que antecedem o consumo de álcool e cigarro, identificando padrões e desenvolvendo estratégias alternativas.<br>
- <b>Terapia de Aceitação e Compromisso (ACT):</b> Trabalharia a relação dela com emoções desagradáveis, a esquiva experiencial e a construção de uma vida orientada por valores pessoais.<br>
- <b>Entrevista Motivacional:</b> Exploraria a ambivalência em relação aos hábitos, ajudando-a a identificar suas próprias razões para mudar, sem imposições.<br>
- <b>Abordagem psicodinâmica:</b> Investigaria possíveis conflitos emocionais, experiências anteriores e padrões relacionais que poderiam estar relacionados aos comportamentos atuais.<br>
O objetivo não seria transformar a mulher em alguém mais comportada ou menos espontânea, mas compreender se suas escolhas estão alinhadas com aquilo que ela realmente deseja para a própria vida.""",
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
Quando estou com você, parece que entro em outra realidade

De um jeito diferente, como deveria ser
Te levo para um canto, por você, eu até viraria mais uma dose
Bêbado todas as noites, curtindo cada música
Alterado todas as noites, dançando sem parar

Bêbados durante todo o verão
Bêbados durante todo o verão
Passamos o verão inteiro bêbados
Bebendo, nos deixando levar, curtindo até perder o equilíbrio

Noites que viram madrugada, olhos vermelhos
Amnésia, eu preciso de você

Agora estou com as emoções à flor da pele
Perco o controle quando estou com você
Espero não ter falado demais
Acho que sempre passo dos limites quando estou com você

De um jeito diferente, como deveria ser
Te levo para um canto, por você, eu até viraria mais uma dose
Bêbado todas as noites, curtindo cada música
Alterado todas as noites, dançando sem parar
(Fingindo a noite inteira)

Bêbados durante todo o verão
Bêbados durante todo o verão
Passamos o verão inteiro bêbados
Bebendo, nos deixando levar, curtindo até perder o equilíbrio

Noites que viram madrugada, olhos vermelhos
Amnésia no gelo
Madrugadas, olhos vermelhos
Amnésia, eu preciso de você

Bêbado, bêbado, bêbado, bêbado
Bêbado, bêbado, bêbado, bêbado
(Levantem seus copos; não vá embora)
Bêbado, bêbado, bêbado, bêbado
Bêbado, bêbado, bêbado, bêbado

Bêbados durante todo o verão
Bêbados durante todo o verão
Isso está se espalhando por aí, yeah""",
        "curiosidades_lista": [
            "🍷 <b>AS DUAS FORMAS DE EMBRIAGUEZ:</b> Zayn apresenta, logo no início da música, a ideia central de duas formas de embriaguez: a causada pelo álcool e pelas drogas e aquela provocada pela paixão. He está “bêbado” tanto pelo efeito das substâncias quanto pelo amor da pessoa com quem está.",
            "🌿 <b>OLHOS VERMELHOS E AMNESIA:</b> Os olhos vermelhos e vidrados indicam o possível uso de drogas — talvez, mais especificamente, da variedade de maconha chamada Amnesia. Já a sensação de estar fora de si e as falhas de memória podem representar a descarga de adrenalina e a espécie de névoa constante em que os dois vivem por causa desse amor."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — DRUNK</b><br><br>
A psicologia poderia trabalhar essa música a partir de uma ideia central: a confusão entre a intoxicação provocada por substâncias e a intensidade emocional de estar apaixonado.<br><br>
A interpretação apresentada sugere que o narrador vive duas experiências simultâneas: está sob efeito de álcool ou drogas e, ao mesmo tempo, completamente envolvido pela pessoa que ama. A música aproxima essas duas sensações, como se ambas provocassem euforia, perda de controle e uma espécie de desligamento da realidade. Isso abre espaço para discutir alguns conceitos psicológicos interessantes.<br><br>
<b>1: Sistema de recompensa cerebral</b><br>
Um dos primeiros conceitos que podemos explorar é o sistema de recompensa cerebral. Quando uma pessoa se apaixona, especialmente no início de um envolvimento, podem ocorrer alterações na atividade de circuitos relacionados à motivação, ao prazer e à busca por recompensas. A dopamina é um dos neurotransmissores envolvidos nesse processo. Ela participa da motivação, da aprendizagem por recompensa e da busca por experiências prazerosas.<br><br>
Isso ajuda a compreender por que estar perto de alguém por quem sentimos atração pode provocar: euforia e entusiasmo, desejo de permanecer perto da pessoa, pensamentos frequentes sobre ela, expectativa pelo próximo encontro e sensação de que tudo fica mais interessante quando ela está presente. Na música, quando Zayn diz que fica intoxicado na presença da pessoa amada, podemos interpretar esta comparação como uma representação da intensidade da paixão. Entretanto, é importante não confundir as coisas: apaixonar-se não é biologicamente equivalente a consumir drogas. A música utiliza uma metáfora para aproximar experiências que podem compartilhar alguns mecanismos de recompensa.<br><br>
<b>2: Intoxicação e alteração da percepção</b><br>
A música também apresenta sinais de alteração da consciência: olhos vermelhos, dificuldade para enxergar direito, sensação de estar fora de si e falhas de memória.<br><br>
Do ponto de vista psicológico e neuropsicológico, podemos analisar a partir dos efeitos das substâncias psicoativas sobre o funcionamento cerebral. O álcool, por exemplo, pode prejudicar: atenção e concentração, coordenação motora, julgamento e tomada de decisões, controle dos impulsos e formação de novas memórias. Já a cannabis pode provocar alterações na percepção do tempo, atenção, memória de curto prazo e coordenação, além de efeitos variáveis sobre o humor. Um detalhe interessante é a expressão amnesia on ice. A amnésia pode funcionar como uma metáfora para a perda de lembranças durante estas noites de intoxicação, mas também pode representar uma experiência tão intensa que o narrador parece perder a noção do que acontece ao redor. Se estivéssemos avaliando uma pessoa real, seria importante investigar a frequência e a quantidade do consumo, os prejuízos associados e se existem episódios de apagão alcoólico. Não seria adequado concluir que há dependência apenas pela letra.<br><br>
<b>3: Reforço positivo e associação entre prazer e substâncias</b><br>
Aqui podemos utilizar um conceito da Análise do Comportamento: o reforço positivo. O reforço positivo acontece quando uma consequência agradável aumenta a probabilidade de um comportamento voltar a acontecer.<br><br>
Imagine a seguinte situação: o indivíduo consome álcool ou outra substância, sente euforia, desinibição ou prazer, associa aquela experiência a uma situação agradável, como estar com alguém de quem gosta, e passa a ter maior motivação para repetir a combinação destas experiências. Com o tempo, determinados estímulos podem adquirir valor motivacional. Uma festa, uma música, um lugar ou até a presença de uma pessoa podem despertar a vontade de consumir novamente. Isso é particularmente relevante na música porque o narrador associa repetidamente a intoxicação à presença da pessoa amada. É possível pensar em um processo de aprendizagem no qual o consumo e a experiência afetiva passam a estar fortemente associados.<br><br>
<b>4: Desinibição e perda de controle emocional</b><br>
No segundo verso, Zayn diz: “Right now, I'm emotional / I lose control when I'm with you”. He afirma estar emocionalmente vulnerável e perder o controle quando está com aquela pessoa. Podemos relacionar isso à desinibição comportamental.<br><br>
O álcool, por exemplo, pode prejudicar o funcionamento de processos cognitivos responsáveis por avaliar consequências, controlar impulsos e regular comportamentos. Assim, uma pessoa intoxicada pode: falar coisas que normalmente evitaria, expressar sentimentos com maior intensidade, tomar decisões impulsivas, ter dificuldade para avaliar situações e demonstrar emoções de maneira menos controlada. Mas existe outra possibilidade: he não está necessariamente perdendo o controle apenas por estar intoxicado. A presença daquela pessoa também pode despertar emoções que he tem dificuldade para administrar. Essa distinção seria importante em uma investigação psicológica: o que está relacionado aos efeitos da substância e o que está relacionado ao vínculo afetivo?<br><br>
<b>5: Vulnerabilidade emocional</b><br>
Outro trecho interessante é: “I hope I haven't said too much / Guess I always push my luck when I'm with you”. He espera não ter falado demais e reconhece que costuma arriscar mais do que deveria quando está com a pessoa. Isso pode ser interpretado pela perspectiva da vulnerabilidade emocional. Quando gostamos de alguém, podemos sentir medo de demonstrar sentimentos em excesso, parecer inconvenientes ou revelar algo que preferiríamos manter em segredo. Existe uma tensão entre dois movimentos: Aproximação: vontade de demonstrar carinho, revelar sentimentos e criar intimidade; e autoproteção: receio de rejeição, julgamento ou exposição emocional. O narrador parece oscilar entre estes movimentos. He quer se aproximar, mas também demonstra preocupação com aquilo que pode ter revelado. A intoxicação pode intensificar esta exposição, mas não necessariamente explica toda a vulnerabilidade presente na relação.<br><br>
<b>6: A idealização da experiência amorosa</b><br>
A comparação entre estar apaixonado e estar intoxicado também permite discutir a idealização romântica. Na paixão, principalmente em fases iniciais, existe uma tendência possível de atribuir grande importância à pessoa desejada e às experiências vividas com ela. A presença dessa pessoa pode parecer transformar completamente o ambiente, os acontecimentos e até a percepção que temos de nós mesmos. Na música, o narrador descreve uma experiência em que tudo parece girar em torno da outra pessoa: as noites, as festas, as bebidas e a sensação de euforia. Uma questão interessante seria investigar se he está apaixonado pela pessoa em sua totalidade ou também pela sensação que experimenta quando está ao lado dela. São coisas diferentes. É possível desenvolver uma relação com alguém e, ao mesmo tempo, ficar muito ligado à intensidade emocional que essa pessoa proporciona.<br><br>
<b>O TRABALHO DO PSICÓLOGO</b><br><br>
Se uma pessoa chegasse à clínica relatando uma rotina semelhante à descrita na música, o psicólogo não partiria imediatamente da conclusão de que ela tem dependência química ou está vivendo um relacionamento disfuncional. Primeiro, investigaria o contexto.<br><br>
• <b>Terapia Cognitivo-Comportamental (TCC):</b> Identificaria situações, pensamentos e emoções associados ao consumo, trabalhando padrões de comportamento e estratégias de enfrentamento.<br>
• <b>Análise do Comportamento:</b> Investigaria os antecedentes e as consequências do consumo, identificando os reforçadores que mantêm esse comportamento.<br>
• <b>Terapia de Aceitação e Compromisso (ACT):</b> Trabalharia a relação com emoções intensas, impulsividade, esquiva emocional e escolhas alinhadas aos valores pessoais.<br>
• <b>Entrevista Motivacional:</b> Exploraria a ambivalência em relação ao consumo, ajudando a pessoa a reconhecer possíveis prejuízos e suas próprias motivações para mudar.<br><br>
Também seria importante avaliar possíveis consequências do consumo na vida afetiva, acadêmica, profissional e social.""",
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
Ouvi falar de quantos caminhos percorreu
Só pra ter que começar de novo
Ouvi falar de tudo o que você passou
E parece que você precisa de um amigo, de alguém

Por favor, não espere
Não vou voltar pra casa esta noite
Eu quero te amar
Mas não consigo

Desde que você
Olhe nos meus olhos
Eu vou aonde você estiver
E vou seguir seus passos

Ouvi falar de tudo o que você fez
E de todas as batalhas que enfrentou
Ouvi falar de todo amor que você perdeu
Tudo acabou antes mesmo de começar
Ouvi falar de quantos caminhos percorreu
Só pra ter que começar de novo
Ouvi falar de tudo o que você passou
E parece que você precisa de um amigo, de alguém

Nunca duvidei de mim mesmo
Mas duvidei de você
Cansei de me olhar
Pelo retrovisor

Ouvi falar de tudo o que você fez
E de todas as batalhas que enfrentou
Ouvi falar de todo amor que você perdeu
Tudo acabou antes mesmo de começar
Ouvi falar de quantos caminhos percorreu
Só pra ter que começar de novo
Ouvi falar de tudo o que você passou
E parece que você precisa de um amigo, de alguém""",
        "curiosidades_lista": [
            "🪞 <b>1. UMA CONVERSA COM O PRÓPRIO REFLEXO:</b> Em seu livro autobiográfico, Zayn explicou que 'Rear View' foi construída como uma espécie de reflexão diante do espelho. He conversou com o produtor Malay sobre o que estava sentindo naquele período e sobre a experiência de seguir carreira solo, parecendo conversar consigo mesmo para compreender suas escolhas e sentimentos.",
            "🚗 <b>2. O SIGNIFICADO SIMBÓLICO DO RETROVISOR:</b> O título significa 'retrovisor', que serve justamente para olhar aquilo que ficou para trás enquanto continuamos seguindo em frente. Psicologicamente, a música traduz a exaustão de olhar para o próprio passado, revisitar experiências e perceber que é preciso parar de viver em função do que já aconteceu (como he diz no trecho em que está cansado de se olhar pelo retrovisor).",
            "🎤 <b>3. A POSSÍVEL REFERÊNCIA AO ONE DIRECTION:</b> Lançada em 2016 no álbum <i>Mind of Mine</i> (seu debut solo pós-1D), críticos e revistas como a <i>Teen Vogue</i> relacionaram versos sobre perdas, guerras e recomeços ao fim daquela fase intensa da sua vida, marcando o peso de deixar algo gigante para trás.",
            "🥀 <b>4. A CONTRADIÇÃO EMOCIONAL:</b> Existe uma oposição super marcante na letra entre a disposição de acompanhar alguém ('I'll go wherever you are, I'll follow behind') e o reconhecimento doloroso de que não consegue amar ('I wanna love you, but I can't'). Se pensarmos que he conversa com o próprio reflexo, revela-se alguém que deseja se acolher, mas ainda trava ao lidar com as próprias cicatrizes."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — REAR VIEW</b><br><br>
A psicologia poderia trabalhar <b>rEaR vIeW</b>, do Zayn, a partir de temas como autoconhecimento, conflitos internos, autoestima, experiências afetivas anteriores, dificuldade de seguir em frente e necessidade de acolhimento emocional. O interessante dessa música é que ela permite duas interpretações: a de alguém que tenta acolher uma pessoa marcada por experiências difíceis e a de alguém que está, na verdade, conversando consigo mesmo.<br><br>
<b>1. O retrovisor e a ruminação</b><br>
O próprio título, <i>rEaR vIeW</i> (retrovisor), funciona como uma metáfora para olhar constantemente para aquilo que ficou para trás. Na psicologia, podemos relacionar isso à ruminação, um processo caracterizado pela repetição de pensamentos sobre experiências, problemas, sentimentos e acontecimentos passados. Uma pessoa que apresenta padrões de ruminação pode:<br>
• relembrar constantemente situações que provocaram sofrimento;<br>
• questionar decisões que tomou;<br>
• imaginar como as coisas poderiam ter acontecido de outra maneira;<br>
• ter dificuldade para direcionar a atenção ao presente;<br>
• reinterpretar experiências antigas repetidamente, sem chegar a uma solução.<br>
Por exemplo, alguém que passou por um relacionamento frustrado pode continuar pensando no que fez de errado, no que poderia ter evitado e no motivo pelo qual a relação não funcionou. O problema não está em recordar o passado; a reflexão pode ser importante para o aprendizado. A dificuldade aparece quando a pessoa fica presa a esses pensamentos e eles começam a prejudicar sua vida atual.<br><br>
<b>2. Autoconceito e confiança interpessoal</b><br>
Um dos trechos mais interessantes é: <i>“I never doubted myself / But I doubted you”</i> ("Nunca duvidei de mim mesmo, mas duvidei de você"). Essa passagem pode ser relacionada ao conceito de autoconceito, que diz respeito ao conjunto de percepções, crenças e avaliações que uma pessoa possui sobre si mesma. Uma pessoa pode ter uma percepção relativamente estável de quem é, mas apresentar inseguranças quando suas relações interpessoais são colocadas à prova. Por exemplo:<br>
• Confiar nas próprias capacidades, mas não confiar nas intenções de outra pessoa;<br>
• Ter segurança sobre suas escolhas, mas questionar as escolhas de alguém próximo;<br>
• Sentir que conhece a si mesmo, mas não compreender o comportamento de alguém importante.<br>
Isso também permite discutir a confiança interpessoal. A confiança não depende apenas da autoestima; ela envolve experiências anteriores, expectativas, percepção de segurança e comportamentos observados nas relações. O verso sugere uma contradição: o narrador parece seguro de si, mas reconhece que teve dificuldades para confiar em outra pessoa.<br><br>
<b>3. Modelos internos de funcionamento e bagagem emocional</b><br>
O refrão apresenta alguém que passou por muitas experiências, enfrentou conflitos, perdeu amores e precisou recomeçar diversas vezes. Podemos relacionar isso aos modelos internos de funcionamento, conceito desenvolvido por John Bowlby na Teoria do Apego. Esses modelos são representações mentais construídas a partir das experiências de relacionamento, especialmente nas primeiras relações de cuidado. Eles influenciam a maneira como uma pessoa percebe a si mesma, os outros e a disponibilidade de afeto nas relações. Por exemplo, alguém que vivenciou repetidas experiências de rejeição pode desenvolver expectativas de que será abandonado ou de que não é digno de amor. Isso não significa que todas as pessoas que sofreram rejeições desenvolverão insegurança afetiva, pois experiências posteriores também podem modificar essas expectativas. Na música, os relacionamentos anteriores aparecem como uma espécie de bagagem emocional. A pessoa parece ter passado por tantas situações difíceis que talvez esteja cansada de tentar novamente. A psicologia investigaria se essas experiências influenciam a maneira como ela estabelece novos vínculos.<br><br>
<b>4. Apoio social e a necessidade de um amigo</b><br>
Um dos versos mais significativos é: <i>“And it sounds like you need a friend, a friend.”</i> ("E parece que você precisa de um amigo, de alguém."). Aqui podemos trabalhar o conceito de apoio social. O apoio social envolve a percepção de que existem pessoas disponíveis para oferecer ajuda, compreensão, orientação e acolhimento, assumindo diferentes formas:<br>
• <b>Apoio emocional:</b> receber carinho, compreensão e escuta;<br>
• <b>Apoio instrumental:</b> receber ajuda prática diante de uma dificuldade;<br>
• <b>Apoio informacional:</b> receber orientações e conselhos;<br>
• <b>Apoio de pertencimento:</b> sentir-se incluído e parte de um grupo.<br>
A personagem da música parece carregar uma história de perdas e dificuldades. O narrador reconhece que talvez ela não precise necessariamente de um relacionamento amoroso naquele momento, mas de alguém que esteja disposto a ouvi-la. Isso traz uma questão interessante: nem toda necessidade de afeto é uma necessidade romântica. Às vezes, o que uma pessoa mais precisa é de segurança emocional, companhia e a sensação de que não precisa enfrentar tudo sozinha.<br><br>
<b>5. Ambivalência afetiva</b><br>
O segundo verso apresenta uma contradição: <i>“I wanna love you / But I can't.”</i> ("Eu quero te amar, mas não consigo."). Esse trecho permite discutir a ambivalência afetiva. A ambivalência acontece quando sentimentos, desejos ou tendências diferentes coexistem em relação à mesma pessoa ou situação. No contexto dos relacionamentos, alguém pode:<br>
• desejar intimidade, mas ter medo de se envolver;<br>
• sentir carinho, mas não conseguir oferecer disponibilidade emocional;<br>
• querer permanecer em uma relação, mas perceber que não está preparado;<br>
• sentir atração, mas reconhecer incompatibilidades.<br>
Uma pessoa pode gostar de alguém e ainda assim não conseguir sustentar um relacionamento. É importante não interpretar automaticamente essa dificuldade como medo de compromisso ou estilo de apego evitativo, pois existem diversas explicações possíveis, como circunstâncias pessoais, conflitos internos, falta de disponibilidade ou incompatibilidade. Na psicoterapia, seria importante compreender o que significa esse "não consigo".<br><br>
<b>6. Identidade narrativa e o fim do retrovisor</b><br>
Se considerarmos a interpretação de que Zayn está conversando consigo mesmo, surge uma possibilidade ainda mais interessante. O trecho <i>“I'm tired of looking at myself in my rear view”</i> ("Estou cansado de me olhar pelo retrovisor") pode representar o esgotamento de uma pessoa que está constantemente revisitando a própria história. Isso pode ser relacionado à identidade narrativa, conceito estudado na psicologia da personalidade. A identidade narrativa é a maneira como organizamos nossas experiências em uma história sobre quem somos. Não somos constituídos apenas pelo que aconteceu conosco, mas também pela maneira como interpretamos esses acontecimentos e incorporamos essas experiências à nossa percepção de identidade. Por exemplo, duas pessoas podem passar por experiências semelhantes de rejeição, mas construir narrativas diferentes: uma pode interpretar a experiência como prova de que não merece ser amada, enquanto outra pode compreender que aquela relação não funcionou, mas que isso não determina seu valor pessoal. A experiência é importante, mas a interpretação que construímos sobre ela também influencia a maneira como seguimos em frente. Nesse sentido, deixar de olhar constantemente pelo retrovisor não significa apagar o passado; significa conseguir reconhecer o que aconteceu sem permitir que todas as experiências anteriores determinem quem somos hoje.""",
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
Quatro letras nunca foram a questão
Ela gosta quando sou desleixado
E eu gosto quando ela tira a roupa

Você está procurando meu amor no lugar errado
Não pense que só porque está comigo, isso é de verdade
Você está procurando meu amor no lugar errado
Não pare o que está fazendo, porque eu gosto do seu jeito

Estou aqui com você porque sua energia combina comigo
Parece que você também tem uma boa cabeça
Mas tudo precisa acontecer na hora certa
A gente só combina durante a noite
Eu percebo o tipo de coisa que você tenta esconder, amor, gosto de te agradar
Faço de tudo para te tratar bem, mas não posso te ensinar a amar
Porque sou cheio de problemas, sei muito bem quem sou e não sou boa companhia
Você pode me ter esta noite ou nunca mais, pensei que tivesse entendido
Amor, algumas pessoas nasceram para ser amadas, outras só sabem aproveitar o momento
Então aceite o que estou disposto a oferecer e goste ou não

Você está procurando meu amor no lugar errado
Não pense que só porque está comigo, isso é de verdade
Você está procurando meu amor no lugar errado
Não pare o que está fazendo, porque eu gosto do seu jeito

Não pare o que está fazendo, o que está fazendo
Não pare o que está fazendo, não pare

Eu não, eu realmente não sei
Eu não, eu realmente não me importo
Talvez seja melhor manter isso em segredo
Há histórias que não quero contar

Você está procurando meu amor no lugar errado
Não pense que só porque está comigo, isso é de verdade
Você está procurando meu amor no lugar errado
Não pare o que está fazendo, porque eu gosto do seu jeito

Você está procurando meu amor no lugar errado
Não pense que só porque está comigo, isso é de verdade
Você está procurando meu amor no lugar errado
Não pare o que está fazendo, porque eu gosto do seu jeito""",
        "curiosidades_lista": [
            "🔥 <b>A QUÍMICA DE MILHÕES:</b> 'wRoNg' traz uma parceria impecável com a cantora Kehlani, unindo vocais R&B super suaves a uma letra crua sobre desejo noturno e expectativas desalinhadas.",
            "🕶️ <b>O CONFLITO DO TÍTULO:</b> A letra fala diretamente sobre querer alguém sem oferecer amor, e o título <i>Wrong</i> ('Errado') resume bem esse conflito. O personagem percebe que a outra pessoa está procurando amor nele, mas sabe que não pode oferecer aquilo que ela deseja. Mesmo assim, quer continuar tendo intimidade com ela.",
            "⚖️ <b>EXPECTATIVAS DESALINHADAS:</b> É uma relação marcada por uma diferença nítida de expectativas: enquanto uma pessoa parece querer algo mais profundo e duradouro, a outra está interessada principalmente no prazer e na companhia daquele momento exato.",
            "🎯 <b>PROCURANDO NO LUGAR ERRADO:</b> Uma das ideias centrais e mais marcantes da música é exatamente o aviso direto: <i>'Você está procurando meu amor no lugar errado.'</i> Não espere romance onde há apenas a intensidade do agora!"
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — WRONG</b><br><br>
A psicologia poderia trabalhar <b>Wrong</b> a partir de um conflito muito interessante: o desejo de intimidade sem a disposição ou a capacidade de construir um vínculo afetivo na mesma intensidade que a outra pessoa. A música apresenta alguém que sente atração, gosta da companhia da outra pessoa e quer continuar tendo contato físico e sexual com ela. Entretanto, deixa claro que não pretende oferecer o amor que ela parece procurar. O ponto central não é necessariamente que o personagem seja incapaz de amar. É que existe uma diferença entre aquilo que ele deseja receber de uma relação e aquilo que está disposto a oferecer.<br><br>
<b>1. Indisponibilidade emocional e intimidade</b><br>
Uma das primeiras questões seria investigar a indisponibilidade emocional do personagem. Ele demonstra abertura para a intimidade física, mas estabelece um limite quando a relação começa a envolver sentimentos e expectativas afetivas.<br>
Isto é interessante porque intimidade não é uma coisa só. Podemos distinguir:<br>
• <b>Intimidade física:</b> desejo, contato corporal e sexualidade.<br>
• <b>Intimidade emocional:</b> compartilhar sentimentos, vulnerabilidades e experiências pessoais.<br>
• <b>Intimidade afetiva:</b> desenvolver carinho, compromisso, reciprocidade e investimento no vínculo.<br>
O personagem parece confortável com a primeira, mas não demonstra a mesma disposição para as outras. Na psicologia, seria importante investigar o motivo: ele não deseja um relacionamento naquele momento? Tem medo de se envolver? Não sente pela outra pessoa o mesmo que ela sente? Ou simplesmente prefere relações sem compromisso?<br><br>
<b>2. Teoria do apego: aproximação e distanciamento</b><br>
A teoria do apego, desenvolvida por John Bowlby, também oferece uma perspectiva interessante. Na vida adulta, experiências anteriores de vínculo podem influenciar a maneira como uma pessoa lida com proximidade, confiança, dependência e intimidade.<br>
O personagem poderia apresentar características compatíveis com um padrão de apego evitativo, especialmente se existisse um desconforto persistente diante da dependência emocional e de relações mais profundas. Poderíamos observar:<br>
• Preferência por manter autonomia e controle.<br>
• Desconforto quando a outra pessoa espera maior envolvimento.<br>
• Tendência a estabelecer limites quando a relação começa a ficar emocionalmente próxima.<br>
• Maior facilidade para manter relações físicas do que para compartilhar vulnerabilidades.<br>
Mas existe uma ressalva importante: não querer um relacionamento não significa ter apego evitativo. Uma pessoa pode estar emocionalmente disponível, compreender seus sentimentos e simplesmente não querer construir um compromisso com alguém específico. Portanto, seria necessário investigar o padrão de comportamento ao longo de diferentes relações, e não apenas interpretar uma música.<br><br>
<b>3. Reforço positivo e comportamento sexual</b><br>
A análise comportamental também ajudaria a compreender por que o personagem deseja continuar naquela relação, mesmo sabendo que existe uma diferença de expectativas.<br>
Pense na dinâmica:<br>
1. Ele encontra alguém por quem sente atração.<br>
2. A aproximação proporciona prazer, satisfação sexual e companhia.<br>
3. Essas experiências agradáveis aumentam a probabilidade de he procurar novamente aquela pessoa.<br>
4. Quando surgem cobranças ou expectativas emocionais, he pode se afastar para evitar o desconforto. Nesse cenário, o contato físico funciona como uma fonte de reforço positivo, enquanto o afastamento pode funcionar como uma maneira de escapar de situações emocionalmente desconfortáveis. Isso não significa que he esteja manipulando conscientemente a outra pessoa. O comportamento pode ser mantido pelas consequências que produz, mesmo sem uma intenção deliberada.<br><br>
<b>4. Dissonância cognitiva: querer alguém, mas não querer se envolver</b><br>
A teoria da dissonância cognitiva, de Leon Festinger, também pode ser aplicada. A dissonância acontece quando uma pessoa experimenta pensamentos, atitudes ou comportamentos que entram em conflito.<br>
No caso da música, poderíamos imaginar uma contradição:<br>
• Ele gosta da companhia daquela pessoa.<br>
• Deseja continuar tendo relações com ela.<br>
• Percebe que ela pode querer algo mais profundo.<br>
• Sabe que não pretende oferecer esse envolvimento.<br>
Existe uma tensão entre querer manter a proximidade e reconhecer que essa proximidade pode alimentar expectativas que ele não deseja corresponder. Uma maneira de reduzir este desconforto é estabelecer verbalmente seus limites: ele avisa que não pode oferecer amor. Isso pode ser uma forma legítima de comunicação, mas não elimina automaticamente as consequências emocionais da relação.<br><br>
<b>5. A perspectiva da outra pessoa: expectativas e sofrimento emocional</b><br>
É importante não analisar apenas quem está dizendo que não quer amar. A outra pessoa também ocupa uma posição importante nessa dinâmica. Imagine alguém que começa uma relação casual, mas desenvolve sentimentos. A pessoa pode interpretar os momentos de carinho, intimidade e atenção como sinais de que existe uma possibilidade de relacionamento. Quando percebe que o outro não deseja a mesma coisa, pode experimentar:<br>
• Frustração por expectativas não correspondidas.<br>
• Ansiedade diante da incerteza.<br>
• Sensação de rejeição.<br>
• Dificuldade para interromper uma relação que ainda proporciona prazer.<br>
• Esperança de que o outro mude de ideia.<br>
Aqui existe uma questão importante: a pessoa pode continuar recebendo recompensas emocionais e físicas suficientes para permanecer na relação, mesmo que suas necessidades afetivas não estejam sendo atendidas.<br><br>
<b>6. O aspecto psicológico mais interessante de Wrong</b><br>
Para mim, a música apresenta três elementos que merecem ser diferenciados:<br>
• <b>Desejo:</b> he sente atração e quer continuar tendo aquela pessoa por perto.<br>
• <b>Disponibilidade emocional:</b> não demonstra interesse em oferecer um vínculo amoroso.<br>
• <b>Responsabilidade afetiva:</b> he reconhece que a outra pessoa pode estar procurando algo que he não pretende oferecer.<br>
A última dimensão é especialmente interessante. Ser honesto sobre não querer um relacionamento é importante, mas responsabilidade afetiva também envolve considerar como as próprias atitudes podem alimentar expectativas. Uma pessoa pode dizer que não quer compromisso e, ainda assim, manter comportamentos contraditórios que dificultam o afastamento da outra.""",
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
E por tudo, por tudo que você faz
Tudo que você faz
Tudo que você faz

Quando você fica assim
Eu simplesmente não consigo resistir
Eu sei, às vezes eu escondo o que sinto
Mas dessa vez não consigo
Porque isso vai acabar comigo
Mas você não vai acreditar em mim
Acredita em mim

Porque eu sou um bobo por você
E por tudo que você faz
Eu sou um bobo por você
E por tudo, por tudo que você faz

Eu sei, eu sei
Se tivesse a chance, eu faria tudo de novo, ah
Porque eu não consigo evitar
Porque eu não consigo me controlar
Eu simplesmente adoro ser um bobo por você

Porque eu sou um bobo por você
E por tudo que você faz
Eu sou um bobo por você
E por tudo, por tudo que você faz""",
        "curiosidades_lista": [
            "🎸 <b>A INFLUÊNCIA CLÁSSICA DOS BEATLES:</b> Em sua autobiografia, Zayn contou que estava ouvindo muito Beatles durante a produção de <i>Mind of Mine</i>, revelando que os acordes de piano no começo de 'Fool for You' e as guitarras foram diretamente inspirados por esse som. Críticos de portais como o <i>Drowned in Sound</i> descreveram a faixa como uma verdadeira balada à la Beatles pela combinação marcante de piano, bateria e vocais dramáticos.",
            "🎯 <b>O DESAFIO DE ESCOLHER ENTRE 48 MÚSICAS:</b> Zayn revelou que gravou nada menos do que 48 faixas durante todo o processo de criação de <i>Mind of Mine</i>. Por causa disso, ele teve uma dificuldade enorme para selecionar quais entrariam no álbum, fazendo de 'Fool for You' uma escolha muito especial para o projeto.",
            "🎛️ <b>O CONTRASTE COM O R&B:</b> Enquanto o restante de <i>Mind of Mine</i> mergulha profundamente no R&B contemporâneo, no soul, no hip-hop e em sonoridades atmosféricas, 'Fool for You' ganha destaque justamente por trazer essa sonoridade acústica e orgânica.",
            "🥀 <b>O CICLO DA PERDA DE CONTROLE:</b> A letra inteira traça um caminho psicológico inevitável: <i>'Eu preciso de você e odeio isso'</i> ➔ <i>'Não consigo resistir'</i> ➔ <i>'Às vezes escondo o que sinto, mas dessa vez não consigo'</i> ➔ <i>'Isso vai acabar comigo'</i>. No final, há uma reviravolta quase irônica e apaixonada: mesmo sabendo dos riscos, ele conclui: <i>'Eu faria tudo de novo'</i> e <i>'Eu simplesmente adoro ser um bobo por você'</i>."
        ],
        "psicologia": """🧠 <b>ANÁLISE COMPORTAMENTAL — FOOL FOR YOU</b><br><br>
<b>1. A Rendição Emocional e a Perda de Controle</b><br>
"Eu preciso de você e odeio isso / Porque eu não consigo evitar, porque eu não consigo me controlar"<br>
Psicologicamente, a música retrata o conflito entre o desejo de autonomia e a força avassaladora de um apego apaixonado. Admitir ser um "bobo" por alguém envolve baixar todas as defesas psicológicas, o que gera uma ambivalência dolorosa: ao mesmo tempo em que a conexão traz uma sensação mágica ("entre um sonho e uma cena de filme"), ela também desperta o medo de se machucar ("porque isso vai acabar comigo").<br><br>
<b>2. O Ciclo da Vulnerabilidade e da Repetição</b><br>
"Se tivesse a chance, eu faria tudo de novo"<br>
Mesmo reconhecendo o risco e o sofrimento potencial ("odeio precisar de você"), o eu lírico escolhe reentrar no ciclo de vulnerabilidade. Na psicologia dos relacionamentos, isso demonstra como o reforço emocional de uma paixão intensa muitas vezes supera o medo racional da dor, perpetuando vínculos profundos e difíceis de romper.""",
        "link_clipe": "https://www.youtube.com/watch?v=yM2Gaxg1O28&list=RDyM2Gaxg1O28&start_radio=1"
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
    if "wrong" in t.lower() or "fool for you" in t.lower():
        return None
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
        .container {
            max-width: 2050px;
            margin: 0 auto;
        }
        .site-header {
            text-align: center;
            margin-bottom: 35px;
        }
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
        .track-info {
            flex: 1;
        }
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
            transition: transform 0.1s;
        }
        .clipe-btn:hover {
            transform: translate(-3px, -3px);
            box-shadow: 6px 6px 0px #2c2c2c;
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
        .column-side {
            display: flex;
            flex-direction: column;
            gap: 45px;
        }
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
        ::-webkit-scrollbar { width: 16px; }
        ::-webkit-scrollbar-track { background: #FFFDF9; }
        ::-webkit-scrollbar-thumb { background: #d6b8c4; border-radius: 8px; border: 3.5px solid #2c2c2c; }
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

@app.route("/api/now-playing")
def now_playing():
    global last_saved_id
    try:
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
    except:
        pass
    return jsonify({"playing": False})

if __name__ == "__main__":
    print("\n✨ Seu site está no ar! Abra no navegador: http://127.0.0.1:5000 ✨\n")
    app.run(port=5000)