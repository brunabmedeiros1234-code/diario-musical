
/* XOXO — site estático e conexão Spotify via Authorization Code + PKCE. */

const $ = (q) => document.querySelector(q);
const $$ = (q) => Array.from(document.querySelectorAll(q));

const STORE = 'xoxo_spotify_pkce';

let songs = [], current = null, playing = null;
let lastProgress = 0, lastUpdate = 0;
let refreshTimer = null;
let selectedLyrics = 'translation';
let currentView = 'music';

const defaultCover = 'assets/album-drop-dead.webp';

const escapeHTML = (s='') =>
  String(s).replace(/[&<>"']/g, c => ({
    '&':'&amp;',
    '<':'&lt;',
    '>':'&gt;',
    '"':'&quot;',
    "'":'&#39;'
  }[c]));

const formatTime = ms => {
  let s = Math.floor(Math.max(0, ms || 0) / 1000);
  return `${Math.floor(s/60)}:${String(s%60).padStart(2,'0')}`;
};

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

$('#modal').addEventListener('click', e => {
  if (e.target.id === 'modal') closeModal();
});

window.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeModal();
});

// CLIENT ID DO SPOTIFY CONFIGURADO
// NUNCA COLOQUE O CLIENT SECRET.

const SPOTIFY_CLIENT_ID = '51ebc5fc21fa4e359bebdd37175c9f13';

const getID = () =>
  SPOTIFY_CLIENT_ID.trim() === 'COLE_SEU_CLIENT_ID_AQUI'
    ? ''
    : SPOTIFY_CLIENT_ID.trim();

// JANELA DE CONEXÃO DO SPOTIFY

function spotifySettings(message='') {
  modal(`
    <h2>♡ Conecte seu Spotify</h2>

    <p>
      Autorize sua própria conta para acompanhar
      a música que você está ouvindo.
      Cada pessoa verá apenas o Spotify dela.
    </p>

    ${!getID()
      ? '<div class="notice">O proprietário do site ainda precisa configurar o Client ID no arquivo app.js.</div>'
      : ''
    }

    ${message
      ? `<p class="notice">${escapeHTML(message)}</p>`
      : ''
    }

    <button class="action" id="saveSpotify"
      ${!getID() ? 'disabled' : ''}>
      ♡ Conectar meu Spotify
    </button>

    <button class="action" id="disconnectSpotify">
      Desconectar minha conta
    </button>
  `);

  $('#saveSpotify').onclick = () => startLogin();

  $('#disconnectSpotify').onclick = () => {
    localStorage.removeItem(STORE);
    sessionStorage.removeItem('xoxo_pkce_verifier');
    sessionStorage.removeItem('xoxo_oauth_state');

    playing = null;
    closeModal();

    $('#playingStatus').textContent = '♡ MODO REVISTA';
    $('#syncNote').textContent =
      'Spotify desconectado — você pode explorar a revista normalmente.';
  };
}

// AUTORIZAÇÃO SEGURA DO SPOTIFY

function randomString(n=64) {
  const letters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~';

  const nums = crypto.getRandomValues(new Uint8Array(n));

  return Array.from(
    nums,
    n => letters[n % letters.length]
  ).join('');
}

async function sha256(s) {
  return crypto.subtle.digest(
    'SHA-256',
    new TextEncoder().encode(s)
  );
}

