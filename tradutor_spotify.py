import os
import uuid
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, jsonify, redirect, request, session, render_template_string

ID = os.getenv("SPOTIPY_CLIENT_ID", "51ebc5fc21fa4e359bebdd37175c9f13")[cite: 1]
SEC = os.getenv("SPOTIPY_CLIENT_SECRET", "8670dd178bb0463086bdbda323dc889f")[cite: 1]
URI = os.getenv("SPOTIPY_REDIRECT_URI", "http://127.0.0.1:5000/callback")[cite: 1]
SCOPES = "user-read-playback-state user-read-currently-playing"[cite: 1]

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
Quando precisar de companhia"""[cite: 1]

CURIOSIDADES_WHO = [
    "🎬 <b>TRILHA DE GHOSTBUSTERS (2016) & ESTILO DO TÍTULO:</b> A música foi escrita para o filme <i>Ghostbusters</i>, de 2016, e recebeu o título de “WHo”, com algumas letras maiúsculas e outras minúsculas. Essa forma de escrever segue o mesmo estilo que ZAYN vinha usando nos títulos de suas músicas alguns meses antes, no álbum <i>Mind of Mine</i>, lançado em março de 2016.",
    "👻 <b>REFERÊNCIA COM NOVO SENTIDO:</b> Aqui, ZAYN faz uma referência à famosa música-tema do <i>Ghostbusters</i> original, composta e interpretada por Ray Parker Jr., mas dá a ela um sentido um pouco diferente. Em vez de simplesmente repetir a ideia da canção original, ele pergunta à pessoa para quem canta quem ela vai procurar quando estiver em apuros ou se sentir sozinha. Ao longo dos versos, ele tenta mostrar que essa pessoa deveria procurá-lo, deixando claro que está disposto a aparecer e ajudá-la quando ela mais precisar."
][cite: 1]

PSICOLOGIA_WHO = """🧠 <b>ANÁLISE PSICOLÓGICA — WHO</b><br><br>
A música “WHo” trabalha uma ideia psicológica bastante interessante: a necessidade de ter alguém em quem confiar quando a vida se torna difícil. Mais do que perguntar quem a outra pessoa vai procurar nos momentos de desespero, o narrador tenta se apresentar como essa figura de segurança. Ele não oferece apenas companhia; promete proteção, proximidade e disponibilidade emocional. Isso faz com que a canção possa ser interpretada como uma tentativa de construir um vínculo no qual uma pessoa se torna o ponto de apoio da outra.<br><br>
<b>1. Vulnerabilidade e base segura</b><br>
O primeiro aspecto importante é a representação da vulnerabilidade. As imagens de escuridão, dificuldade para encontrar um caminho e pressão excessiva funcionam como metáforas para momentos de desorientação emocional. Psicologicamente, elas remetem a situações em que alguém sente que perdeu o controle, não consegue encontrar soluções ou está sobrecarregado pelas próprias circunstâncias. Nesses momentos, a presença de outra pessoa pode oferecer uma sensação de estabilidade. A música parece compreender que, quando alguém está fragilizado, nem sempre precisa de respostas imediatas: às vezes, precisa saber que não enfrentará tudo sozinho.<br><br>
Isso se relaciona com a ideia de base segura, desenvolvida na teoria do apego de John Bowlby. Em vínculos afetivos, uma figura de apego pode funcionar como uma referência de proteção, alguém a quem recorremos quando sentimos medo, insegurança ou sofrimento. Quando o narrador diz que irá até a pessoa e que ela sabe que ele vai salvá-la, ele se coloca justamente nessa posição: a de alguém que deseja ser percebido como confiável e acessível nos momentos de necessidade. É importante, porém, distinguir a interpretação da letra de uma relação real: a música apresenta uma promessa de proteção, mas não permite concluir como esse vínculo funcionaria na prática.<br><br>
<b>2. Disponibilidade emocional, pertencimento e repetição</b><br>
Outro ponto relevante é a maneira como a música constrói a ideia de disponibilidade emocional. A pergunta repetida — quem você vai chamar quando precisar de alguém? — não parece ser apenas uma pergunta sobre ajuda prática. Existe uma dimensão afetiva nela: o narrador quer ocupar um lugar específico na vida daquela pessoa. Ele não quer ser simplesmente alguém que aparece ocasionalmente, mas alguém que seja lembrado espontaneamente quando as coisas dão errado. Isso revela uma busca por importância emocional, pelo desejo de ser reconhecido como alguém indispensável ou, pelo menos, profundamente significativo.<br><br>
Essa necessidade também pode ser compreendida pela perspectiva do pertencimento. Os seres humanos possuem uma necessidade psicológica de estabelecer vínculos nos quais se sintam aceitos, valorizados e necessários. Na música, entretanto, essa necessidade aparece direcionada para o outro: o narrador tenta demonstrar que pode oferecer aquilo de que a pessoa precisa. Existe uma espécie de reivindicação afetiva implícita: quando você estiver vulnerável, quero que seja a mim que você procure. Ele deseja ser escolhido justamente nos momentos de necessidade.<br><br>
A repetição da pergunta também merece atenção. Musicalmente, ela reforça o tema central, mas, em uma leitura psicológica, pode ser interpretada como uma tentativa de fixar uma ideia na mente da outra pessoa. O narrador não pergunta uma única vez; insiste na questão de quem será procurado. Essa insistência pode transmitir segurança e convicção, como se ele já soubesse que é a pessoa certa para ocupar esse lugar. Ao mesmo tempo, pode sugerir uma necessidade de confirmação: não basta estar disponível, ele quer que o outro reconheça sua disponibilidade e o escolha.<br><br>
<b>3. Cuidado, reconhecimento e responsabilidade emocional</b><br>
Há ainda uma diferença interessante entre oferecer ajuda e desejar ser aquele que oferece ajuda. A primeira atitude está relacionada ao cuidado; a segunda pode envolver também uma necessidade de reconhecimento. Quando alguém deseja muito ser a pessoa que salva outra, pode existir uma mistura de afeto genuíno com o desejo de se sentir importante na vida dela. Isso não significa que o cuidado seja falso ou calculado. Significa apenas que, nas relações humanas, o desejo de ajudar nem sempre está completamente separado da vontade de ser valorizado. Na letra, essa ambiguidade permanece aberta: não sabemos se o narrador está simplesmente expressando dedicação ou se também deseja garantir um lugar privilegiado na vida da pessoa.<br><br>
A promessa de salvamento também pode ser analisada pela questão da responsabilidade emocional. Ao dizer que estará presente quando a outra pessoa enfrentar dificuldades, o narrador assume uma posição bastante ativa: ele não espera necessariamente que o outro encontre uma solução sozinho, mas se oferece como parte dessa solução. Isso pode ser acolhedor, porque transmite a ideia de que a vulnerabilidade não será recebida com rejeição. Entretanto, existe uma diferença entre apoiar alguém e assumir o papel de responsável por resolver o sofrimento dessa pessoa. A música trabalha com uma promessa romântica de proteção, não com uma descrição realista dos limites que existem em qualquer relação saudável.<br><br>
<b>4. Imagens de perigo, incerteza e permanência</b><br>
Outro elemento é a maneira como o sofrimento é apresentado por meio de imagens de perigo. A água profunda, o tubarão e a pressão excessiva representam ameaças que parecem maiores do que a capacidade individual de enfrentamento. Essas imagens podem ser entendidas como formas de representar a sensação de estar emocionalmente encurralado. O tubarão, em particular, introduz uma ideia de perseguição: não se trata apenas de estar em uma situação difícil, mas de sentir que alguma coisa ameaça continuamente a própria segurança. Nesse cenário, a figura do narrador aparece como uma possibilidade de proteção contra aquilo que a pessoa não consegue controlar.<br><br>
O trecho em que ele pergunta quem está certo e afirma que estará por perto acrescenta outra camada. A necessidade de saber quem está certo pode remeter a conflitos, dúvidas e situações em que a pessoa não sabe como interpretar o que está acontecendo. O narrador não se oferece apenas para situações de perigo físico ou emocional, mas também para momentos de confusão. Ele parece querer transmitir que sua presença não depende de a outra pessoa estar bem, tranquila ou com todas as respostas. Ele estará próximo mesmo quando houver medo, incerteza e dificuldade para compreender os acontecimentos.<br><br>
A frase sobre se tornar um fantasma caso aquilo acabe é especialmente interessante porque introduz uma possibilidade de perda. Até então, a música constrói a imagem de alguém que estará presente e poderá ser chamado sempre que necessário. Nesse momento, porém, surge a ideia de que alguma coisa pode terminar. O fantasma pode representar aquilo que permanece depois de uma ausência: uma lembrança, uma presença psicológica ou alguém que continua existindo na memória mesmo quando já não faz parte da realidade cotidiana. A interpretação é ambígua, mas cria um contraste importante entre a promessa de proximidade e a possibilidade de desaparecimento.<br><br>
Nesse sentido, a música também toca na relação entre presença e permanência. Uma pessoa pode deixar de estar fisicamente disponível e, ainda assim, continuar ocupando espaço na vida emocional de alguém. Memórias, experiências e vínculos não desaparecem necessariamente quando uma relação termina. A imagem do fantasma transforma essa permanência em algo quase literal: mesmo que a relação deixe de existir, alguma parte dela pode continuar acompanhando a pessoa.<br><br>
<b>5. Atitudes prometidas e lugar de confiança</b><br>
Também é importante observar que a canção não apresenta uma declaração amorosa convencional. O narrador não concentra sua mensagem em dizer que ama alguém, mas em demonstrar que estará disponível quando essa pessoa precisar. Isso desloca a expressão do afeto para o campo das atitudes prometidas. Em vez de afirmar diretamente a intensidade do sentimento, ele tenta convencer o outro de que sua presença tem valor. É uma forma de expressar interesse por meio da proteção, da lealdade e da disponibilidade.<br><br>
No fundo, “WHo” parece falar menos sobre quem alguém chamaria em uma emergência e mais sobre quem deseja ocupar esse lugar de confiança na vida de outra pessoa. O narrador quer ser lembrado quando tudo estiver difícil, quando as soluções parecerem distantes e quando a solidão se tornar mais evidente. Existe ternura nessa oferta de companhia, mas também uma vontade de ser escolhido e reconhecido. A música constrói, assim, uma fantasia afetiva bastante humana: a de ser a pessoa para quem alguém se volta quando não sabe mais a quem recorrer. E talvez sua questão psicológica mais interessante esteja justamente nisso: não querer apenas estar ao lado de alguém, mas desejar ser aquela presença cuja ausência seria sentida e cuja existência representaria segurança."""[cite: 1]

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
Não precisa se jogar de cabeça, não preciso de provas

Linda loucura
Você é como um filme, muda a cena
Sinto o gosto da sua doce indecência
É tudo por uma boa causa, acho que você tá fazendo tudo certo

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
Não precisa se jogar de cabeça, não preciso de provas
Você estava bem no limite

Me dê tudo isso, me dê você por inteiro
Não precisa se jogar de cabeça, não preciso de provas
Me dê tudo isso, me dê você por inteiro
Não precisa se jogar de cabeça, não preciso de provas

Então tira tudo
Vamos derrubar todas as nossas barreiras
Agora eu quero ver tudo, oh-oh
Não quero que essa vontade passe
Então vamos cruzar os limites que deixamos pra trás
Agora eu quero ver tudo, oh-oh

Você estava bem no limite
Me dê tudo isso, me dê você por inteiro
Não precisa se jogar de cabeça, não preciso de provas
Você estava bem no limite
Me dê tudo isso, me dê você por inteiro
Não precisa se jogar de cabeça, não preciso de provas
Você estava bem no limite"""[cite: 1]

