
/* XOXO MY MUSIC DIARY
   Site estático + Spotify PKCE
   Curiosidades em páginas de revista
*/

const $ = q => document.querySelector(q);
const $$ = q => Array.from(document.querySelectorAll(q));

const STORE = 'xoxo_spotify_pkce';
const SPOTIFY_CLIENT_ID = '1ab7d1db359b4f11b020a79363e8da3c';

const defaultCover = 'assets/album-drop-dead.webp';

let songs = [];
let current = null;
let playing = null;
let lastProgress = 0;
let lastUpdate = 0;
let refreshTimer = null;
let currentView = 'music';
let manualSelection = false;

const escapeHTML = (value = '') =>
  String(value).replace(/[&<>"']/g, char => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[char]));

const formatTime = ms => {
  const seconds = Math.floor(Math.max(0, ms || 0) / 1000);
  return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
};

const getID = () => SPOTIFY_CLIENT_ID.trim();

const redirect = () => location.origin + location.pathname;

/* ====================================
   JANELINHAS DO SITE
==================================== */

function modal(html) {
  $('#modalBody').innerHTML = html;
  $('#modal').classList.remove('hidden');
  document.body.style.overflow = 'hidden';
}

function closeModal() {
  $('#modal').classList.add('hidden');
  document.body.style.overflow = '';
}

$('#closeModal').onclick = closeModal;

$('#modal').addEventListener('click', event => {
  if (event.target.id === 'modal') closeModal();
});

window.addEventListener('keydown', event => {
  if (event.key === 'Escape') closeModal();
});

/* ====================================
   SPOTIFY
==================================== */

function spotifySettings(message = '') {
  modal(`
    <h2>♡ Conecte seu Spotify</h2>

    <p>
      Autorize sua própria conta para acompanhar
      a música que você está ouvindo.
      Cada pessoa verá apenas o Spotify dela.
    </p>

    ${message
      ? `<p class="notice">${escapeHTML(message)}</p>`
      : ''
    }

    <button class="action" id="saveSpotify">
      ♡ Conectar meu Spotify
    </button>

    <button class="action" id="disconnectSpotify">
      Desconectar minha conta
    </button>
  `);

  $('#saveSpotify').onclick = startLogin;

  $('#disconnectSpotify').onclick = () => {
    localStorage.removeItem(STORE);
    sessionStorage.removeItem('xoxo_pkce_verifier');
    sessionStorage.removeItem('xoxo_oauth_state');

    playing = null;
    manualSelection = false;
    window.xoxoLastKey = null;

    closeModal();

    $('#playingStatus').textContent = '♡ MODO REVISTA';
    $('#syncNote').textContent =
      'Spotify desconectado — explore a revista normalmente.';
  };
}

function randomString(length = 64) {
  const letters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';

  const numbers = crypto.getRandomValues(
    new Uint8Array(length)
  );

  return Array.from(
    numbers,
    number => letters[number % letters.length]
  ).join('');
}

async function sha256(value) {
  return crypto.subtle.digest(
    'SHA-256',
    new TextEncoder().encode(value)
  );
}

const b64url = buffer =>
  btoa(String.fromCharCode(...new Uint8Array(buffer)))
    .replace(/\+/g, '-')
    .replace(/\//g, '_')
    .replace(/=+$/, '');

async function startLogin() {
  const verifier = randomString();
  const state = randomString(24);
  const challenge = b64url(await sha256(verifier));

  sessionStorage.setItem('xoxo_pkce_verifier', verifier);
  sessionStorage.setItem('xoxo_oauth_state', state);

  const parameters = new URLSearchParams({
    response_type: 'code',
    client_id: getID(),
    scope: 'user-read-currently-playing user-read-playback-state',
    redirect_uri: redirect(),
    state,
    code_challenge_method: 'S256',
    code_challenge: challenge
  });

  location.href =
    'https://accounts.spotify.com/authorize?' + parameters;
}

async function exchange(parameters) {
  const response = await fetch(
    'https://accounts.spotify.com/api/token',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams(parameters)
    }
  );

  if (!response.ok) {
    const error = await response.text();

    throw new Error(
      `Não foi possível autorizar o Spotify (${response.status}). ` +
      `Confira o Client ID e o Redirect URI. ${error.slice(0, 120)}`
    );
  }

  const data = await response.json();

  const previous = JSON.parse(
    localStorage.getItem(STORE) || '{}'
  );

  const payload = {
    access_token: data.access_token,
    refresh_token: data.refresh_token || previous.refresh_token,
    expires_at: Date.now() + data.expires_in * 1000 - 60000
  };

  localStorage.setItem(STORE, JSON.stringify(payload));

  return payload;
}

async function handleCallback() {
  const url = new URL(location.href);

  const error = url.searchParams.get('error');
  const code = url.searchParams.get('code');

  if (!code && !error) return;

  const state = url.searchParams.get('state');

  history.replaceState(
    {},
    '',
    redirect() + location.hash
  );

  if (error) {
    spotifySettings(
      'O Spotify não autorizou a conexão: ' + error
    );
    return;
  }

  const correctState = sessionStorage.getItem(
    'xoxo_oauth_state'
  );

  const verifier = sessionStorage.getItem(
    'xoxo_pkce_verifier'
  );

  if (!state || state !== correctState || !verifier) {
    spotifySettings(
      'A verificação de segurança expirou. Tente conectar novamente.'
    );
    return;
  }

  try {
    await exchange({
      grant_type: 'authorization_code',
      code,
      redirect_uri: redirect(),
      client_id: getID(),
      code_verifier: verifier
    });

    sessionStorage.removeItem('xoxo_pkce_verifier');
    sessionStorage.removeItem('xoxo_oauth_state');

    closeModal();
  } catch (error) {
    spotifySettings(error.message);
  }
}

async function getToken() {
  let data = JSON.parse(
    localStorage.getItem(STORE) || '{}'
  );

  if (!data.access_token) return null;

  if (Date.now() < data.expires_at) {
    return data.access_token;
  }

  if (!data.refresh_token) return null;

  try {
    data = await exchange({
      grant_type: 'refresh_token',
      refresh_token: data.refresh_token,
      client_id: getID()
    });

    return data.access_token;
  } catch (error) {
    localStorage.removeItem(STORE);

    $('#syncNote').textContent =
      'A conexão expirou. Reconecte seu Spotify.';

    return null;
  }
}

function renderNow(data) {
  $('#playingStatus').textContent = data.is_playing
    ? '▶ TOCANDO AGORA'
    : 'Ⅱ MÚSICA PAUSADA';

  $('#syncNote').textContent =
    '♡ Sincronizado com o seu Spotify';

  paintProgress();
}

function paintProgress() {
  const duration =
    playing?.item?.duration_ms || current?.duration || 0;

  const progress = playing
    ? lastProgress + (
        playing.is_playing
          ? Date.now() - lastUpdate
          : 0
      )
    : 0;

  $('#elapsed').textContent = formatTime(progress);
  $('#duration').textContent = formatTime(duration);

  $('#progressFill').style.width = duration
    ? `${Math.min(100, progress / duration * 100)}%`
    : '0%';
}

async function loadNow() {
  const token = await getToken();

  if (!token) {
    if (!manualSelection) {
      $('#syncNote').textContent =
        'Conecte seu Spotify para sincronizar automaticamente ♡';
    }
    return;
  }

  try {
    const response = await fetch(
      'https://api.spotify.com/v1/me/player/currently-playing',
      {
        headers: {
          Authorization: `Bearer ${token}`
        },
        cache: 'no-store'
      }
    );

    if (response.status === 204) {
      $('#playingStatus').textContent = '♫ NADA TOCANDO';

      if (!manualSelection) {
        $('#syncNote').textContent =
          'Dê play em alguma música no Spotify ♡';
      }

      return;
    }

    if (response.status === 401) {
      const data = JSON.parse(
        localStorage.getItem(STORE) || '{}'
      );

      data.expires_at = 0;

      localStorage.setItem(STORE, JSON.stringify(data));
      return;
    }

    if (response.status === 403) {
      $('#syncNote').textContent =
        'A API do Spotify não liberou o acesso. Confira as permissões.';
      return;
    }

    if (!response.ok) {
      throw new Error(`Spotify respondeu ${response.status}`);
    }

    const data = await response.json();

    if (!data.item || data.currently_playing_type !== 'track') {
      return;
    }

    playing = data;
    lastProgress = data.progress_ms || 0;
    lastUpdate = Date.now();

    if (manualSelection) {
      $('#playingStatus').textContent = '♡ NA REVISTA';
      $('#syncNote').textContent =
        'Você está lendo uma matéria da revista ♡';
      return;
    }

    renderNow(data);

    const track = data.item;
    const key = (track.id || '') + '-' + track.name;

    if (window.xoxoLastKey !== key) {
      window.xoxoLastKey = key;

      applyTrack({
        title: track.name,
        artist: track.artists?.map(a => a.name).join(', ') || 'Artista',
        cover: track.album?.images?.[0]?.url || defaultCover,
        spotifyUrl: track.external_urls?.spotify || '',
        duration: track.duration_ms,
        trackId: track.id
      }, true);
    }
  } catch (error) {
    $('#syncNote').textContent =
      'Não foi possível atualizar: ' + error.message;
  }
}

/* ====================================
   DADOS DAS MÚSICAS
==================================== */

function findSong(title, artist) {
  return songs.find(song =>
    song.title.toLowerCase() === title.toLowerCase() &&
    song.artist.toLowerCase() === artist.toLowerCase()
  ) || null;
}

function applyTrack(track, isLive = false) {
  const song = findSong(track.title, track.artist);

  if (!isLive) {
    manualSelection = true;
  }

  current = {
    ...track,
    ...(song || {}),
    cover: isLive
      ? track.cover
      : (song?.cover || track.cover || defaultCover),
    spotifyUrl: isLive
      ? track.spotifyUrl
      : (song?.spotifyUrl || track.spotifyUrl)
  };

  document.title =
    `${current.title} — ${current.artist} | XOXO My Music Diary`;

  $('#playerTitle').textContent =
    `${current.title} — ${current.artist}`;

  $('#articleTitle').textContent = current.title;
  $('#articleArtist').textContent = current.artist;

  $('#crumbTitle').textContent =
    `${current.title} — ${current.artist}`.toUpperCase();

  $('#albumCover').src = current.cover || defaultCover;

  $('#spotifyOpen').href =
    current.spotifyUrl || 'https://open.spotify.com/';

  $('#articleDescription').textContent =
    current.intro ||
    'Sua trilha sonora virou matéria de revista! ♡ Ainda não cadastramos o conteúdo desta música.';

  $('#aboutText').textContent =
    current.intro ||
    `Agora é ${current.title}, de ${current.artist}, que está na sua playlist.`;

  const curiosityItems = current.curiosities || [];

  const curiosityPart = curiosityItems.slice(0, 5);
  const detailsPart = curiosityItems.slice(5);

  $('#percebePreview').innerHTML = detailsPart.length
    ? detailsPart.slice(0, 2).map(text =>
        `<p>♡ ${escapeHTML(text).slice(0, 235)}${text.length > 235 ? '…' : ''}</p>`
      ).join('')
    : `<p>${escapeHTML(
        current.percebe ||
        'Os detalhes desta música ainda não foram cadastrados.'
      )}</p>`;

  $('#photoArtist').src =
    song?.title === 'drop dead'
      ? 'assets/olivia-photo.webp'
      : (track.cover || defaultCover);

  $('#heroPortrait').src =
    song?.title === 'drop dead'
      ? 'assets/olivia-hero.webp'
      : (track.cover || defaultCover);

  $('#heroArtist').innerHTML =
    escapeHTML(current.artist).replace(/ /g, '<br>') + ' ♡';

  const vibes = current.vibes || [
    ['No repeat', 95],
    ['Meu momento', 80],
    ['Playlist', 90],
    ['Favorita', 75]
  ];

  $('#vibes').innerHTML = vibes.map(([name, number]) => `
    <div class="vibe-line">
      <span>${escapeHTML(name)} ♡</span>
      <span class="meter">
        <i style="width:${Number(number)}%"></i>
      </span>
      <b>${Number(number)}%</b>
    </div>
  `).join('');

  $('#forYou').innerHTML =
    typeof current.forYou === 'string'
      ? `<p class="for-you-copy">${escapeHTML(current.forYou)}</p>`
      : Array.isArray(current.forYou)
        ? current.forYou.map(text =>
            `<p>${escapeHTML(text)} ♡</p>`
          ).join('')
        : '<p class="for-you-copy">Uma música especial para guardar no seu diário! ♡</p>';

  $('#curiosityPreview').innerHTML =
    (curiosityPart.length
      ? curiosityPart.slice(0, 2)
      : ['Essa música ainda não tem curiosidades cadastradas.']
    ).map(text =>
      `<p>♡ ${escapeHTML(text).slice(0, 230)}${text.length > 230 ? '…' : ''}</p>`
    ).join('');

  $('#psyPreview').textContent = current.psychology
    ? current.psychology.replace(/^[^\n]*\n*/, '').slice(0, 1050) + '…'
    : 'A análise psicológica desta faixa ainda não foi escrita.';

  renderLivedQuiz();
  renderMoodboard();
  renderLyrics();

  if (!isLive) {
    playing = null;
    lastProgress = 0;
    paintProgress();

    $('#playingStatus').textContent = '♡ NA REVISTA';
    $('#syncNote').textContent =
      'Você está explorando a revista ♡';
  }

  history.replaceState(
    {},
    '',
    location.pathname + '#' +
    encodeURIComponent(current.title + '--' + current.artist)
  );
}

/* ====================================
   TRADUÇÃO
==================================== */

function renderLyrics() {
  const text =
    current?.translation ||
    'Ainda não temos tradução cadastrada para esta música.';

  $('#lyricsText').textContent = text
    .replace(/ +(?=\n)/g, '')
    .replace(/\n{3,}/g, '\n\n');
}

$('#connectSpotify').onclick = spotifySettings;

/* ====================================
   CURIOSIDADES EM PÁGINAS
==================================== */

/*
  ESTA É A PARTE NOVA!

  Quando a pessoa clica em
  "Ver todas as curiosidades",
  aparece uma curiosidade por vez.

  Botões: Voltar e Avançar.

  As curiosidades continuam sendo
  carregadas do dados.json ou songs.json.
*/

function showPagedChapters(title, items, variant = 'curios') {
  const chapters = Array.isArray(items) && items.length
    ? items
    : ['Ainda não há textos cadastrados para esta seção.'];

  let index = 0;

  modal('<div id="chapterPager"></div>');

  function renderPage() {
    const chapter = String(chapters[index] || '');

    /*
      Se o texto começar com um título,
      separa o título do restante.

      Também reconhece o padrão:
      💘 TÍTULO! Texto da curiosidade...
    */

    let heading = '';
    let body = chapter;

    const lineBreak = chapter.indexOf('\n');

    if (lineBreak > 0 && lineBreak < 180) {
      heading = chapter.slice(0, lineBreak).trim();
      body = chapter.slice(lineBreak + 1).trim();
    } else {
      const match = chapter.match(
        /^(.{5,160}?[!?])\s+([\s\S]+)$/
      );

      if (match) {
        heading = match[1].trim();
        body = match[2].trim();
      }
    }

    const content = heading
      ? `
        <h3 class="chapter-page-title">
          ${escapeHTML(heading)}
        </h3>
        <p class="chapter-page-body">
          ${escapeHTML(body)}
        </p>
      `
      : `
        <p class="chapter-page-body">
          ${escapeHTML(chapter)}
        </p>
      `;

    $('#chapterPager').innerHTML = `
      <section
        class="chapter-pager chapter-pager--${variant}"
        aria-label="${escapeHTML(title)}"
      >

        <div class="chapter-pager-head">
          <p class="chapter-pager-kicker">
            XOXO MY MUSIC DIARY · EDIÇÃO ESPECIAL ♡
          </p>

          <h2>
            ${escapeHTML(title)} —
            ${escapeHTML(current.title)}
          </h2>

          <span class="chapter-pager-count">
            PÁGINA ${index + 1} DE ${chapters.length}
          </span>
        </div>

        <div class="chapter-pager-paper">
          <span
            class="chapter-pager-sticker"
            aria-hidden="true"
          >
            ✧ EXCLUSIVO!
          </span>

          ${content}
        </div>

        <div class="chapter-pager-navigation">
          <button
            class="chapter-pager-button"
            id="prevChapter"
            ${index === 0 ? 'disabled' : ''}
          >
            ← Voltar
          </button>

          <span
            class="chapter-pager-pages"
            aria-live="polite"
          >
            ${index + 1} / ${chapters.length}
          </span>

          <button
            class="chapter-pager-button"
            id="nextChapter"
            ${index === chapters.length - 1 ? 'disabled' : ''}
          >
            Avançar →
          </button>
        </div>
      </section>
    `;

    $('#prevChapter').onclick = () => {
      if (index > 0) {
        index--;
        renderPage();
      }
    };

    $('#nextChapter').onclick = () => {
      if (index < chapters.length - 1) {
        index++;
        renderPage();
      }
    };

    const scroller = document.querySelector('.modal-inner');

    if (scroller) {
      scroller.scrollTop = 0;
    }
  }

  renderPage();
}

function showCurios() {
  showPagedChapters(
    '☆ Curiosidades',
    (current.curiosities || []).slice(0, 5),
    'curios'
  );
}

function showPercebe() {
  showPagedChapters(
    '⌕ Você percebeu?',
    (current.curiosities || []).slice(5),
    'percebe'
  );
}

function showPsy() {
  modal(`
    <h2>
      🧠 Análise psicológica:
      ${escapeHTML(current.title)}
    </h2>

    ${
      current.psychology
        ? current.psychology
            .split(/\n\n+/)
            .map(paragraph =>
              `<p>${escapeHTML(paragraph)}</p>`
            ).join('')
        : '<p>Esta análise ainda não foi cadastrada.</p>'
    }
  `);
}

$('#allCuriosities').onclick = showCurios;
$('#allPercebe').onclick = showPercebe;
$('#readPsychology').onclick = showPsy;

/* ====================================
   TESTE VOCÊ JÁ VIVEU ISSO?
==================================== */

const dropDeadQuestions = [
  'Já pesquisou a vida de um crush na internet antes de conhecê-lo melhor?',
  'Já ficou com borboletas no estômago só de imaginar um beijo?',
  'Já passou uma noite inteira dando indiretas para alguém?',
  'Já imaginou um futuro inteiro com alguém que acabou de conhecer?'
];

const genericQuestions = [
  'Já sentiu que uma música descrevia exatamente a sua história?',
  'Já repetiu uma música só para reviver uma emoção?',
  'Já imaginou uma cena de filme ouvindo essa canção?',
  'Já quis mandar um trecho dessa música para alguém especial?'
];

function renderLivedQuiz() {
  const isDrop =
    current.title.toLowerCase() === 'drop dead' &&
    current.artist.toLowerCase().includes('olivia rodrigo');

  const questions =
    Array.isArray(current.quizQuestions) &&
    current.quizQuestions.length
      ? current.quizQuestions
      : (isDrop ? dropDeadQuestions : genericQuestions);

  $('#quizIntro').textContent =
    current.quizIntro ||
    (
      current.quizTitle && !isDrop
        ? current.quizTitle.replace(
            /^VOCÊ JÁ VIVEU ISSO?\s*[—–-]\s*/i,
            ''
          )
        : isDrop
          ? 'Uma paixão que começa com frio na barriga e mil possibilidades na cabeça... soa familiar?'
          : `Escutando ${current.title}, será que você já viveu uma história parecida?`
    );

  $('#livedQuestions').innerHTML = questions.map(
    (question, index) => `
      <label class="lived-question">
        <input
          type="checkbox"
          name="lived"
          value="${index}"
        >
        <span class="heart-box">♡</span>
        <span>${escapeHTML(question)}</span>
      </label>
    `
  ).join('');

  $('#livedOutcome').textContent = '';
}

$('#livedResultButton').onclick = () => {
  const checked = $$('#livedQuestions input:checked').length;

  const message = checked === 0
    ? 'Ainda não viveu essa história? Talvez a próxima música seja a sua!'
    : checked === 1
      ? 'Um pedacinho dessa história já parece familiar!'
      : checked === 2
        ? 'Alerta de protagonista: você entende bem essa vibe!'
        : checked === 3
          ? 'Você e essa música têm mais em comum do que parece!'
          : 'MATCH TOTAL! Essa música poderia ser uma página do seu diário!';

  $('#livedOutcome').textContent =
    `${checked}/4 ♡ ${message}`;
};

/* ====================================
   MOODBOARD
==================================== */

function renderMoodboard() {
  const drop =
    current.title.toLowerCase() === 'drop dead' &&
    current.artist.toLowerCase().includes('olivia rodrigo');

  const stupid =
    current.title.toLowerCase() === 'stupid song' &&
    current.artist.toLowerCase().includes('olivia rodrigo');

  $('#moodDescription').textContent =
    current.moodDescription ||
    (
      stupid
        ? 'Uma paixão intensa, meio caótica e completamente fora de controle: festa no fim da noite, cidade acesa e cartas cheias de sentimento.'
        : drop
          ? 'Versalhes, borboletas no estômago, bilhetinhos rosa e um encontro que não deveria acabar...'
          : `Recortes visuais para entrar no universo de ${current.title}.`
    );

  const images = $$('#moodCollage img');

  const fallback = drop
    ? [
        'assets/mood-bar.webp',
        'assets/mood-versailles.webp',
        'assets/mood-hands.webp'
      ]
    : stupid
      ? [
          'musicas/olivia-rodrigo-stupid-song/festa.jpg',
          'musicas/olivia-rodrigo-stupid-song/cidade.jpg',
          'musicas/olivia-rodrigo-stupid-song/cartas.jpg'
        ]
      : [
          current.cover || defaultCover,
          current.cover || defaultCover,
          current.cover || defaultCover
        ];

  images.forEach((image, index) => {
    const source = Array.isArray(current.moodboard)
      ? current.moodboard[index]
      : null;

    image.src = source || fallback[index] || defaultCover;

    image.alt =
      `Moodboard de ${current.title} — foto ${index + 1}`;
  });
}

/* ====================================
   BUSCA DE MÚSICAS
==================================== */

function songSearch(query) {
  query = (query || '').trim();

  if (!query) return;

  const matches = songs.filter(song =>
    (song.title + ' ' + song.artist)
      .toLowerCase()
      .includes(query.toLowerCase())
  );

  modal(`
    <h2>⌕ Buscar no XOXO</h2>

    <p>
      Resultados para:
      <b>${escapeHTML(query)}</b>
    </p>

    ${
      matches.map(song => `
        <div
          class="result"
          data-select="${escapeHTML(song.title)}"
        >
          ♡ <b>${escapeHTML(song.title)}</b>
          — ${escapeHTML(song.artist)}
          <br>
          <small>
            Ver tradução, curiosidades e análise
          </small>
        </div>
      `).join('') ||
      '<p>Nenhuma matéria cadastrada com esse nome.</p>'
    }
  `);
}

$('#searchGo').onclick = () =>
  songSearch($('#search').value);

$('#search').addEventListener('keydown', event => {
  if (event.key === 'Enter') {
    songSearch($('#search').value);
  }
});

document.addEventListener('click', event => {
  const selected = event.target.closest('[data-select]');

  if (selected) {
    const song = songs.find(
      item => item.title === selected.dataset.select
    );

    if (song) {
      closeModal();

      applyTrack({
        ...song,
        cover: defaultCover
      }, false);
    }
  }

  const suggested = event.target.closest('[data-song]');

  if (suggested) {
    window.open(
      'https://open.spotify.com/search/' +
      encodeURIComponent(suggested.dataset.song),
      '_blank',
      'noopener,noreferrer'
    );
  }
});

/* ====================================
   MENU DA REVISTA
==================================== */

$$('.nav-btn').forEach(button => {
  button.onclick = () => {
    currentView = button.dataset.view;

    $$('.nav-btn').forEach(item => {
      item.classList.toggle('active', item === button);
    });

    if (currentView === 'home') {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
      return;
    }

    if (currentView === 'music') return;

    const pages = {
      artists: [
        '☆ Artistas',
        'Conheça os artistas pelas músicas que você adicionar ao diário.'
      ],
      playlists: [
        '♫ Playlists',
        'Crie uma trilha sonora para seus crushes, dramas e dias inesquecíveis.'
      ],
      tests: [
        '♡ Testes',
        'Descubra qual música combina com você!'
      ],
      about: [
        'ⓘ Sobre o XOXO',
        'Um diário musical com visual de revista teen dos anos 2013/2014.'
      ]
    };

    const [title, description] = pages[currentView];

    modal(`
      <h2>${title}</h2>
      <p>${description}</p>

      ${
        currentView === 'tests'
          ? '<button class="action" id="launchQuiz">Fazer teste ♡</button>'
          : currentView === 'artists'
            ? songs.map(song => `
                <div
                  class="result"
                  data-select="${escapeHTML(song.title)}"
                >
                  ♡ ${escapeHTML(song.artist)}
                  — ${escapeHTML(song.title)}
                </div>
              `).join('')
            : ''
      }
    `);

    if (currentView === 'tests') {
      $('#launchQuiz').onclick = () => {
        closeModal();

        $('#livedQuestions').scrollIntoView({
          behavior: 'smooth',
          block: 'center'
        });
      };
    }
  };
});

/* ====================================
   INICIALIZAÇÃO DO SITE
==================================== */

async function init() {
  try {
    const response = await fetch('songs.json', {
      cache: 'no-store'
    });

    if (!response.ok) {
      throw new Error('songs.json indisponível');
    }

    const catalog = (await response.json()).songs || [];

    /*
      O songs.json aceita:
      - músicas escritas diretamente nele;
      - caminhos para dados.json em subpastas.
    */

    const loaded = await Promise.all(
      catalog.map(async entry => {
        if (typeof entry !== 'string') return entry;

        try {
          const result = await fetch(entry, {
            cache: 'no-store'
          });

          if (!result.ok) {
            throw new Error(`HTTP ${result.status}`);
          }

          return await result.json();
        } catch (error) {
          console.warn(
            'Não foi possível abrir a música:',
            entry,
            error
          );

          return null;
        }
      })
    );

    songs = loaded.filter(
      song => song && song.title && song.artist
    );

  } catch (error) {
    $('#syncNote').textContent =
      'Erro ao carregar músicas: ' + error.message;
  }

  await handleCallback();

  const firstSong = songs[0];

  if (firstSong) {
    /*
      Na primeira abertura, mostra a
      primeira música da revista.
    */

    applyTrack({
      ...firstSong,
      cover: defaultCover
    }, false);

    manualSelection = false;
  }

  await loadNow();

  refreshTimer = setInterval(loadNow, 12000);

  setInterval(paintProgress, 1000);
}

init();