const b64url = buf =>
  btoa(String.fromCharCode(...new Uint8Array(buf)))
    .replace(/\+/g,'-')
    .replace(/\//g,'_')
    .replace(/=+$/,'');

const redirect = () =>
  location.origin + location.pathname;

async function startLogin() {
  const id = getID();

  if (!id) return spotifySettings();

  const verifier = randomString();
  const state = randomString(24);
  const challenge = b64url(await sha256(verifier));

  sessionStorage.setItem('xoxo_pkce_verifier', verifier);
  sessionStorage.setItem('xoxo_oauth_state', state);

  const p = new URLSearchParams({
    response_type: 'code',
    client_id: id,
    scope: 'user-read-currently-playing user-read-playback-state',
    redirect_uri: redirect(),
    state,
    code_challenge_method: 'S256',
    code_challenge: challenge
  });

  location.href =
    'https://accounts.spotify.com/authorize?' + p;
}

async function exchange(params) {
  const response = await fetch(
    'https://accounts.spotify.com/api/token',
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      },
      body: new URLSearchParams(params)
    }
  );

  if (!response.ok) {
    let err = await response.text();

    throw new Error(
      `Não foi possível autorizar o Spotify (${response.status}). Confira o Client ID e o Redirect URI. ${err.slice(0,120)}`
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
  const u = new URL(location.href);
  const error = u.searchParams.get('error');
  const code = u.searchParams.get('code');

  if (!code && !error) return;

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

  const state = u.searchParams.get('state');
  const correct = sessionStorage.getItem('xoxo_oauth_state');
  const verifier = sessionStorage.getItem('xoxo_pkce_verifier');

  if (!state || state !== correct || !verifier) {
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

  } catch(e) {
    spotifySettings(e.message);
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

  } catch(e) {
    localStorage.removeItem(STORE);

    $('#syncNote').textContent =
      'A conexão expirou. Reconecte seu Spotify.';

    return null;
  }
}

// MÚSICA TOCANDO AGORA

async function loadNow() {
  const t = await getToken();

  if (!t) {
    if (getID()) {
      $('#syncNote').textContent =
        'Spotify ainda não autorizado. Clique em Conectar Spotify para concluir o acesso ♡';
    }
    return;
  }

  try {
    const res = await fetch(
      'https://api.spotify.com/v1/me/player/currently-playing',
      {
        headers: {
          Authorization: `Bearer ${t}`
        },
        cache: 'no-store'
      }
    );

    if (res.status === 204) {
      $('#playingStatus').textContent = '♫ NADA TOCANDO';
      $('#syncNote').textContent =
        'Dê play em alguma música no Spotify ♡';
      return;
    }

    if (res.status === 401) {
      const d = JSON.parse(
        localStorage.getItem(STORE) || '{}'
      );

      d.expires_at = 0;
      localStorage.setItem(STORE, JSON.stringify(d));
      return;
    }

    if (res.status === 403) {
      $('#syncNote').textContent =
        'A API do Spotify não liberou o acesso. Confira as permissões e o usuário autorizado.';
      return;
    }

    if (!res.ok) {
      throw new Error(`Spotify respondeu ${res.status}`);
    }

    const d = await res.json();

    if (!d.item || d.currently_playing_type !== 'track') {
      return;
    }

    playing = d;
    lastProgress = d.progress_ms || 0;
    lastUpdate = Date.now();

    renderNow(d);

    const tSong = d.item;
    const key = (tSong.id || '') + '-' + tSong.name;

    if (window.xoxoLastKey !== key) {
      window.xoxoLastKey = key;

      applyTrack({
        title: tSong.name,
        artist: tSong.artists?.map(a => a.name).join(', ') || 'Artista',
        cover: tSong.album?.images?.[0]?.url || defaultCover,
        spotifyUrl: tSong.external_urls?.spotify || '',
        duration: tSong.duration_ms,
        trackId: tSong.id
      }, true);
    }

  } catch(e) {
    $('#syncNote').textContent =
      'Não foi possível atualizar: ' + e.message;
  }
}

function renderNow(d) {
  $('#playingStatus').textContent = d.is_playing
    ? '▶ TOCANDO AGORA'
    : 'Ⅱ MÚSICA PAUSADA';

  $('#syncNote').textContent =
    '♡ Sincronizado com o seu Spotify';

  paintProgress();
}

function paintProgress() {
  const ms =
    playing?.item?.duration_ms || current?.duration || 0;

  const progress = playing
    ? lastProgress + (
        playing.is_playing
          ? Date.now() - lastUpdate
          : 0
      )
    : 0;

  $('#elapsed').textContent = formatTime(progress);
  $('#duration').textContent = formatTime(ms);

  $('#progressFill').style.width = ms
    ? `${Math.min(100, progress/ms*100)}%`
    : '0%';
}

// CONTEÚDO DA REVISTA

function findSong(title, artist) {
  return songs.find(
    s =>
      s.title.toLowerCase() === title.toLowerCase() &&
      s.artist.toLowerCase() === artist.toLowerCase()
  ) || null;
}

function applyTrack(track, isLive=false) {
  const song = findSong(track.title, track.artist);

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
    'Sua trilha sonora virou matéria de revista! ♡ Ainda não cadastramos a tradução, as curiosidades e a análise desta música.';

  $('#aboutText').textContent =
    current.intro ||
    `Agora é ${current.title}, de ${current.artist}, que está na sua playlist. Que sentimentos essa música desperta em você?`;

  const curiosityItems = current.curiosities || [];
  const cut = 5;

  const curiosityPart = curiosityItems.slice(0,cut);
  const detailsPart = curiosityItems.slice(cut);

  $('#percebePreview').innerHTML = detailsPart.length
    ? detailsPart.slice(0,2).map(x =>
        `<p>♡ ${escapeHTML(x).slice(0,235)}${x.length>235?'…':''}</p>`
      ).join('')
    : `<p>${escapeHTML(
        current.percebe ||
        'Os detalhes desta música ainda não foram cadastrados.'
      )}</p>`;

  $('#photoArtist').src =
    (song?.title === 'drop dead')
      ? 'assets/olivia-photo.webp'
      : (track.cover || defaultCover);

  $('#heroPortrait').src =
    (song?.title === 'drop dead')
      ? 'assets/olivia-hero.webp'
      : (track.cover || defaultCover);

  $('#heroArtist').innerHTML =
    escapeHTML(current.artist).replace(/ /g,'<br>') + ' ♡';

  const vibes = current.vibes || [
    ['No repeat',95],
    ['Meu momento',80],
    ['Playlist',90],
    ['Favorita',75]
  ];

  $('#vibes').innerHTML = vibes.map(
    ([name,n]) => `
      <div class="vibe-line">
        <span>${escapeHTML(name)} ♡</span>
        <span class="meter">
          <i style="width:${Number(n)}%"></i>
        </span>
        <b>${Number(n)}%</b>
      </div>
    `
  ).join('');

  $('#forYou').innerHTML =
    typeof current.forYou === 'string'
      ? `<p class="for-you-copy">${escapeHTML(current.forYou)}</p>`
      : Array.isArray(current.forYou)
        ? current.forYou.map(x =>
            `<p>${escapeHTML(x)} ♡</p>`
          ).join('')
        : '<p class="for-you-copy">Uma música especial para guardar no seu diário! ♡</p>';

  $('#curiosityPreview').innerHTML =
    (curiosityPart.length
      ? curiosityPart.slice(0,2)
      : ['Essa música ainda não tem curiosidades cadastradas.']
    ).map(x =>
      `<p>♡ ${escapeHTML(x).slice(0,230)}${x.length>230?'…':''}</p>`
    ).join('');

  $('#psyPreview').textContent = current.psychology
    ? current.psychology.replace(/^[^\n]*\n*/,'').slice(0,1050) + '…'
    : 'A análise psicológica desta faixa ainda não foi escrita.';

  renderLivedQuiz();
  renderMoodboard();
  renderLyrics();

  if (!isLive) {
    playing = null;
    lastProgress = 0;
    paintProgress();

    $('#playingStatus').textContent = '♡ NA REVISTA';

    $('#syncNote').textContent = getID()
      ? 'Aguardando atualização do Spotify...'
      : 'Conecte o Spotify para sincronizar automaticamente ♡';
  }

  history.replaceState(
    {},
    '',
    location.pathname + '#' +
    encodeURIComponent(current.title + '--' + current.artist)
  );
}

// TRADUÇÃO

function renderLyrics() {
  const txt =
    current?.translation ||
    'Ainda não temos tradução cadastrada para esta música.';

  $('#lyricsText').textContent = txt
    .replace(/ +(?=\n)/g,'')
    .replace(/\n{3,}/g,'\n\n');
}

$('#connectSpotify').onclick = () => spotifySettings();

// CURIOSIDADES E ANÁLISE PSICOLÓGICA

function showChapters(title,items) {
  modal(`
    <h2>${escapeHTML(title)} — ${escapeHTML(current.title)}</h2>

    ${items.length
      ? items.map(t =>
          `<div class="chapter">
            <p>${escapeHTML(t)}</p>
          </div>`
        ).join('')
      : '<p>Ainda não há textos cadastrados para esta seção.</p>'
    }
  `);
}

function showCurios() {
  showChapters(
    '☆ Curiosidades',
    (current.curiosities || []).slice(0,5)
  );
}

function showPercebe() {
  showChapters(
    '⌕ Você percebeu?',
    (current.curiosities || []).slice(5)
  );
}

function showPsy() {
  modal(`
    <h2>🧠 Análise psicológica: ${escapeHTML(current.title)}</h2>

    ${current.psychology
      ? current.psychology.split(/\n\n+/).map(
          p => `<p>${escapeHTML(p)}</p>`
        ).join('')
      : '<p>Esta análise ainda não foi cadastrada.</p>'
    }
  `);
}

$('#allCuriosities').onclick = showCurios;
$('#allPercebe').onclick = showPercebe;
$('#readPsychology').onclick = showPsy;

// QUIZ VOCÊ JÁ VIVEU ISSO?

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

  const questions = isDrop
    ? dropDeadQuestions
    : genericQuestions;

  $('#quizIntro').textContent = isDrop
    ? 'Uma paixão que começa com frio na barriga e mil possibilidades na cabeça... soa familiar?'
    : `Escutando ${current.title}, de ${current.artist}, será que você também já viveu uma história parecida?`;

  $('#livedQuestions').innerHTML = questions.map(
    (q,i) => `
      <label class="lived-question">
        <input type="checkbox" name="lived" value="${i}">
        <span class="heart-box">♡</span>
        <span>${escapeHTML(q)}</span>
      </label>
    `
  ).join('');

  $('#livedOutcome').textContent = '';
}

