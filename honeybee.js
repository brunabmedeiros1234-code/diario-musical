
/*
  XOXO MY MUSIC DIARY
  HONEYBEE | OLIVIA RODRIGO

  Arquivo adicional.
  Não altera o Client ID do Spotify.
  Não apaga drop dead nem stupid song.
*/

(() => {
  "use strict";

  const honeybee = {
    title: "honeybee",
    artist: "Olivia Rodrigo",
    lookup: ["honeybee", "olivia rodrigo"],

    /*
      Imagem provisória já usada pela revista.
      Depois podemos substituir pela capa de honeybee.
    */
    cover: "assets/olivia-top.webp",

    spotifyUrl:
      "https://open.spotify.com/search/honeybee%20Olivia%20Rodrigo",

    intro:
      "Sabe quando você encontra alguém tão especial que começa a torcer para que aquela felicidade nunca tenha fim? É exatamente disso que Olivia Rodrigo fala em “honeybee”! Depois de tantas músicas sobre corações partidos, a cantora mostra um lado mais doce e maduro do amor, com passeios à noite, apelidos carinhosos e aquela sensação maravilhosa de ter alguém sempre por perto.\n\nSó que nem tudo são flores! Olivia está tão apaixonada que começa a pensar em como seria doloroso perder essa pessoa. Ela não está sofrendo por um amor que acabou, mas torcendo para que um amor que está dando certo continue assim. Ai, que mistura de fofura com medo de sofrer, né?",

    translation: `Então acho que é verdade mesmo
O tempo consegue curar até as piores feridas
E todos aqueles clichês que eu conhecia
Passaram a fazer sentido quando te vi
Vamos caminhar no escuro
Pular a cerca do parque
Meu amor, meu docinho
Meu Deus, como eu amo o jeito que você olha pra mim

É tão difícil explicar o que eu sinto
Sem parecer que estou exagerando
Mas, mesmo quando fico em silêncio
Eu te amo, meu bem, eu prometo
E espero nunca ter que ver seu rosto enquanto você vai embora
Porque é um rosto que eu juro que poderia passar a vida inteira admirando
Só me resta torcer para que seja assim

Vem me buscar, me acompanha até em casa
E parece até que Deus resolveu me dar uma sorte
Doce feito mel, gostoso como uma tangerina
Você não quer ficar aqui comigo mais um pouquinho?
No escuro, eu não tenho medo
Porque basta estender a mão e você está ali
Estrelas cadentes, carros em alta velocidade
Tudo o que é meu agora parece ser nosso

É tão difícil explicar o que eu sinto
Sem parecer que estou exagerando
Mas, mesmo quando fico em silêncio
Eu te amo, meu bem, eu prometo
E espero nunca ter que ver seu rosto enquanto você vai embora
Porque é um rosto que eu juro que poderia passar a vida inteira admirando
Só me resta torcer para que seja assim

Espero nunca ter que ver seu rosto enquanto você vai embora
Porque é um rosto que eu juro que poderia passar a vida inteira admirando
Só me resta torcer para que seja assim

É tão difícil explicar o que eu sinto
Sem parecer que estou exagerando
Mas, mesmo quando fico em silêncio
Eu prometo
E espero nunca ter que ver seu rosto enquanto você vai embora
Porque é um rosto que eu juro que poderia passar a vida inteira admirando
Só me resta torcer para que seja assim`,

    /*
      Os cinco primeiros itens aparecem em Curiosidades.
      Os demais aparecem em Você percebeu?
      Mantemos os 17 assuntos.
    */

    curiosities: [
      `💗 O TEMPO REALMENTE CURA AS FERIDAS DO CORAÇÃO?

“Então acho que é verdade mesmo / O tempo consegue curar até as piores feridas”

O início de “honeybee” mostra uma mudança importante em relação ao tom de SOUR e GUTS. Antes, Olivia Rodrigo cantava sobre ressentimentos, decepções e dores que pareciam impossíveis de superar. Em “the grudge”, por exemplo, ela admite que perdoar exige uma força que ainda não sente possuir.

Agora, a perspectiva é outra. Ao viver um novo relacionamento, ela percebe que as dores antigas podem deixar de ocupar o centro de sua vida. Isso não significa que outra pessoa tenha apagado seu sofrimento, mas que novas experiências podem transformar a maneira como enxergamos o passado.

No especial Amex Story of My Song, Olivia comentou que, quando era adolescente e estava com o coração partido, acreditava que talvez nunca mais encontrasse alguém. Com o tempo, descobriu que é possível amar outras pessoas profundamente e construir conexões completamente diferentes.

É uma das mensagens mais esperançosas da música: aquilo que parece insuperável hoje não precisa definir todo o nosso futuro.`,

      `🎬 O ROMANCE DE NOTTING HILL ESCONDIDO NA LETRA!

“Vamos caminhar no escuro / Pular a cerca do parque”

Essa imagem faz referência ao filme Um Lugar Chamado Notting Hill, de 1999. Em uma das cenas, William e Anna passeiam juntos à noite e entram em um jardim particular depois de pular a cerca.

Olivia contou que ama o filme e achou aquela cena especialmente bonita. O trecho transforma a caminhada em uma pequena aventura romântica, como se os dois estivessem vivendo um momento que pertence apenas a eles.

Alguns fãs também encontram semelhanças entre o filme e o relacionamento de Olivia com Louis Partridge. Anna é americana e William é inglês, assim como Olivia é americana e Louis é inglês. Essa associação específica, porém, é uma interpretação dos fãs, não uma confirmação da cantora.

E teve pista antes do lançamento! Em 4 de julho de 2025, durante sua apresentação no Festival Roskilde, na Dinamarca, Olivia apareceu usando uma camiseta com a frase “Hop the fence in the park”.`,

      `🐝 BABY BOY: O APELIDO QUE DIVIDIU OS FÃS!

“Meu amor, meu docinho”

Olivia usa as expressões “baby boy” e “honeybee” para transmitir ternura e intimidade. “Honeybee” significa literalmente “abelha-do-mel”, enquanto “baby boy” é um apelido carinhoso que pode soar delicado ou brincalhão dentro de um relacionamento.

Mas nem todo mundo achou fofo! Algumas pessoas nas redes sociais consideraram estranho chamar um homem adulto de “baby boy”. Outros fãs defenderam a cantora, lembrando que homens usam expressões como “baby girl” em músicas românticas sem necessariamente receber as mesmas críticas.

Também houve quem lembrasse que “baby boy” aparece há décadas no R&B e no pop. Um exemplo conhecido é “Baby Boy”, de Beyoncé, lançada em 2003.

No contexto de “honeybee”, o apelido combina com a ideia de um amor que não precisa parecer sofisticado o tempo inteiro. Às vezes, a intimidade também permite ser boba, carinhosa e completamente melosa.`,

      `🎹 O DESAFIO DE ESCREVER SOBRE UM AMOR MAIS MADURO!

Olivia descreveu “honeybee” como uma das músicas mais antigas do álbum you seem pretty sad for a girl so in love e contou que escrevê-la foi um desafio criativo.

Ela já havia escrito canções de amor antes, mas sentia que muitas tinham uma perspectiva mais adolescente. Dessa vez, queria transmitir um amor mais maduro, com nuances, complexidades e uma vulnerabilidade que realmente correspondesse ao momento que estava vivendo.

Em entrevista ao podcast Popcast, Olivia explicou que desejava escrever uma música clássica de cantora e compositora. Ela se sentou ao piano, escreveu a canção e sentiu que finalmente tinha encontrado palavras para uma emoção muito difícil de descrever.

Segundo a cantora, uma das maiores dificuldades era falar sobre o amor de maneira original, já que tantos artistas exploraram esse sentimento ao longo dos anos.

Ela também comentou que, considerando a história completa do álbum, “honeybee” talvez seja uma das faixas mais tristes. E isso diz muito sobre a mistura de felicidade e medo que percorre a letra.`,

      `💍 UMA MÚSICA PARA TOCAR NO CASAMENTO?

“Eu te amo, meu bem, eu prometo”

Em conversa com a Audacy Music, Olivia comentou que “honeybee” foi uma experiência diferente em sua trajetória como compositora.

A cantora explicou que queria escrever uma canção verdadeiramente dedicada à felicidade do amor romântico. Ela chegou a brincar que a faixa lembrava aquelas músicas que as pessoas escolhem para tocar em casamentos e disse que esperava que alguém realmente a utilizasse dessa maneira.

O mais interessante é que a música não se limita a uma declaração perfeita e inabalável. No meio de tanto carinho, aparece a consciência de que o relacionamento pode não durar para sempre.

É justamente essa combinação que a torna emocionante: Olivia está feliz e apaixonada, mas não esconde a vulnerabilidade de amar alguém profundamente.`,

      `📖 QUANDO OS CLICHÊS ROMÂNTICOS FAZEM SENTIDO!

“E todos aqueles clichês que eu conhecia / Passaram a fazer sentido quando te vi”

Olivia reconhece que algumas declarações de amor que antes pareciam exageradas começaram a ganhar significado quando ela própria se apaixonou.

Isso não quer dizer que a cantora passou a acreditar que uma pessoa pode salvar ou resolver a vida emocional da outra. Na música “the cure”, ela questiona justamente essa expectativa de que o amor romântico funcione como solução para todos os problemas.

O contraste é interessante. É possível descobrir a beleza de um relacionamento e, ao mesmo tempo, reconhecer que nenhuma outra pessoa tem a responsabilidade de curar todas as nossas dificuldades.

O amor pode oferecer companhia, apoio e momentos felizes, mas também precisamos desenvolver recursos próprios para enfrentar os conflitos internos.`,

      `👀 O QUE EXISTE DE TÃO ESPECIAL EM UM OLHAR?

“Meu Deus, como eu amo o jeito que você olha pra mim”

Olivia não declara apenas que gosta da aparência ou da companhia do parceiro. Ela destaca a maneira como é olhada por ele.

Esse detalhe sugere a felicidade de perceber carinho, interesse e admiração no olhar de alguém. Existe uma diferença entre amar uma pessoa e sentir que nossa presença também é importante para ela.

A exclamação “Meu Deus” intensifica esse encantamento. Parece aquele momento em que a pessoa está tão feliz com uma demonstração de afeto que não consegue encontrar palavras melhores.

Na letra, essa sensação reaparece quando Olivia afirma que parece que Deus finalmente resolveu lhe dar uma sorte.`,

      `🤫 O AMOR TAMBÉM EXISTE NO SILÊNCIO!

“Mas, mesmo quando fico em silêncio”

Durante o especial Amex Story of My Song, Olivia explicou que uma parte muito bonita do amor aparece nos momentos silenciosos.

Ela comentou que não é necessário fazer grandes demonstrações o tempo inteiro. Às vezes, basta olhar para o outro lado da sala e saber que existe alguém ali que realmente se importa conosco.

Essa interpretação dá ainda mais força ao refrão. Olivia está tentando escrever uma declaração sincera, mas reconhece que seus sentimentos continuam existindo mesmo quando ela não consegue expressá-los em palavras.

Em uma relação próxima, a presença, a atenção e os pequenos gestos também podem funcionar como demonstrações importantes de carinho.`,

      `🥺 O VERSO MAIS BONITO TAMBÉM É O MAIS ASSUSTADOR!

“E espero nunca ter que ver seu rosto enquanto você vai embora / Porque é um rosto que eu juro que poderia passar a vida inteira admirando”

Esse é um dos momentos mais importantes da música. Olivia não está descrevendo uma separação que aconteceu, mas o medo de perder alguém que ainda está ao seu lado.

Em entrevista à Apple Music, ela explicou que existe uma fragilidade nesse verso da qual gosta muito. A cantora contou que ficou emocionada ao perceber que tinha escrito exatamente aquilo que sentia.

Segundo Olivia, estar com alguém a quem amamos profundamente também pode ser assustador porque começamos a reconhecer que temos algo muito precioso a perder.

Ela descreveu a diferença entre desejar recuperar algo que já perdemos e estar feliz no presente, torcendo para que aquilo não termine.

Em outras entrevistas, incluindo conversas com Hits Radio UK e Capital Buzz, Olivia voltou a destacar esse trecho como um dos seus favoritos.

A força emocional está nessa contradição: o rosto que ela gostaria de admirar pela vida inteira também poderia, um dia, ser o rosto de uma despedida.`,

      `✨ HERE'S TO HOPING: A FRASE QUE RESUME O ÁLBUM!

“Só me resta torcer para que seja assim”

Durante uma conversa com Zane Lowe, para a Apple Music, Olivia comentou que considera “here's to hoping” uma das frases que melhor representam o álbum.

Ela explicou que a esperança aparece de várias maneiras ao longo da história: o desejo de viver um amor especial, a expectativa de se sentir melhor e a tentativa de acreditar que as coisas vão dar certo.

Entretanto, essa esperança não é uma certeza. O futuro permanece desconhecido e os sentimentos podem mudar.

No começo da história, existe a empolgação de finalmente encontrar algo que parecia tão desejado. Mais adiante, outras músicas exploram conflitos, decepções e expectativas que não se concretizaram.

Por isso, a frase é tão significativa. Olivia não promete que o amor durará para sempre. Ela expressa o desejo de que isso aconteça.`,

      `🌆 A FANTASIA ROMÂNTICA PERFEITA DE OLIVIA!

“Vem me buscar, me acompanha até em casa”

Olivia revelou no especial Amex Story of My Song que esse é praticamente o cenário romântico dos seus sonhos.

Ela imaginou uma noite em que estaria jantando com as amigas, tomando Aperol Spritz, até que o namorado aparecesse para buscá-la.

Os dois caminhariam juntos até em casa, conversando sobre a noite. E, se tivesse acontecido alguma fofoca no jantar, ela poderia contar todos os detalhes no caminho.

A graça está na simplicidade da fantasia. Não é uma viagem luxuosa nem um gesto grandioso. É a felicidade de compartilhar coisas pequenas com alguém de quem gostamos.

A mesma imagem de ser acompanhada até em casa também aparece em “drop dead”, criando uma ligação entre as músicas.`,

      `🍀 QUANDO A VIDA FINALMENTE RESOLVE DAR UMA SORTE!

“E parece até que Deus resolveu me dar uma sorte”

No original, Olivia canta “God threw me a bone”.

A expressão inglesa “throw someone a bone” é utilizada quando alguém recebe uma ajuda, uma oportunidade ou uma pequena recompensa depois de passar por dificuldades.

Sua origem figurada lembra a imagem de oferecer um osso a um cachorro, dando-lhe alguma coisa para aliviar sua situação.

Em “honeybee”, Olivia usa a expressão para transmitir a sensação de que, depois de tantas desilusões, alguma coisa boa finalmente aconteceu em sua vida.

É quase como se ela pensasse que, depois de tanto sofrimento amoroso, finalmente teve a oportunidade de viver uma história feliz.`,

      `🍊 MEL, TANGERINAS E UMA PAIXÃO AÇUCARADA!

“Doce feito mel, gostoso como uma tangerina”

Em uma entrevista sobre a música, Olivia explicou que queria transmitir aquela sensação de que tudo parece doce e maravilhoso quando estamos apaixonados.

A cantora associou a imagem do mel e da tangerina a algo açucarado, saboroso e encantador.

É uma metáfora que combina com o título “honeybee” e com o clima delicado da canção.

Olivia também havia dado uma pista antes do lançamento. Em 12 de julho de 2025, no Mad Cool Festival, em Madri, apareceu usando uma blusa branca com a expressão “sticky sweet”.

A imagem da doçura reforça o contraste com outras partes do álbum, nas quais o amor aparece como uma experiência muito mais complicada.`,

      `🌙 POR QUE O ESCURO DEIXA DE DAR MEDO?

“Você não quer ficar aqui comigo mais um pouquinho? / No escuro, eu não tenho medo / Porque basta estender a mão e você está ali”

A escuridão pode representar tanto a noite quanto momentos de tristeza, insegurança e dificuldade emocional.

Olivia encontra conforto na ideia de que o parceiro continua presente mesmo quando as circunstâncias não são perfeitas.

Em situações difíceis, nem sempre precisamos de grandes conselhos. Às vezes, a companhia e a disposição de permanecer ao nosso lado são profundamente importantes.

O gesto de estender a mão transmite a percepção de disponibilidade afetiva.

A música valoriza justamente essa forma de intimidade: saber que existe alguém por perto e que não precisamos enfrentar todos os momentos difíceis sozinhos.`,

      `🌠 ESTRELAS CADENTES E CARROS EM ALTA VELOCIDADE!

“Estrelas cadentes, carros em alta velocidade”

As estrelas cadentes costumam ser associadas a desejos, esperança e sorte. Essa imagem combina com a vontade de Olivia de que seu relacionamento continue.

Já os carros em alta velocidade podem representar a intensidade de uma paixão que parece difícil de controlar.

Em “stupid song”, Olivia utiliza uma imagem semelhante ao se comparar a um carro disparado pela avenida, sem freios.

Essa metáfora também cria um contraste com “making the bed”, do álbum GUTS. Nessa música, a cantora descreve um sonho recorrente em que dirige pela cidade e percebe que os freios não funcionam.

Em “making the bed”, a imagem sugere falta de controle. Em “honeybee”, pode representar a empolgação de viver uma relação tão importante.`,

      `💞 QUANDO O QUE É MEU COMEÇA A PARECER NOSSO!

“Tudo o que é meu agora parece ser nosso”

No especial Amex Story of My Song, Olivia explicou que, quando estamos nos apaixonando, a linha que separa nossa vida da vida da outra pessoa pode parecer cada vez mais fina.

Nossas experiências, lembranças, conquistas e dificuldades passam a fazer parte de uma história compartilhada.

A cantora comentou, com humor, que é filha única e precisou aprender a dividir melhor as coisas.

Para ela, é bonito quando o desejo de compartilhar surge espontaneamente, simplesmente porque gostamos tanto de alguém.

Na psicologia dos relacionamentos, essa aproximação pode ser relacionada à expansão do self, ideia desenvolvida por Arthur Aron e colaboradores.

Isso não significa perder a individualidade, mas permitir que uma relação próxima amplie nossas experiências e perspectivas.`,

      `💌 A DECLARAÇÃO QUE SE COMPLETA NO SILÊNCIO!

“Mas, mesmo quando fico em silêncio / Eu prometo”

No final de “honeybee”, Olivia modifica discretamente o refrão.

Antes, ela cantava que, mesmo quando ficava em silêncio, amava a pessoa e prometia que esse sentimento era verdadeiro.

Na última repetição, a declaração fica incompleta. Ela canta apenas “Eu prometo”.

A essa altura, quem está ouvindo já sabe quais palavras ficaram de fora.

É como se o próprio silêncio completasse a declaração de amor.

Essa escolha reforça uma das mensagens mais delicadas da canção: nem todo sentimento precisa ser verbalizado o tempo inteiro para continuar existindo.`
    ],

    psychology: `POR TRÁS DA LETRA ♡ A PSICOLOGIA DE “HONEYBEE”

Por que encontrar o amor que sempre desejamos também pode despertar nossos maiores medos?

Existe algo particularmente comovente em “honeybee”, de Olivia Rodrigo. Diferentemente das músicas em que a cantora tenta compreender o fim de um relacionamento, aqui ela se encontra diante de uma experiência que parece quase desconhecida: a felicidade de amar alguém e se sentir correspondida. Não há uma traição para superar, uma discussão para revisitar ou um antigo namorado para esquecer. Pela primeira vez, o conflito não está naquilo que ela perdeu, mas na possibilidade de perder algo que ainda possui. É justamente essa contradição que transforma uma canção aparentemente tão doce em uma das reflexões mais vulneráveis sobre o amor.

Logo nos primeiros versos, Olivia reconhece que o tempo talvez seja realmente capaz de curar até as feridas mais profundas. Essa percepção representa uma mudança importante na maneira como ela interpreta suas experiências anteriores. Quando estamos emocionalmente envolvidos em uma situação dolorosa, é comum termos dificuldade de imaginar um futuro em que aquele sofrimento já não ocupe tanto espaço. A intensidade do presente pode fazer com que sentimentos passageiros pareçam permanentes. Entretanto, à medida que novas experiências são construídas, nossa relação com as lembranças também pode se transformar. O que antes parecia impossível de superar passa a ser compreendido como uma parte da nossa história, e não como uma sentença sobre tudo o que ainda iremos viver. Olivia não está necessariamente dizendo que seu novo relacionamento a curou, mas que voltar a amar lhe permitiu perceber que sua vida emocional não terminou nas decepções do passado.

Essa mudança também aparece quando ela admite que os clichês românticos começaram a fazer sentido. Existe uma diferença entre conhecer intelectualmente um sentimento e experimentá-lo. Podemos ouvir milhares de declarações de amor, assistir a romances e compreender perfeitamente o significado de querer passar a vida inteira com alguém, mas nada disso reproduz exatamente a experiência subjetiva de estar apaixonada. A emoção modifica a maneira como atribuímos significado às situações. Um passeio à noite, uma conversa aparentemente banal ou um simples olhar podem adquirir uma importância que dificilmente teriam em outras circunstâncias. O que antes parecia exagero passa a representar uma experiência íntima e verdadeira.

Talvez por isso os momentos mais românticos de “honeybee” sejam também os mais cotidianos. Olivia não descreve um relacionamento marcado por grandes acontecimentos, mas por gestos aparentemente pequenos: alguém que a busca, acompanha sua caminhada até em casa, senta para lhe fazer companhia e permanece ao seu lado quando tudo está escuro. Na psicologia dos relacionamentos, a percepção de que o parceiro compreende, valoriza e responde às nossas necessidades emocionais é considerada um aspecto importante da intimidade. Não se trata apenas de ter alguém por perto, mas de sentir que nossa presença importa para essa pessoa. Quando Olivia canta que basta estender a mão para encontrá-lo, o gesto transmite uma sensação de disponibilidade afetiva. É a tranquilidade de não precisar enfrentar sozinha todos os momentos difíceis.

Há também uma delicadeza especial na dificuldade que ela encontra para expressar seus sentimentos. Ao admitir que não consegue descrevê-los de maneira suficientemente sincera, Olivia revela uma limitação bastante humana: nem sempre conseguimos traduzir em palavras aquilo que experimentamos emocionalmente. Algumas emoções são formadas por tantas sensações, expectativas e lembranças que qualquer tentativa de explicação parece simplificá-las. Sua preocupação em encontrar uma forma honesta de falar sobre o amor sugere que ela não deseja apenas fazer uma declaração bonita. Ela quer que as palavras correspondam à profundidade da experiência que está vivendo. É interessante que, justamente por isso, uma das demonstrações mais significativas da música aconteça quando ela afirma que continua amando mesmo em silêncio. O sentimento não deixa de existir simplesmente porque não está sendo verbalizado.

Entretanto, a aparente tranquilidade da canção começa a adquirir outro significado quando Olivia confessa que espera nunca precisar ver o rosto da pessoa amada indo embora. O verso introduz uma ameaça que, até então, não parecia existir. Não há qualquer indicação de que uma separação esteja acontecendo naquele momento, mas a possibilidade já é suficiente para despertar sofrimento. Esse mecanismo pode ser compreendido a partir da antecipação emocional, nossa capacidade de imaginar situações futuras e experimentar sentimentos relacionados a elas antes mesmo que aconteçam. Essa habilidade pode nos ajudar a reconhecer riscos e nos preparar para dificuldades, mas também pode fazer com que soframos por acontecimentos que talvez nunca se concretizem.

O mais interessante é que Olivia parece descobrir o medo justamente quando encontra a felicidade. Enquanto estava tentando superar antigas decepções, sua dor estava relacionada à ausência de algo que desejava recuperar. Agora, a situação se inverte: ela tem aquilo que queria, mas percebe que não existe garantia de permanência. O amor torna-se, ao mesmo tempo, uma fonte de segurança e de vulnerabilidade. Quanto maior o valor emocional atribuído ao relacionamento, mais assustadora pode parecer a possibilidade de sua perda. Não porque amar intensamente implique necessariamente viver insegura, mas porque estabelecer uma conexão profunda também significa reconhecer que outra pessoa passou a ocupar um lugar importante na nossa vida.

Essa contradição ajuda a compreender por que “honeybee” pode soar tão melancólica mesmo sendo uma declaração de amor. Olivia parece incapaz de separar completamente a felicidade presente da consciência de que ela pode ser passageira. Ao observar o rosto de seu parceiro, não pensa apenas em como gosta de olhá-lo, mas também em como seria doloroso vê-lo partir. O mesmo rosto que desperta ternura poderia, em outra circunstância, tornar-se a última imagem de uma despedida. A força emocional do verso está nessa sobreposição de possibilidades: o futuro que ela deseja construir e aquele que teme enfrentar.

Quando Olivia canta que tudo o que possui começa a parecer dos dois, surge outra dimensão importante da experiência amorosa. O psicólogo Arthur Aron e seus colaboradores desenvolveram o modelo de expansão do self, segundo o qual relacionamentos próximos podem ampliar nossa percepção de quem somos. Ao nos envolvermos profundamente com alguém, passamos a conhecer novas perspectivas, compartilhar experiências e incluir aspectos da vida dessa pessoa em nossa própria identidade. Em “honeybee”, essa aproximação aparece como uma transformação espontânea. Suas conquistas, lembranças e experiências parecem ganhar um novo significado diante da possibilidade de compartilhá-las. O amor deixa de ser apenas um sentimento direcionado ao outro e passa a influenciar a maneira como ela imagina sua própria vida.

No entanto, a canção não termina com uma promessa definitiva. Olivia não afirma que encontrou alguém com quem certamente envelhecerá, nem garante que o relacionamento resistirá a qualquer dificuldade. Em vez disso, repete uma expressão aparentemente simples: “Here's to hoping”. Há uma diferença importante entre acreditar que algo vai acontecer e desejar profundamente que aconteça. A esperança pressupõe a existência de incerteza. Só precisamos torcer por aquilo que não podemos garantir.

É justamente essa escolha que revela a maturidade emocional da composição. Olivia não tenta transformar seu desejo em uma certeza absoluta. Ela reconhece, ainda que de maneira delicada, que o futuro de um relacionamento não depende apenas da intensidade do sentimento vivido no presente. Amar alguém não nos concede controle sobre suas escolhas, sobre as circunstâncias da vida ou sobre as transformações que ambos ainda poderão experimentar. Existe uma vulnerabilidade inevitável em construir expectativas ao lado de outra pessoa, porque nenhuma promessa é capaz de eliminar completamente a imprevisibilidade das relações humanas.

Talvez o aspecto mais bonito de “honeybee” esteja no fato de que Olivia não precisa estar sofrendo para reconhecer a fragilidade do amor. Sua felicidade é verdadeira, assim como o receio de que ela termine. Os dois sentimentos podem coexistir sem que um necessariamente invalide o outro. A música retrata aquele momento em que alguém percebe que encontrou uma relação tão significativa que já não consegue imaginar o futuro sem considerá-la parte dele.

No fundo, “honeybee” não fala apenas sobre o desejo de permanecer ao lado de alguém. Fala sobre o que acontece psicologicamente quando deixamos outra pessoa se tornar importante o suficiente para nos afetar profundamente. Olivia descobre que se apaixonar não significa apenas experimentar alegria, encantamento e segurança, mas também aceitar uma forma de vulnerabilidade que não pode ser completamente evitada. E talvez seja por isso que sua declaração mais intensa não seja uma promessa de eternidade, mas um desejo silencioso de continuidade. Ela não sabe se aquele amor vai durar para sempre. Sabe apenas que, se pudesse escolher, passaria a vida inteira conhecendo aquele rosto.`,

    forYou:
      "Você já sofreu tanto por amor que chegou a acreditar que nunca mais sentiria algo tão bonito? Mas, quando menos esperava, conheceu alguém que fez seu coração voltar a acreditar no romance? Então “honeybee” pode ser a trilha sonora do seu diário! Essa música é para quem ama os pequenos gestos, encontra felicidade em uma simples companhia e deseja guardar cada momento especial. E também para quem, mesmo estando muito feliz, às vezes sente aquele medinho de perder alguém que se tornou importante demais. Afinal, querer que uma história dure para sempre é uma coisa muito humana, né? 🐝💗",

    quizTitle: "VOCÊ JÁ AMOU ASSIM? ♡",
    quizIntro:
      "Aquele amor doce que também dá um friozinho na barriga! Quantas dessas situações você já viveu?",

    quizQuestions: [
      "💗 Já conheceu alguém que fez você voltar a acreditar no amor depois de uma grande decepção?",
      "🌙 Já sentiu tanta segurança ao lado de alguém que até os momentos difíceis pareciam menos assustadores?",
      "🥺 Já ficou com medo de perder uma pessoa mesmo quando tudo estava dando certo entre vocês?",
      "💌 Já gostou tanto de alguém que começou a imaginar uma vida inteira ao lado dessa pessoa?"
    ],

    moodDescription:
      "Passeios à noite, mãos entrelaçadas, jardins secretos e aquele amor tão doce que a gente gostaria de guardar para sempre. 🐝💗"
  };

  const honeybeeIntro =
    "Depois de tantas decepções amorosas, Olivia Rodrigo finalmente encontrou alguém que faz até os momentos mais simples parecerem especiais. Em “honeybee”, a cantora celebra um amor doce, tranquilo e cheio de carinho, daqueles que fazem a gente querer congelar o tempo.\n\nMas existe um detalhe que deixa tudo ainda mais emocionante: quanto mais feliz ela está, mais percebe que tem algo precioso a perder. Entre passeios românticos, declarações sinceras e o desejo de permanecer juntinhos, Olivia descobre que amar também significa se permitir sentir um pouquinho de medo. 💌";

  /*
    LOVE LAB DA EDIÇÃO HONEYBEE
    A reportagem fica guardada em uma janela.
  */

  const honeybeeLab = `
    <article class="love-lab-modal">
      <div class="love-lab-modal-header">
        <span class="love-lab-modal-tag">
          EDIÇÃO #02 | O MEDO DE PERDER O AMOR
        </span>
        <h2 class="love-lab-modal-title">
          ♡ LOVE LAB: Experimentos do coração
        </h2>
      </div>

      <div class="love-lab-modal-paper">
        <h3>
          ♡ Por que temos tanto medo de perder alguém
          quando finalmente estamos felizes?
        </h3>

        <p class="love-lab-lead">
          Você está apaixonada, tudo parece estar dando certo
          e aquela pessoa faz até os dias mais comuns parecerem
          especiais. Mas, do nada, surge um pensamento:
          “E se um dia eu perder tudo isso?”.
          O relacionamento nem está em crise, mas sua cabeça
          já está imaginando uma despedida digna de filme triste.
          Amiga, por que nosso cérebro insiste em pensar no pior
          justamente quando estamos vivendo algo tão bom?
          A psicologia tem uma explicação!
        </p>

        <h3>🧠 O cérebro tem medo de perder o que ama?</h3>

        <p>
          Você já percebeu como a possibilidade de perder algo
          pode parecer muito mais assustadora do que a felicidade
          de conquistá-lo? Pois é! Esse fenômeno tem nome:
          <strong>aversão à perda</strong>.
        </p>

        <p>
          Os psicólogos Daniel Kahneman e Amos Tversky estudaram
          como as pessoas tomam decisões diante de possibilidades
          de ganhos e perdas. Em suas pesquisas, observaram que,
          em determinadas situações, o impacto psicológico de
          perder alguma coisa tende a ser maior do que a satisfação
          de ganhar algo equivalente.
        </p>

        <p>
          Mas o que isso tem a ver com o amor?
          TUDO, pelo menos como uma possível maneira de
          compreender nossas preocupações românticas!
        </p>

        <p>
          Quando nos apaixonamos, aquela pessoa começa a ocupar
          um lugar especial na nossa vida. Criamos memórias,
          imaginamos planos e descobrimos uma felicidade que
          talvez nem soubéssemos que existia.
          Só que, quanto mais valorizamos tudo isso,
          mais assustadora pode parecer a possibilidade de perder.
        </p>

        <p>
          É justamente essa contradição que aparece em “honeybee”,
          quando Olivia Rodrigo canta que espera nunca precisar
          ver o rosto da pessoa amada indo embora.
          Ela não está necessariamente sofrendo por uma separação.
          Está feliz, apaixonada e vivendo algo especial.
          Mas perceber o quanto ama alguém também significa
          reconhecer o quanto uma despedida poderia doer.
        </p>

        <p>
          E aqui vem a parte mais interessante:
          <strong>
            sentir medo de perder uma pessoa não significa
            que você acredita que ela vai embora.
          </strong>
          Às vezes, significa apenas que você reconhece
          o valor que aquele relacionamento tem na sua vida.
        </p>

        <p>
          É importante lembrar que os estudos originais sobre
          aversão à perda não investigaram especificamente
          o medo de separações amorosas. A relação com
          “honeybee” é uma interpretação psicológica
          do sentimento apresentado na música.
        </p>

        <div class="love-lab-message">
          <h4>💌 VEREDITO DO LOVE LAB:</h4>
          <p>
            Talvez uma das partes mais assustadoras de se
            apaixonar seja perceber que agora existe alguém
            cuja ausência faria uma diferença enorme na sua vida.
            Mas não vale deixar o medo de um possível fim
            roubar a felicidade de um amor que está
            acontecendo agora, né?
          </p>
        </div>

        <div class="love-lab-source">
          <strong>📚 REFERÊNCIA CIENTÍFICA:</strong>
          <p>
            Kahneman, D., &amp; Tversky, A. (1979).
            <em>
              Prospect Theory: An Analysis of Decision under Risk.
            </em>
            Econometrica, 47(2), 263 a 291.
            <a
              href="https://doi.org/10.2307/1914185"
              target="_blank"
              rel="noopener noreferrer"
            >Consultar o estudo</a>.
          </p>
        </div>
      </div>
    </article>
  `;

  let storedLab = null;
  let currentlyHoneybee = false;

  const isHoneybee = () => {
    const title = document.querySelector("#articleTitle");
    const artist = document.querySelector("#articleArtist");

    return !!title && !!artist &&
      title.textContent.trim().toLowerCase() === "honeybee" &&
      artist.textContent.toLowerCase().includes("olivia rodrigo");
  };

  /*
    Insere a música no catálogo já carregado.
    Aguarda o app.js terminar de ler songs.json.
  */

  async function registerSong() {
    let attempts = 0;

    const tryRegister = () => {
      attempts += 1;

      try {
        if (typeof songs !== "undefined" &&
            Array.isArray(songs) &&
            songs.length > 0) {

          const exists = songs.some(s =>
            s.title.toLowerCase() === "honeybee" &&
            s.artist.toLowerCase() === "olivia rodrigo"
          );

          if (!exists) {
            songs.push(honeybee);
          }

          /*
            Se a pessoa abrir o endereço da edição,
            mostra honeybee diretamente.
          */

          const hash = decodeURIComponent(
            location.hash.replace(/^#/, "")
          ).toLowerCase();

          if (hash.includes("honeybee") &&
              typeof applyTrack === "function" &&
              !isHoneybee()) {

            applyTrack({
              ...honeybee,
              cover: honeybee.cover
            }, false);
          }

          return true;
        }
      } catch (error) {
        console.warn("XOXO Honeybee:", error);
      }

      return attempts >= 160;
    };

    if (tryRegister()) return;

    const timer = setInterval(() => {
      if (tryRegister()) {
        clearInterval(timer);
      }
    }, 250);
  }

  function updateHoneybeeEdition() {
    const lab = document.querySelector("#loveLab");
    const template = document.querySelector("#loveLabFullArticle");
    const article = document.querySelector("#articleDescription");
    const heading = document.querySelector(".intro-highlight");

    if (!lab || !template) return;

    if (!storedLab) {
      storedLab = {
        header: lab.querySelector(".love-lab-tag")?.textContent || "",
        brand: lab.querySelector(".love-lab-brand")?.textContent || "",
        question: lab.querySelector(".love-lab-preview h3")?.textContent || "",
        preview: lab.querySelector(".love-lab-preview p")?.textContent || "",
        full: template.innerHTML,
        heading: heading?.textContent || ""
      };
    }

    const active = isHoneybee();

    if (active) {
      if (!currentlyHoneybee) {
        const tag = lab.querySelector(".love-lab-tag");
        const brand = lab.querySelector(".love-lab-brand");
        const question = lab.querySelector(".love-lab-preview h3");
        const preview = lab.querySelector(".love-lab-preview p");

        if (tag) {
          tag.textContent =
            "EDIÇÃO #02 | O MEDO DE PERDER O AMOR";
        }
        if (brand) {
          brand.textContent =
            "♡ LOVE LAB: Experimentos do coração";
        }
        if (question) {
          question.textContent =
            "♡ Por que temos tanto medo de perder alguém quando finalmente estamos felizes?";
        }
        if (preview) {
          preview.textContent =
            "Você está apaixonada, tudo parece estar dando certo e aquela pessoa faz até os dias mais comuns parecerem especiais. Mas, do nada, surge um pensamento: “E se um dia eu perder tudo isso?”. O relacionamento nem está em crise, mas sua cabeça já está imaginando uma despedida digna de filme triste. Amiga, por que nosso cérebro insiste em pensar no pior justamente quando estamos vivendo algo tão bom? A psicologia tem uma explicação!";
        }

        template.innerHTML = honeybeeLab;
        currentlyHoneybee = true;
      }

      if (heading) {
        heading.textContent =
          "CRUSH ALERT! ♡ Quando amar também dá um friozinho na barriga!";
      }

      if (article &&
          article.textContent !== honeybeeIntro) {
        article.textContent = honeybeeIntro;
      }

      /*
        A edição antiga tem uma regra que esconde
        o LOVE LAB de outras músicas.
        Aqui liberamos o cartão em honeybee.
      */
      if (lab.hidden) {
        lab.hidden = false;
      }

    } else if (currentlyHoneybee && storedLab) {
      const tag = lab.querySelector(".love-lab-tag");
      const brand = lab.querySelector(".love-lab-brand");
      const question = lab.querySelector(".love-lab-preview h3");
      const preview = lab.querySelector(".love-lab-preview p");

      if (tag) tag.textContent = storedLab.header;
      if (brand) brand.textContent = storedLab.brand;
      if (question) question.textContent = storedLab.question;
      if (preview) preview.textContent = storedLab.preview;

      template.innerHTML = storedLab.full;

      if (heading) {
        heading.textContent = storedLab.heading;
      }

      currentlyHoneybee = false;
    }
  }

  function installEdition() {
    const title = document.querySelector("#articleTitle");
    const artist = document.querySelector("#articleArtist");
    const lab = document.querySelector("#loveLab");

    if (!title || !artist) return;

    const onChange = () => {
      requestAnimationFrame(updateHoneybeeEdition);
    };

    const observer = new MutationObserver(onChange);

    [title, artist].forEach(el => {
      observer.observe(el, {
        childList: true,
        subtree: true,
        characterData: true
      });
    });

    /*
      Se o código da edição anterior tentar
      esconder o cartão, ele volta a aparecer
      somente quando honeybee estiver aberta.
    */
    if (lab) {
      const visibilityObserver = new MutationObserver(() => {
        if (isHoneybee() && lab.hidden) {
          requestAnimationFrame(() => {
            if (isHoneybee()) lab.hidden = false;
          });
        }
      });

      visibilityObserver.observe(lab, {
        attributes: true,
        attributeFilter: ["hidden"]
      });
    }

    const quizButton =
      document.querySelector("#livedResultButton");

    if (quizButton) {
      quizButton.addEventListener("click", () => {
        if (!isHoneybee()) return;

        const selected = document.querySelectorAll(
          "#livedQuestions input:checked"
        ).length;

        const outcome =
          document.querySelector("#livedOutcome");

        if (!outcome) return;

        const result = selected === 0
          ? "♡ Coração que vai no seu próprio ritmo! Nem toda história precisa começar com borboletas no estômago."
          : selected <= 2
            ? "💌 Romântica de coração aberto! Você valoriza os pequenos gestos e está aprendendo a aproveitar o presente."
            : "🐝 Honeybee girl! Você conhece bem essa mistura de ternura, felicidade e friozinho na barriga. Só não deixe o medo do futuro roubar seus momentos bons!";

        outcome.textContent = `${selected}/4 ♡ ${result}`;
      });
    }

    updateHoneybeeEdition();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", () => {
      installEdition();
      registerSong();
    });
  } else {
    installEdition();
    registerSong();
  }
})();