TRADUCAO_TIO = """Eu sinto o gosto na sua boca e não consigo largar
Você é louca como eu, não consegue perceber?
A gente pode dar um jeito nisso, eu acredito
Você se excita comigo, é quase como se estivesse traindo

Eu só quero ficar te olhando enquanto você tira
Tira toda a maquiagem, amor, tira tudo
Eu só quero ficar te olhando enquanto você tira
Tira toda a roupa e deixa eu te ver tirando tudo

Tira, tira
Amor, simplesmente tira
Tira, tira
Amor, simplesmente tira

Me encosta contra a parede, não pega leve
Você gosta de intensidade como eu, é disso que você precisa
Vamos ficar nus e descobrir nossos segredos mais íntimos
Se é isso que é, então é isso que é

Eu só quero ficar te olhando enquanto você tira
Tira toda a maquiagem, amor, tira tudo
Eu só quero ficar te olhando enquanto você tira
Tira toda a roupa e deixa eu te ver tirando tudo

Tira, tira
Amor, simplesmente tira
Tira, tira
Amor, simplesmente tira
Tira, tira
Amor, simplesmente tira
Tira, tira
Amor, simplesmente tira

Eu mal posso esperar pra ver tudo
Eu tô tão excitado e agora tudo isso é meu
Eu mal posso esperar pra ver tudo
Eu tô tão excitado

Eu só quero ficar te olhando enquanto você tira
Tira toda a maquiagem, amor, tira tudo
Eu só quero ficar te olhando enquanto você tira
Tira toda a roupa e deixa eu te ver tirando tudo

Eu só quero ficar te olhando enquanto você tira
Tira toda a maquiagem, amor, tira tudo
Eu só quero ficar te olhando enquanto você tira
Tira toda a roupa e deixa eu te ver tirando tudo"""[cite: 1]