$('#livedResultButton').onclick = () => {
  const n = $$('#livedQuestions input:checked').length;

  const msg = n===0
    ? 'Ainda não viveu essa história? Talvez a próxima música seja a sua!'
    : n===1
      ? 'Um pedacinho dessa história já parece familiar!'
      : n===2
        ? 'Alerta de protagonista: você entende bem essa vibe!'
        : n===3
          ? 'Você e essa música têm mais em comum do que parece!'
          : 'MATCH TOTAL! Essa música poderia ser uma página do seu diário!';

  $('#livedOutcome').textContent =
    `${n}/4 ♡ ${msg}`;
};

// MOODBOARD DA MÚSICA

function renderMoodboard() {
  const drop =
    current.title.toLowerCase() === 'drop dead' &&
    current.artist.toLowerCase().includes('olivia rodrigo');

  $('#moodDescription').textContent = drop
    ? 'Versalhes, borboletas no estômago, bilhetinhos rosa e um encontro que não deveria acabar...'
    : `Recortes visuais para entrar no universo de ${current.title}.`;

  const img = $$('#moodCollage img');

  if (drop) {
    img[0].src = 'assets/mood-bar.webp';
    img[1].src = 'assets/mood-versailles.webp';
    img[2].src = 'assets/mood-hands.webp';
  } else {
    img.forEach(el =>
      el.src = current.cover || defaultCover
    );
  }

  img[0].alt = drop
    ? 'Bar de luz âmbar: o encontro da música'
    : `Moodboard de ${current.title}: capa`;

  img[1].alt = drop
    ? 'Pintura de anjos em Versalhes'
    : `Moodboard de ${current.title}: capa`;

  img[2].alt = drop
    ? 'Pintura a óleo de duas mãos entrelaçadas'
    : `Moodboard de ${current.title}: capa`;
}

