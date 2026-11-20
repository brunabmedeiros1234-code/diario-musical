# ♡ XOXO My Music Diary

Site estilo revista teen (Capricho / Todateen / Atrevida 2013–2014), criado com HTML, CSS e JavaScript. Não precisa de Flask, Python nem de banco de dados. Basta publicar como **site estático** no Render.

## 1. Subir os arquivos no GitHub

1. Crie um repositório novo no GitHub, por exemplo `xoxo-my-music-diary`.
2. Na página do repositório: **Add file → Upload files**. Arraste **o conteúdo da pasta** (index.html, styles.css, app.js, songs.json e a pasta assets), não a pasta externa inteira.
3. Clique em **Commit changes**. Confirme que `index.html` aparece na raiz do repositório.

## 2. Publicar no Render

1. Acesse https://dashboard.render.com/ e clique em **New → Static Site**.
2. Conecte o GitHub e selecione seu repositório.
3. Em **Build Command**, deixe vazio (se o formulário exigir, use `echo ready`).
4. Em **Publish Directory**, coloque apenas `.` (um ponto).
5. Clique em **Deploy Static Site**.

**Importante:** escolha *Static Site*, não *Web Service*, porque este projeto não usa Python/Flask. Se você tinha um serviço antigo com `gunicorn`, pode deixar esse serviço de lado e usar o novo Static Site.

## 3. Fazer a página acompanhar o Spotify

A sincronização usa a Spotify Web API (`/v1/me/player/currently-playing`), com login **Authorization Code + PKCE**, sem guardar Client Secret no site.

1. Acesse https://developer.spotify.com/dashboard e crie um aplicativo Spotify.
2. Copie o **Client ID**.
3. Em **Settings → Redirect URIs**, adicione **a URL exata do site no Render seguida de `/`**, por exemplo: `https://seu-site.onrender.com/`. Se usar domínio personalizado, adicione também a URL desse domínio, com `/`.
4. Salve no painel do Spotify.
5. Abra o site publicado, clique em **♡ Conectar Spotify**, cole o Client ID e faça o login na sua conta.
6. Comece a ouvir música no aplicativo do Spotify. O site consulta a reprodução aproximadamente a cada 12 segundos. Capa, título, artista e progresso são sincronizados. Se pausar, o site mostra o estado pausado.

**Atenção às limitações:** aplicativos Spotify em modo de desenvolvimento podem permitir acesso apenas às contas autorizadas pelo proprietário do aplicativo e podem estar sujeitos a requisitos de conta/plano e quotas definidos pelo Spotify. Se der erro 403, verifique a lista de usuários autorizados no dashboard. A API pode exigir certas permissões. O site não toca música por conta própria: o botão *Ouvir agora* abre o Spotify. As traduções e análises **não são fornecidas automaticamente pela API Spotify**. Para ter a matéria completa de cada música, você precisa cadastrar o conteúdo em `songs.json`.

## 4. Adicionar outras músicas

Abra `songs.json` no GitHub, clique no lápis ✎ e adicione outros objetos dentro do array `songs`. Use a estrutura de `drop dead` como exemplo. Campos: `title`, `artist`, `intro`, `translation`, `original` (apenas letras sobre as quais você tem autorização de publicação), `curiosities` (lista de textos), `psychology`, `percebe`, `vibes` (pares de nome e porcentagem), `forYou`. Não copie letras de terceiros sem autorização.

Quando a faixa tocar no Spotify, o site compara **título e nome do artista** com as matérias cadastradas. Caso não encontre, muda automaticamente capa, título e artista, e informa que a matéria ainda não foi cadastrada.

## Fotos e arte

As imagens iniciais foram recortadas da **imagem de referência fornecida por você**, para aproximar o visual do modelo. Para publicar publicamente, confirme que você tem direito de usar essas fotos/imagens ou substitua por arquivos próprios/licenciados na pasta `assets`. Algumas fotos incluem elementos gráficos da própria referência. O site usa fontes do Google Fonts; sem internet pode exibir fontes alternativas.

## Teste antes de publicar

Abra o terminal dentro da pasta e rode `python -m http.server 8000`, depois visite `http://localhost:8000/` (para o login Spotify, use o domínio HTTPS publicado no Render ou um redirect local compatível cadastrado no Spotify). Abrir `index.html` diretamente com `file://` pode impedir que o navegador carregue `songs.json`.

## Seções interativas da revista

A coluna lateral agora tem **💘 Você já viveu isso?** (quiz com quatro perguntas clicáveis e resultado) e **📸 Moodboard da música** (colagem de fotos). Para “drop dead”, as perguntas e a estética são específicas; para músicas ainda não cadastradas, a seção usa perguntas genéricas e a capa do Spotify. As antigas seções de sugestões de músicas, playlist, new music e mais conteúdo foram retiradas dos cartões.