TRADUCAO_LIKE_I_WOULD = """Ei, tudo bem? Quanto tempo, né?
Não sou muito de ficar falando dessas coisas
Mas pensei em saber como você tá, enquanto acendo um cigarro
É meio frio da minha parte, eu sei
É meio frio da minha parte

Sei que tá tarde, mas tô a mil
Vi seu rosto e isso me deu vontade
Pelo visto, você deixou tudo pra trás e agora tá seguindo em frente
É meio frio da minha parte, eu sei
É meio frio da minha parte

Ah, ah, provavelmente isso vai soar errado
Mas prometo que não vai demorar
Ah, ah, se a gente nunca mais puder voltar
Achei que você gostaria de saber

Ele não vai te tocar como eu
Não vai te amar como eu amaria
Ele não conhece seu corpo
Não sabe te dar prazer
Não vai te amar como eu amaria
Como eu amaria

Tudo bem você ainda me querer, porque eu também quero você
Pensei bastante sobre isso, mas agora já me decidi
Então para de desperdiçar meu tempo e mexer com a minha cabeça
É meio frio da minha parte, eu sei
É meio frio da minha parte

Ah, ah, provavelmente isso vai soar errado
Mas prometo que não vai demorar
Ah, ah, se a gente nunca mais puder voltar
Achei que você gostaria de saber

Ele não vai te tocar como eu
Não vai te amar como eu amaria
Ele não conhece seu corpo
Não sabe te dar prazer
Não vai te amar como eu amaria
Como eu amaria, como eu amaria

Ele não vai te tocar como eu
Não vai te amar como eu amaria
Ele não conhece seu corpo
Não sabe te dar prazer
Não vai te amar como eu amaria
Como eu amaria, como eu amaria

Ele não consegue, não consegue, não consegue
Te amar como eu amaria
Não consegue te amar como eu poderia
Ele não conhece seu corpo
Não conhece seu corpo

Ele não vai te tocar como eu
Não vai te amar como eu amaria
Ele não conhece seu corpo
Não sabe te dar prazer
Não vai te amar como eu amaria
Como eu amaria, como eu amaria
Ele não consegue te tocar como eu
Não consegue te amar como eu
Ele não conhece seu corpo
Não sabe te dar prazer
Não vai te amar como eu amaria
Como eu amaria, como eu amaria"""[cite: 1]