// BUSCA DE MÚSICAS

function songSearch(q) {
  q = (q || '').trim();

  if (!q) return;

  const matches = songs.filter(
    s =>
      (s.title + ' ' + s.artist)
        .toLowerCase()
        .includes(q.toLowerCase())
  );

  modal(`
    <h2>⌕ Buscar no XOXO</h2>
    <p>Resultados para: <b>${escapeHTML(q)}</b></p>

    ${matches.map(
      s => `
        <div class="result" data-select="${escapeHTML(s.title)}">
          ♡ <b>${escapeHTML(s.title)}</b>
          — ${escapeHTML(s.artist)}
          <br>
          <small>Ver tradução, curiosidades e análise</small>
        </div>
      `
    ).join('') ||
    '<p>Nenhuma matéria cadastrada com esse nome. Você ainda pode ouvir a música no Spotify e a capa mudará automaticamente quando estiver tocando.</p>'
    }
  `);
}

$('#searchGo').onclick = () =>
  songSearch($('#search').value);

$('#search').addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    songSearch($('#search').value);
  }
});

document.addEventListener('click', e => {
  const t = e.target.closest('[data-select]');

  if (t) {
    const s = songs.find(
      s => s.title === t.dataset.select
    );

    if (s) {
      closeModal();
      applyTrack({
        ...s,
        cover: defaultCover
      }, false);
    }
  }

  const suggested = e.target.closest('[data-song]');

  if (suggested) {
    const q = suggested.dataset.song;

    window.open(
      'https://open.spotify.com/search/' +
      encodeURIComponent(q),
      '_blank',
      'noopener,noreferrer'
    );
  }
});