PSICOLOGIA_LIKE_I_WOULD = """🧠 <b>ANÁLISE COMPORTAMENTAL — LIKE I WOULD</b><br><br>
“Like I Would” apresenta uma situação emocional bastante específica: alguém que, mesmo depois do término de um relacionamento, continua se percebendo como insubstituível na vida da outra pessoa. O eu lírico sabe que sua antiga parceira está com alguém novo, mas não parece aceitar completamente essa realidade. Em vez de simplesmente expressar saudade ou desejar uma reconciliação, ele constrói uma comparação constante entre si e o atual companheiro dela. A mensagem central é que o novo parceiro pode até ocupar seu antigo lugar, mas jamais conseguirá reproduzir aquilo que existia entre os dois. Psicologicamente, essa postura permite explorar questões como rivalidade afetiva, autoestima, ciúme retrospectivo, necessidade de validação, apego, competição e dificuldade de elaborar uma perda.<br><br>
<b>1. Comunicação indireta e autoproteção</b><br>
Logo no início, quando o eu lírico reaparece perguntando como a outra pessoa está, existe uma contradição interessante entre a aparente casualidade do contato e a intensidade emocional que surge posteriormente. Ele começa com uma abordagem descontraída, como alguém que apenas deseja saber notícias depois de muito tempo, mas rapidamente deixa transparecer que sua intenção não é tão inocente. Isso pode ser compreendido pelo conceito de comunicação indireta, quando uma pessoa evita expressar diretamente aquilo que deseja e utiliza uma abordagem aparentemente neutra para testar a receptividade do outro. Em vez de dizer imediatamente que sente falta, que ainda deseja a pessoa ou que gostaria de retomar alguma coisa, ele inicia uma conversa aparentemente despretensiosa. Essa estratégia pode funcionar como uma forma de autoproteção: ao não revelar completamente suas intenções, ele reduz o risco de uma rejeição explícita. Se a outra pessoa demonstrar interesse, existe espaço para avançar; se não demonstrar, ele ainda pode fingir que estava apenas perguntando como ela estava.<br><br>
<b>2. Vulnerabilidade e resistência à exposição emocional</b><br>
A expressão de que não costuma conversar sobre esse tipo de coisa também sugere uma dificuldade em demonstrar vulnerabilidade. Existe uma distância entre o que o personagem sente e aquilo que está disposto a admitir. Essa contradição é psicologicamente relevante porque a vulnerabilidade envolve aceitar a possibilidade de ser emocionalmente afetado pela resposta de alguém. Procurar uma antiga parceira significa reconhecer que ela ainda possui alguma importância, mas admitir isso abertamente também significa se colocar em uma posição na qual pode ser rejeitado. Por isso, a postura aparentemente indiferente pode funcionar como uma defesa contra a exposição emocional. Não necessariamente porque ele não sente, mas porque talvez não queira demonstrar o quanto ainda sente.<br><br>
<b>3. Ambivalência emocional e distanciamento afetivo</b><br>
O comportamento descrito no primeiro verso também pode ser relacionado à ambivalência emocional. O personagem demonstra interesse em restabelecer o contato, mas sua maneira de abordar a situação é marcada por frieza e provocação. Ele parece querer proximidade sem assumir completamente a posição de alguém que está buscando reconciliação. Essa combinação entre aproximação e distanciamento pode ser interpretada como uma tentativa de preservar o controle da situação. Em termos psicológicos, isso se aproxima de estratégias defensivas de racionalização e distanciamento afetivo: em vez de entrar em contato diretamente com a saudade, a insegurança ou o medo de ter sido substituído, ele transforma essas emoções em uma atitude mais provocadora e aparentemente segura. Não é possível afirmar que o personagem utiliza conscientemente essas defesas, mas elas oferecem uma maneira de compreender a contradição apresentada pela letra.<br><br>
<b>4. Memória afetiva e gatilhos de aproximação</b><br>
Um dos aspectos mais interessantes aparece quando ele afirma que viu o rosto da antiga parceira e isso despertou sua vontade de procurá-la. Aqui podemos observar o funcionamento da memória afetiva e dos estímulos associados a experiências emocionais. Uma imagem, uma música, um lugar ou até uma conversa podem reativar lembranças relacionadas a uma pessoa significativa. Essas lembranças não recuperam apenas informações sobre o passado; podem trazer de volta sensações, expectativas e estados emocionais que estavam associados àquela relação. O contato visual, mesmo que aconteça por uma fotografia ou publicação, pode funcionar como um estímulo que reativa o desejo de aproximação. Isso não significa necessariamente que o indivíduo nunca tenha superado o relacionamento. Significa que determinadas experiências afetivas podem continuar emocionalmente acessíveis, mesmo depois de um período de afastamento.<br><br>
<b>5. Substituição afetiva e identidade relacional</b><br>
A frase em que ele reconhece que a outra pessoa aparentemente seguiu em frente introduz uma questão ainda mais profunda: a dificuldade de aceitar a substituição afetiva. O término de um relacionamento não representa apenas a perda de uma pessoa, mas também a perda de uma posição que ocupávamos na vida dela. Antes, o eu lírico era aquele que conhecia sua intimidade, participava de sua rotina e tinha acesso a determinadas formas de carinho. Agora, existe outra pessoa ocupando esse espaço. Essa mudança pode provocar uma ameaça à identidade relacional, isto é, à maneira como alguém compreende a si mesmo dentro de um vínculo. Em vez de ser simplesmente alguém que terminou um relacionamento, ele passa a se confrontar com a possibilidade de ser alguém que já não possui a mesma importância para a antiga parceira. É uma experiência que pode atingir diretamente a autoestima, especialmente quando a pessoa associa seu valor à exclusividade que tinha dentro de aquela relação.<br><br>
<b>6. Comparação social e disputa simbólica</b><br>
É nesse ponto que o refrão ganha sua principal dimensão psicológica. Quando ele afirma repetidamente que o novo parceiro não vai tocá-la, amá-la ou conhecer seu corpo como ele conhecia, a música deixa de ser apenas uma expressão de saudade e se transforma em uma disputa simbólica. O eu lírico não está simplesmente dizendo que sente falta da antiga companheira; está tentando estabelecer uma hierarquia entre ele e o homem que está com ela atualmente. Ele precisa acreditar que aquilo que ofereceu foi superior e que a experiência compartilhada entre os dois não pode ser reproduzida. Essa postura pode ser relacionada à comparação social, conceito desenvolvido por Leon Festinger, segundo o qual as pessoas avaliam aspectos de si mesmas por meio da comparação com outras. Nesse caso, o atual parceiro funciona como um parâmetro de comparação, e o eu lírico tenta preservar uma avaliação positiva de si mesmo colocando-se em uma posição de superioridade.<br><br>
<b>7. Proteção da autoestima e necessidade de validação</b><br>
Essa comparação também pode funcionar como uma forma de proteção da autoestima. Quando alguém é substituído em uma relação, pode surgir a sensação de que outra pessoa foi considerada mais desejável, mais interessante ou mais adequada. Isso pode produzir questionamentos internos sobre o próprio valor. Ao afirmar que o novo companheiro jamais conseguirá oferecer aquilo que ele oferecia, o personagem constrói uma narrativa na qual não foi realmente superado: ele continua sendo a referência, enquanto o outro é apenas alguém que ocupa temporariamente seu lugar. Essa interpretação permite que ele preserve a sensação de importância, mesmo diante de uma situação que pode representar rejeição ou perda. O problema é que essa segurança depende de uma comparação constante com outra pessoa, em vez de estar fundamentada em uma percepção mais estável do próprio valor.<br><br>
<b>8. Ciúme retrospectivo e exclusividade perdida</b><br>
Outro conceito relevante é o ciúme retrospectivo, embora a situação apresentada seja um pouco diferente de sua definição mais comum. O ciúme retrospectivo está relacionado ao desconforto provocado pelas experiências afetivas e sexuais anteriores de um parceiro. Em “Like I Would”, a questão não é exatamente o passado amoroso da mulher, mas a dificuldade do eu lírico em aceitar que ela esteja construindo uma nova experiência íntima com outra pessoa. Ele parece incomodado não apenas com a existência do novo relacionamento, mas com a possibilidade de que o atual parceiro tenha acesso a uma intimidade que antes pertencia a ele. O corpo da antiga companheira se transforma, simbolicamente, em um território de comparação. Por isso, a insistência em afirmar que o outro não conhece seu corpo da mesma maneira revela uma preocupação com a exclusividade perdida. É como se o personagem tentasse preservar uma espécie de autoridade sobre uma intimidade que já não lhe pertence.<br><br>
<b>9. Territorialidade afetiva e intimidade compartilhada</b><br>
Essa questão também pode ser analisada pelo conceito de territorialidade afetiva, entendido aqui como uma interpretação da dificuldade de abandonar posições de exclusividade dentro de um vínculo. Durante um relacionamento, determinadas experiências tornam-se particulares daquele casal: formas de carinho, hábitos, brincadeiras, conhecimentos íntimos e maneiras de demonstrar afeto. Depois do término, essas experiências continuam existindo na memória, mas deixam de representar um direito sobre a outra pessoa. O eu lírico parece ter dificuldade em realizar essa separação. Ele reconhece que a antiga parceira está com alguém novo, mas ainda fala como se tivesse alguma autoridade para determinar quem é capaz de satisfazê-la. Essa contradição revela a diferença entre lembrar de uma intimidade compartilhada e acreditar que ainda se possui algum tipo de exclusividade sobre ela.<br><br>
<b>10. Sexualidade como dimensão da autoestima e comparação</b><br>
Também é interessante observar como a música associa amor e desempenho sexual. Quando o personagem afirma que o outro não sabe tocar o corpo dela nem tratá-la adequadamente, ele utiliza a intimidade física como uma prova de superioridade afetiva."""[cite: 1]

CURIOSIDADES_TIO = [
    "💋 <b>O SIGNIFICADO DE TIO:</b> 'TiO' é abreviação de <i>'Take It Off'</i> ('Tire Tudo'), o pedido central que dá o tom sensual e direto da faixa no álbum <i>Mind of Mine</i>.",
    "🎭 <b>DESPIR AS MÁSCARAS:</b> A letra fala tanto de tirar a roupa quanto de tirar a maquiagem e as defesas — como se o momento de intimidade pedisse que os dois deixassem tudo à mostra sem filtro.",
    "🔥 <b>INTENSO E SEM MEIO-TERMO:</b> Versos sobre intensidade, segredos íntimos e a sensação de quase estar traindo reforçam a atmosfera de atração proibida e entrega imediata da música.",
    "✨ <b>VOCÊ SABIA? A IDEIA ORIGINAL ERA SUPER DIFERENTE:</b> Você sabia? A ideia original de “Take It Off” era bem diferente do resultado final! Inicialmente, a música não seria tão explícita: a proposta era falar sobre tirar as “camadas” de alguém, deixando de lado a maquiagem, as aparências e as máscaras para conhecer sua verdadeira essência. Mas, durante o processo de composição, o conceito acabou tomando outro rumo e ganhou um sentido muito mais sensual e literal. O que começou como uma música sobre descobrir quem alguém realmente é acabou se transformando em uma canção sobre tirar a roupa e explorar a intimidade a dois. O próprio Zayn comentou que achou divertida essa mudança inesperada de significado! 💋💿"
][cite: 1]

PSICOLOGIA_TIO = """🧠 <b>ANÁLISE PSICOLÓGICA DE “TiO”, DO ZAYN</b><br><br>
“TiO” pode ser interpretada, à primeira vista, como uma música essencialmente sobre desejo sexual e atração física. Entretanto, quando consideramos a explicação de ZAYN sobre a ideia original da composição, encontramos uma dimensão psicológica muito mais interessante. A música nasceu da intenção de retirar as camadas de alguém para enxergar sua verdadeira essência, ultrapassando a maquiagem, as aparências e as imagens que construímos para sermos percebidos pelos outros. Posteriormente, essa proposta se transformou em uma narrativa muito mais explícita, centrada na nudez e na intimidade sexual. Essa mudança permite explorar uma questão importante: até que ponto o desejo de conhecer alguém profundamente se confunde com o desejo de viver uma experiência física com essa pessoa?<br><br>
Na Psicologia das relações interpessoais, a intimidade está diretamente relacionada à autorrevelação, conceito que descreve o processo pelo qual compartilhamos informações pessoais e permitimos que alguém conheça aspectos progressivamente mais profundos da nossa identidade. Não se trata apenas de revelar acontecimentos da própria vida, mas também de apresentar inseguranças, desejos, medos e características que normalmente permanecem protegidas. Nesse sentido, a ideia original de “Take It Off” representava uma busca por vulnerabilidade: retirar as camadas simbólicas que separam a imagem pública da identidade particular. A maquiagem, nessa interpretação, funciona como uma metáfora das aparências e das formas de apresentação social que utilizamos para controlar a maneira como somos percebidos. Isso não significa necessariamente falsidade, mas uma maneira de selecionar aquilo que mostramos ao mundo."""[cite: 1]

CURIOSIDADES_BORDESZ = [
    "🚧 <b>O SIGNIFICADO DE BORDERSZ:</b> O título estilizado <i>'BoRdErSz'</i> remete diretamente a fronteiras e limites — tanto no sentido de ultrapassar barreiras quanto de estar no limiar de algo intenso no álbum <i>Mind of Mine</i>.",
    "🌊 <b>MARÉ ALTA E TUMULTO:</b> A letra brinca com imagens de movimento e transformação — como ir para onde o vento sopra, mudar a perspectiva como o oceano e provocar um tumulto compartilhado."
][cite: 1]

PSICOLOGIA_BORDESZ = """🧠 <b>ANÁLISE COMPORTAMENTAL — A PSICOLOGIA POR TRÁS DE “BoRdErSz”, DE ZAYN</b><br><br>
À primeira vista, “BoRdErSz” parece ser uma música essencialmente sobre desejo e atração. Mas, observada com mais atenção, a letra apresenta uma dinâmica psicológica muito mais interessante: a de alguém que se encontra diante de seus próprios limites e decide, pouco a pouco, atravessá-los. O próprio título, que significa “fronteiras” ou “limites”, funciona como uma espécie de chave para compreender toda a música."""[cite: 1]

TRADUCAO_CRUEL = """O rádio do carro grita, entre ruídos e lágrimas
Notícias de mortes na TV, e então aparece você
É tudo tão absurdo, tão louco, que eu não consigo me concentrar
Só consigo enxergar sua silhueta, ah

O sol nasce em Hollywood, estamos há dias sem dormir
Um desastre perfeito: eu e você"""[cite: 1]

CURIOSIDADES_CRUEL = [
    "📰 <b>NOTICIÁRIO VIOLENTO E REFÚGIO:</b> Em meio a um mundo 'absurdo' e 'louco', a garota distrai o narrador da crueldade da mídia e o lembra de que ainda existem coisas boas.",
    "📹 <b>CCTV E GRAVAÇÃO EM LOOP:</b> A gravação em loop registra imagens continuamente — na música, simboliza as lembranças passando sem parar na mente."
][cite: 1]

PSICOLOGIA_CRUEL = """🧠 <b>ANÁLISE PSICOLÓGICA — CRUEL</b><br><br>
“Cruel” apresenta um contraste psicológico muito interessante entre a brutalidade do mundo exterior e a experiência de intimidade vivida pelo narrador."""[cite: 1]

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