// NAVEGAÇÃO DA REVISTA

$$('.nav-btn').forEach(btn => btn.onclick = () => {
  currentView = btn.dataset.view;

  $$('.nav-btn').forEach(
    b => b.classList.toggle('active', b===btn)
  );

  if (currentView === 'music' || currentView === 'home') {
    if (currentView === 'home') {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    }
    return;
  }

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
      'Um diário musical com visual de revista teen dos anos 2013/2014. As músicas que você ouve no Spotify ganham uma capa especial aqui. As matérias completas dependem dos textos que você cadastrar.'
    ]
  };

  const [title,description] = pages[currentView];

  modal(`
    <h2>${title}</h2>
    <p>${description}</p>

    ${currentView === 'tests'
      ? '<button class="action" id="launchQuiz">Fazer teste ♡</button>'
      : currentView === 'artists'
        ? songs.map(
            s => `
              <div class="result" data-select="${escapeHTML(s.title)}">
                ♡ ${escapeHTML(s.artist)} — ${escapeHTML(s.title)}
              </div>
            `
          ).join('')
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
});

// INICIALIZAÇÃO DO SITE

async function init() {
  try {
    const response = await fetch('songs.json');

    if (!response.ok) {
      throw new Error('songs.json indisponível');
    }

    songs = (await response.json()).songs || [];

  } catch(e) {
    $('#syncNote').textContent =
      'Erro ao carregar músicas: ' + e.message;
  }

  await handleCallback();

  let s = songs[0];

  if (s) {
    applyTrack({
      ...s,
      cover: defaultCover
    }, false);
  }

  await loadNow();

  refreshTimer = setInterval(loadNow, 12000);

  setInterval(paintProgress, 1000);
}

init();