E se eu perdesse minhas chances?  
E se eu dissesse que o jogo acabou?  
E se eu esquecesse minhas falas  
E perdesse completamente o controle?  

Sinceramente, ela é a única que cuida de mim  
Me dá fôlego quando fica difícil respirar  
Esteja eu certo ou errado  
Ela está sempre do meu lado  
E mesmo que eu perca a batalha...  

Sei que ela vai me trazer de volta  
Me trazer de volta, me trazer de volta à vida  
Me trazer de volta  
Me trazer de volta, me trazer de volta à vida  

E se a gente nunca tivesse se conhecido?  
E se eu nunca tivesse encontrado ela?  
É que estou pegando fogo há tanto tempo  
Num mundo que só fica cada vez mais frio  

Sinceramente, ela é a única que cuida de mim  
Me dá fôlego quando fica difícil respirar  
Esteja eu certo ou errado  
Ela está sempre do meu lado  
E mesmo que eu perca a batalha...  

Sei que ela vai me trazer de volta  
Me trazer de volta, me trazer de volta à vida  
Me trazer de volta  
Me trazer de volta, me trazer de volta à vida  

Ninguém faz isso como você  
Já rodei o mundo  
Conheci tantas mulheres  
Passei por tantos lugares  
Vi tantos rostos  
Mas ninguém faz isso como você  

Sinceramente, ela é a única que cuida de mim  
Me dá fôlego quando fica difícil respirar  
Esteja eu certo ou errado  
Ela está sempre do meu lado  
E mesmo que eu perca a batalha  
Sei que ela vai me trazer de volta à vida""",
        "curiosidades_lista": [
            "🥺 <b>1. ZAYN JÁ FALOU SOBRE ANSIEDADE EM OUTRAS MÚSICAS!</b> Quem acompanha a carreira do cantor sabe que ele não costuma esconder suas dificuldades emocionais nas letras. Em “Back To Life”, ele faz uma declaração daquelas para a pessoa amada, mostrando o quanto ela o ajuda a enfrentar os momentos em que tudo parece ficar mais difícil. Mas essa não é a primeira vez que o assunto aparece por aqui! Em músicas como <b>“Fresh Air”</b> e <b>“Insomnia”</b>, ZAYN também aborda questões relacionadas à ansiedade. Parece que, para ele, transformar esses sentimentos em música é uma maneira de colocar para fora aquilo que nem sempre consegue dizer diretamente.",
            "🇵🇰 <b>2. A INTRODUÇÃO ESCONDE UMA HOMENAGEM À FAMÍLIA DE ZAYN!</b> Aqueles “oh, oh” do começo não estão ali por acaso! A maneira como ZAYN constrói a melodia traz uma influência musical do sul da Ásia, funcionando como uma homenagem às suas raízes paquistanesas, herdadas do pai. E ele já mostrou várias vezes que tem orgulho dessa conexão cultural! Antes mesmo do lançamento do álbum, o cantor publicou em seu YouTube uma versão de <b>“Allah Duhai Hai”</b>, música de Bollywood. Ou seja, até nos pequenos detalhes da faixa existe um pedacinho da história dele. Fofo, né?",
            "👀 <b>3. O REFRÃO PODE TER FEITO VOCÊ LEMBRAR DE UMA MÚSICA DOS ANOS 90!</b> Prepare-se para uma viagem no tempo! O refrão de “Back To Life” tem uma conexão com <b>“You Gotta Be”</b>, da cantora Des’ree, um daqueles sucessos que marcaram os anos 90. A música chegou ao quinto lugar da Billboard Hot 100 em 1995. E sabe o que é mais curioso? Naquela época, ZAYN tinha apenas dois aninhos! Imagina ele crescendo e, anos depois, trazendo uma referência a esse clássico para uma música própria?",
            "💕 <b>4. AS DUAS MÚSICAS PRATICAMENTE CONVERSAM UMA COM A OUTRA!</b> E não é só uma questão de melodia! Em “You Gotta Be”, Des’ree canta sobre ter coragem, ser forte e continuar enfrentando os desafios. Já em “Back To Life”, ZAYN fala sobre alguém que o ajuda a se reerguer quando ele sente que está prestes a desistir. A referência funciona quase como uma conversa entre as duas músicas: de um lado, a mensagem de encontrar forças dentro de si; do outro, a descoberta de que o apoio de alguém especial também pode fazer toda a diferença. É aquele lembrete de que ninguém precisa enfrentar tudo sozinho!"
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — BACK TO LIFE</b><br><br>Sabe aquela pessoa que parece conseguir te alcançar até nos dias em que você mesmo não sabe muito bem como lidar consigo? Aquela presença que, de alguma maneira, faz o mundo parecer menos pesado? É mais ou menos desse lugar que nasce <b>“Back To Life”</b>, do ZAYN. Mas, por trás dessa declaração de amor, existe uma questão psicológica bem interessante: o que acontece quando alguém se torna uma das nossas principais fontes de sustentação emocional?<br><br>Logo no início, o narrador apresenta uma sequência de perguntas: e se mudasse de ideia? E se dissesse que tudo acabou? E se esquecesse suas próprias falas e perdesse completamente o controle? Essa repetição de hipóteses cria a sensação de alguém que está imaginando diferentes possibilidades de fracasso. Psicologicamente, isso pode ser relacionado ao pensamento catastrófico, um padrão cognitivo em que a mente antecipa cenários negativos e começa a considerar o que poderia dar errado. Não significa necessariamente que o narrador esteja vivendo uma crise, mas existe uma preocupação com a possibilidade de perder o controle da própria vida, falhar ou chegar a um ponto em que não consiga mais sustentar a imagem que apresenta ao mundo.""",
        "link_clipe": None
    },[cite: 2]
    "common": {
        "artista": "zayn",
        "letra_limpa": """Sempre olhando por trás das minhas barreiras  
Sempre me senti isolado, oh-oh-oh  
Não sei por que eu era tão fechado  
Mas vou encontrar um jeito de deixar você entrar  

Eu vou me arrepender se não tentar, e também se não perguntar o porquê  
Isso é algo verdadeiro, isso é algo certo  
Nunca estive apaixonado, nunca senti nada assim até agora  

Quando me deito na sua cama, preciso de você junto ao meu peito  
Para me aquecer o tempo todo, para tirar meu fôlego  
Isso está escrito nos seus lábios: não existe nada de comum entre nós  
Neste mundo tão comum, onde nada parece suficiente  
Tudo é tão cinza, confundem amor com desejo  
Mas, quando te abraço, não existe nada de comum entre nós""",
        "curiosidades_lista": [
            "💘 <b>UMA CONEXÃO FORA DO COMUM!</b> Em “Common”, a quarta faixa do álbum <i>Icarus Falls</i>, ZAYN fala sobre encontrar alguém que parece preencher um vazio que ele carregava há muito tempo. Depois de se sentir inseguro e isolado, o cantor encontra nessa pessoa uma conexão completamente diferente de todas as outras. E é daí que vem o título da música! Quando ele diz que não existe nada de comum entre os dois, está justamente destacando que o que vivem é especial, algo que não encontra em qualquer pessoa. Pelo visto, para ZAYN, essa paixão está longe de ser só mais uma história de amor! 👀"
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — COMMON</b><br><br>Sabe quando a gente passa tanto tempo tentando se proteger que acaba esquecendo como é deixar alguém chegar de verdade? Você se acostuma a manter certa distância, esconde suas inseguranças, evita demonstrar demais o que sente… até que aparece uma pessoa que faz essas defesas começarem a parecer desnecessárias. É exatamente essa transformação que encontramos em <b>“Common”</b>, do ZAYN.""",
        "link_clipe": None
    },[cite: 3]
    "drop dead": {
        "artista": "zayn",
        "letra_limpa": """Eu sei que o bar fecha às onze  
Mas espero que você nunca termine essa cerveja  
Você sabe cantar de cor “Just Like Heaven”  
E agora que você está bem aqui na minha frente, entendo por que ele escreveu aquela música  

Uma noite, estava entediada na cama  
E fui fuçar sua vida na internet  
É minha intuição feminina  
Porque eu sempre imaginei nós dois exatamente assim  
Bem juntinhos, espremidos na fila do banheiro  
Você parece um anjo nas pinturas das paredes de Versalhes  
Nunca me senti tão viva  
Mas, se você me beijar, posso até morrer""",
        "curiosidades_lista": [
            "💗 <b>OLIVIA RODRIGO — “DROP DEAD”: O COMEÇO DE UMA PAIXÃO, OS SURTOS DE CRUSH E UMA DECLARAÇÃO NADA DISCRETA!</b> “drop dead” é o primeiro single do terceiro álbum de estúdio de <b>Olivia Rodrigo</b>, <i>you seem pretty sad for a girl so in love</i>. A música acompanha aquela fase em que a gente conhece uma pessoa, fica imaginando mil possibilidades e começa a pensar em como seria maravilhoso viver um romance com ela.",
            "👑 <b>UM CLIPE DIGNO DE CONTO DE FADAS!</b> O videoclipe foi gravado no famoso Palácio de Versalhes, na França, justamente por causa de um dos versos da música."
        ],
        "psicologia": """🧠 <b>O QUE ACONTECE NA NOSSA CABEÇA QUANDO ESTAMOS COMPLETAMENTE APAIXONADOS? UMA ANÁLISE PSICOLÓGICA DE “DROP DEAD”, DE OLIVIA RODRIGO 💗</b><br><br>Sabe aquela sensação de conhecer alguém e, de repente, começar a imaginar mil possibilidades ao lado dessa pessoa? É exatamente esse estado de encantamento que Olivia Rodrigo transforma em música em <b>“drop dead”</b>.""",
        "link_clipe": None
    },[cite: 4]
    "i don't wanna live forever": {
        "artista": "zayn",
        "letra_limpa": """Fico de olhos bem abertos, sem conseguir dormir
Atrás destas quatro paredes, esperando que você ligue
É uma existência cruel
Como se não houvesse motivo algum para continuar esperando

Não quero viver para sempre
Porque sei que estaria vivendo em vão
E não quero me encaixar em qualquer lugar
Só quero continuar chamando pelo seu nome
Até você voltar para casa""",
        "curiosidades_lista": [
            "🎬 <b>TRILHA DE CINQUENTA TONS MAIS ESCUROS:</b> A faixa foi criada para a sequência de <i>Cinquenta Tons de Cinza</i>, trazendo um clima intenso e sensual sobre sentir que a vida perde o sentido quando quem se ama vai embora.",
            "🤝 <b>DUETO E COMPOSIÇÃO:</b> Unindo ZAYN e Taylor Swift, a música também conta com Taylor na composição ao lado de Jack Antonoff e Sam Dew."
        ],
        "psicologia": """🧠 <b>PAPO PSICOLÓGICO — I DON'T WANNA LIVE FOREVER</b><br><br>Em “I Don’t Wanna Live Forever”, o que mais chama atenção não é só a saudade de alguém depois de um término. É o jeito como os narradores parecem transformar a ausência amorosa numa crise sobre a própria existência.""",
        "link_clipe": None
    },[cite: 5]
    "let me": {
        "artista": "zayn",
        "letra_limpa": """Meu bem, o que a gente vive na cama tem significado (tem significado)
Sei que, dessa vez, você vai ficar até amanhecer (até amanhecer)
Dias de preguiça debaixo das cobertas e sorvete de baunilha (sorvete de baunilha)
Quero mais do que apenas uma noite juntos, quero você só pra mim

Deixa eu ser o homem da sua vida
Pra que eu possa te amar (possa te amar)
E, se você me deixar ser esse homem,
Vou cuidar de você

Pelo resto da minha vida, pelo resto da sua
Pelo resto da minha vida, pelo resto da sua
Pelo resto das nossas vidas""",
        "curiosidades_lista": [
            "💫 <b>“Quero mais do que apenas uma noite juntos, quero você só pra mim”:</b> ZAYN quer exclusividade e algo que vá muito além de encontros passageiros.",
            "💍 <b>“Pelo resto da minha vida, pelo resto da sua”:</b> ZAYN já comentou que “Let Me” poderia ser interpretada como uma música de casamento."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — LET ME</b><br><br>Sabe quando uma relação começa com muita atração, mas, em algum momento, uma das pessoas percebe que não quer mais viver aquilo apenas como um encontro passageiro? É justamente essa virada que torna <b>“Let Me”</b>, de ZAYN, tão interessante psicologicamente.""",
        "link_clipe": None
    },[cite: 6]
    "natural": {
        "artista": "zayn",
        "letra_limpa": """É como respirar, como falar  
Quando a gente se toca, é como uma força da natureza  
Não é só um sentimento, vamos acreditar  
O nascimento do amor, como uma força da natureza  

Inevitável (é o nosso amor)  
Inesquecível (é o nosso amor)  
Nada se compara à sensação  
De sentir você na minha pele  

Parece tão natural, tão natural  
Quando a gente se entrega  
Como uma força da natureza""",
        "curiosidades_lista": [
            "💗 <b>“Parece tão natural, tão natural, quando a gente se entrega”:</b> ZAYN canta sobre uma conexão tão espontânea que estar junto, trocar carinhos e sentir o toque da outra pessoa acontece sem esforço.",
            "🌊 <b>“Como uma onda, derrubamos as barreiras”:</b> Ondas, furacões e forças naturais viram comparações para uma conexão intensa e espontânea."
        ],
        "psicologia": """🧠 <b>ANÁLISE PSICOLÓGICA — NATURAL</b><br><br>Sabe aquela sensação de estar com alguém e perceber que você não precisa pensar muito no que fazer, no que falar ou em como agir? É justamente essa experiência que está no centro de <b>“Natural”</b>, do ZAYN.""",
        "link_clipe": None
    },[cite: 7]
    "stupid song": {
        "artista": "zayn",
        "letra_limpa": """Nova York nunca pareceu tão triste e cinzenta
Meus amigos estão fumando uns baseados no banheiro
Eles dizem que o amor de verdade é uma prisão que faz você se sentir livre
E todas as garotas dessa festa são tão descoladas
Nunca fui muito boa nisso
Mas não consigo evitar imaginar o que você diz quando conversa comigo

Você é uma faísca no escuro e minhas roupas estão pegando fogo
Você devia sentir o que eu sinto quando alguém diz seu nome
Sou um carro disparado pela avenida, sem freios
E eu quero você mais do que qualquer música boba conseguiria expressar""",
        "curiosidades_lista": [
            "💘 <b>“STUPID SONG”: QUANDO ESTAR APAIXONADA DEIXA A GENTE COMPLETAMENTE FORA DE ÓRBITA!</b> Olivia Rodrigo mergulha em um lado intenso e inquieto da paixão, em que a saudade, o desejo e a obsessão começam a ocupar espaço demais na cabeça.",
            "📖 <b>UMA INSPIRAÇÃO LITERÁRIA NADA CONVENCIONAL!</b> Olivia contou que uma das grandes inspirações para escrever “stupid song” foi o livro <i>Simple Passion</i>, de Annie Ernaux."
        ],
        "psicologia": """🧠 <b>“STUPID SONG”: QUANDO A PAIXÃO COMEÇA A OCUPAR ESPAÇO DEMAIS NA CABEÇA!</b><br><br>Sabe quando você conhece alguém e, de repente, parece que seu cérebro decide transformar essa pessoa no assunto principal de absolutamente tudo? É justamente esse estado de encantamento quase incontrolável que Olivia Rodrigo explora em <b>“stupid song”</b>.""",
        "link_clipe": None
    }[cite: 8]
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
    )[cite: 1]


def encontrar_chave_manual(titulo_faixa):
    titulo = normalizar_chave_faixa(titulo_faixa)[cite: 1]
    if titulo in MUSICAS_MANUAIS:
        return titulo

    titulo_limpo = titulo.split("(")[0].split(" - ")[0].strip()[cite: 1]
    if titulo_limpo in MUSICAS_MANUAIS:
        return titulo_limpo

    for chave in MUSICAS_MANUAIS:
        if chave in titulo:
            return chave

    return None[cite: 1]


def get_lyrics(t, a):
    if encontrar_chave_manual(t):[cite: 1]
        return None[cite: 1]
    try:
        url = f"https://lrclib.net/api/get?artist_name={a}&track_name={t}"[cite: 1]
        r = requests.get(url, timeout=3)[cite: 1]
        if r.status_code == 200:
            return r.json().get("plainLyrics")[cite: 1]
    except Exception:
        pass
    return None[cite: 1]


def criar_oauth():
    return SpotifyOAuth(
        client_id=ID,
        client_secret=SEC,
        redirect_uri=URI,
        scope=SCOPES,
        open_browser=False,
    )[cite: 1]


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
"""[cite: 1]


@app.route("/")
def index():
    sp = obter_cliente_spotify_usuario()
    return render_template_string(HTML_TEMPLATE, logado=bool(sp))[cite: 1]


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
        cur = sp.current_user_playing_track()[cite: 1]
        if cur and cur.get("is_playing") and cur.get("item"):[cite: 1]
            tr = cur["item"][cite: 1]
            tn = tr["name"][cite: 1]
            ar = tr["artists"][0]["name"][cite: 1]
            tid = tr["id"][cite: 1]
            img = tr["album"]["images"][0]["url"][cite: 1]
            p = cur.get("progress_ms", 0)[cite: 1]
            dur = tr.get("duration_ms", 1)[cite: 1]

            if sid:
                ULTIMA_MUSICA_POR_SESSAO[sid] = tid

            key = encontrar_chave_manual(tn)[cite: 1]
            if key:
                letra = MUSICAS_MANUAIS[key]["letra_limpa"][cite: 1]
                gossip = MUSICAS_MANUAIS[key]["curiosidades_lista"][cite: 1]
                psych = MUSICAS_MANUAIS[key]["psicologia"][cite: 1]
                clipe = MUSICAS_MANUAIS[key]["link_clipe"][cite: 1]
            else:
                letra = get_lyrics(tn, ar) or "Letra não encontrada para esta faixa."[cite: 1]
                gossip = [f"<b>BLOG DO SPOTIFY:</b><br>Tocando agora o som de {ar}! 🎧✨"][cite: 1]
                psych = "🧠 <b>ANÁLISE COMPORTAMENTAL:</b><br><br>Esta faixa está tocando livremente no seu player. Analise as emoções e os sentimentos despertados pela melodia!"[cite: 1]
                clipe = None[cite: 1]

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
            })[cite: 1]
    except Exception:
        pass
    return jsonify({"playing": False})[cite: 1]


if __name__ == "__main__":
    print("\n✨ Seu site está no ar! Abra no navegador: http://127.0.0.1:5000 ✨\n")[cite: 1]
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))[cite: 1]