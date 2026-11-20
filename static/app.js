(() => {
'use strict';
const catalog = window.DIARY_CATALOG || [];
const byKey = Object.fromEntries(catalog.map(song => [song.key,song]));
const $ = id => document.getElementById(id);
let active = byKey['drop dead'] || catalog[0];
let currentSpotifyId = null;
let photoURL = null;
let artworkNonce = 0;
const artworkCache = new Map();
let step = 0;
let answers = [];
const questions = [
 {q:'Quando uma música lembra alguém, você...', a:['Escuto cinco vezes e crio um filme na cabeça','Mando para a pessoa sem pensar duas vezes','Guardo a música só para mim','Vou descobrir cada detalhe da letra']},
 {q:'Seu momento favorito numa música é...',a:['O refrão que dá frio na barriga','A batida que faz dançar','O verso triste que parece ter sido escrito pra mim','Aquela frase que me faz pensar por dias']},
 {q:'Se sua vida amorosa fosse uma cena, seria...',a:['Um encontro inesperado à meia-noite','Uma declaração na chuva','Uma despedida dramática','Uma conversa longa e sincera']},
 {q:'Qual frase parece mais com você?',a:['Eu me apaixono por todas as possibilidades','Eu sinto tudo intensamente','Algumas músicas guardam minhas saudades','Eu adoro entender o que sinto']}
];
const results = [
 {title:'💗 A ROMÂNTICA DO REFRÃO',desc:'Você vive a música como quem escreve cenas no diário. Um olhar vira refrão, e uma conversa já rende uma playlist inteirinha. Sua imaginação é sua maior companheira — só não esquece de descobrir a pessoa de verdade também!'},
 {title:'⚡ A PROTAGONISTA POP',desc:'Quando a batida começa, você assume o controle da pista. É intensa, espontânea e gosta de viver suas histórias sem pedir licença. Seu coração merece uma música em alto volume!'},
 {title:'🌙 A GAROTA DA PLAYLIST SECRETA',desc:'Você guarda histórias em melodias. Aquela música antiga pode te transportar para uma lembrança em segundos. Tem um lado sensível e uma capacidade linda de sentir as nuances do que vive.'},
 {title:'🧠 A DETETIVE DAS LETRAS',desc:'Você não só escuta: percebe as entrelinhas, encontra referências e tenta entender cada sentimento. Sua curiosidade é sua marca registrada. A redação te contrataria para investigar os bastidores!'}
];
function cleanHtmlToText(html){const element=document.createElement('div');element.innerHTML=html || '';return element.textContent || '';}
function paragraphs(html){return (html||'').replace(/<br\s*\/?\s*>/gi,'\n').split(/\n\s*\n/).filter(Boolean);}
function setArt(img,url,fallback){img.onerror=()=>{img.onerror=null;img.src=fallback};img.src=url||fallback;}
function makeTag(text){const s=document.createElement('span');s.className='tag';s.textContent='# '+text;return s;}
function chooseSong(key,{scroll=false,fromSpotify=false}={}){
 const song=byKey[key];if(!song)return;
 active=song;
 $('article-title').textContent=song.title.toLowerCase();
 $('article-artist').textContent=song.artist.toUpperCase();
 $('article-summary').textContent=song.summary;
 $('mood').textContent=song.mood;
 $('for-you').textContent='Para quem está vivendo um momento de '+song.mood+' e encontra uma história nos próprios fones de ouvido. ♡';
 for(const id of ['article-tags','mood-tags']){const parent=$(id);parent.replaceChildren();song.tags.forEach(t=>parent.append(makeTag(t)));}
 const lyricsBox=$('lyrics');lyricsBox.replaceChildren();
 const stanzas=(song.translation||'Ainda não há tradução cadastrada para esta música.').replace(/\r/g,'').split(/\n\s*\n/);
 stanzas.forEach(stanza=>{const block=document.createElement('p');block.className='verse';block.textContent=stanza.trim();lyricsBox.append(block)});
 const gossip=$('gossip');gossip.replaceChildren();
 if(song.gossip&&song.gossip.length){song.gossip.forEach((content,i)=>{const block=document.createElement('div');block.className='gossip-card';// Textos editoriais locais do arquivo content.json, nunca de fontes externas.
 block.innerHTML='<small>★ NOTA '+String(i+1).padStart(2,'0')+'</small><div>'+content+'</div>';gossip.append(block)})}
 else{gossip.textContent='Em breve: mais bastidores dessa faixa ♡';}
 const psych=$('psychology');psych.replaceChildren();
 (paragraphs(song.psychology)).forEach(p=>{const block=document.createElement('p');block.innerHTML=p;psych.append(block)});
 const rec=$('recommendations');rec.replaceChildren();
 const recommendations=catalog.filter(s=>s.key!==key).sort((a,b)=>{const aScore=a.tags.filter(x=>song.tags.includes(x)).length;const bScore=b.tags.filter(x=>song.tags.includes(x)).length;return bScore-aScore}).slice(0,4);
 recommendations.forEach(s=>{const a=document.createElement('a');a.className='rec-item';a.href='#materia';const b=document.createElement('b');b.textContent='♫ '+s.title;const small=document.createElement('span');small.textContent=s.artist;a.append(b,small);a.addEventListener('click',()=>chooseSong(s.key,{scroll:true}));rec.append(a)});
 document.querySelectorAll('.song-chip').forEach(b=>{const selected=b.dataset.key===key;b.classList.toggle('selected',selected);b.setAttribute('aria-pressed',String(selected))});
 if(!fromSpotify){$('track-title').innerHTML='';$('track-title').append(document.createTextNode(song.title.toLowerCase()+' '));const em=document.createElement('em');em.textContent='— '+song.artist;$('track-title').append(em);$('player-caption').textContent='Edição especial • escolha sua página favorita ♡';$('spotify-link').href=song.spotify_search;}
 $('feature-title').textContent=song.title+' — '+song.artist;
 $('feature-description').textContent=song.summary;
 $('feature-spotify-link').href=song.spotify_search;
 photoURL=null;
 loadArtwork(song);

 resetQuiz();if(scroll)$('materia').scrollIntoView({behavior:'smooth',block:'start'});
}
async function loadArtwork(song){
 const nonce=++artworkNonce;
 const fallbackCover=window.DIARY_CONFIG.staticBase+'cover.svg';
 const fallbackArtist=window.DIARY_CONFIG.staticBase+'collage.svg';
 setArt($('feature-cover'),fallbackCover,fallbackCover);
 setArt($('feature-artist'),fallbackArtist,fallbackArtist);
 setArt($('artist-photo'),fallbackArtist,fallbackArtist);
 $('feature-artist-caption').textContent=song.artist+' ♡';
 const embedBox=$('spotify-embed-box');embedBox.hidden=true;
 $('spotify-embed').removeAttribute('src');
 try{
  let info=artworkCache.get(song.key);
  if(!info){const res=await fetch('/api/artwork?key='+encodeURIComponent(song.key));if(!res.ok)return;info=await res.json();artworkCache.set(song.key,info)}
  if(nonce!==artworkNonce)return;
  if(info.cover){setArt($('feature-cover'),info.cover,fallbackCover);setArt($('cover'),info.cover,fallbackCover);}
  else setArt($('cover'),fallbackCover,fallbackCover);
  const artistPhoto=info.artist_image||info.cover;
  if(artistPhoto){setArt($('feature-artist'),artistPhoto,fallbackArtist);setArt($('artist-photo'),artistPhoto,fallbackArtist);$('photo-caption').textContent=song.artist+' ♡';}
  if(info.spotify_url){$('feature-spotify-link').href=info.spotify_url;if(!$('playing-label').textContent.includes('TOCANDO'))$('spotify-link').href=info.spotify_url;}
  if(info.spotify_id){$('spotify-embed').src='https://open.spotify.com/embed/track/'+encodeURIComponent(info.spotify_id)+'?utm_source=generator';embedBox.hidden=false;}
 }catch(e){console.warn('Capas indisponíveis agora',e)}
}
function setTab(which){for(const b of document.querySelectorAll('.tab')){const yes=b.dataset.tab===which;b.classList.toggle('active',yes);b.setAttribute('aria-selected',String(yes))}for(const page of document.querySelectorAll('.page'))page.classList.toggle('active',page.id==='page-'+which);const titles={letra:'[ PÁGINA 01 · LETRA & TRADUÇÃO ]',curiosidades:'[ PÁGINA 02 · FOFOCAS & BASTIDORES ]',psicologia:'[ PÁGINA 03 · PSICOLOGIA & COMPORTAMENTO ]'};$('window-title').textContent=titles[which]||titles.letra;}
function renderSongs(term=''){const strip=$('song-strip');strip.replaceChildren();let count=0;catalog.forEach(song=>{if(!((song.title+' '+song.artist).toLowerCase().includes(term.toLowerCase())))return;count++;const b=document.createElement('button');b.className='song-chip';b.dataset.key=song.key;b.setAttribute('aria-pressed',String(song.key===active?.key));const t=document.createElement('strong');t.textContent='♫ '+song.title;const a=document.createElement('small');a.textContent=song.artist;b.append(t,a);b.addEventListener('click',()=>chooseSong(song.key));strip.append(b)});$('song-count').textContent=count+' faixas';if(!count)strip.textContent='Nada por aqui ainda, amiga! Tente outra busca ♡';document.querySelectorAll('.song-chip').forEach(b=>b.classList.toggle('selected',b.dataset.key===active?.key));}
function resetQuiz(){step=0;answers=[];$('quiz-result').hidden=true;$('quiz-step').hidden=false;renderQuestion();}
function renderQuestion(){const q=questions[step];$('quiz-progress').textContent='PERGUNTA '+(step+1)+' DE '+questions.length;$('quiz-track-fill').style.width=((step+1)/questions.length*100)+'%';$('quiz-question').textContent=q.q;const target=$('quiz-options');target.replaceChildren();q.a.forEach((answer,i)=>{const b=document.createElement('button');b.textContent=String.fromCharCode(65+i)+') '+answer;b.onclick=()=>{answers.push(i);step++;if(step<questions.length)renderQuestion();else showResult()};target.append(b)})}
function showResult(){const totals=[0,0,0,0];answers.forEach(x=>totals[x]++);const max=Math.max(...totals);const winner=totals.findIndex(x=>x===max);$('result-title').textContent=results[winner].title;$('result-desc').textContent=results[winner].desc+' • Na edição de '+active.title+', sua vibe é '+active.mood+'.';$('quiz-step').hidden=true;$('quiz-result').hidden=false;}
function formatTime(ms){const s=Math.floor((ms||0)/1000);return Math.floor(s/60)+':'+String(s%60).padStart(2,'0')}
async function syncSpotify(){if(!window.DIARY_CONFIG.connected)return;try{const response=await fetch('/api/now-playing',{cache:'no-store'});if(!response.ok)return;const d=await response.json();if(!d.connected)return;if(!d.id){$('playing-label').textContent='♫ SPOTIFY CONECTADO · SEM MÚSICA';return;}$('playing-label').textContent=d.playing?'● TOCANDO AGORA':'❚❚ PAUSADO';$('track-title').textContent=d.name+' — '+d.artist;$('player-caption').textContent=d.album||'Spotify';$('elapsed').textContent=formatTime(d.progress);$('duration').textContent=formatTime(d.duration);$('bar-fill').style.width=(d.duration?Math.min(100,d.progress/d.duration*100):0)+'%';$('spotify-link').href=d.url||'https://open.spotify.com';setArt($('cover'),d.image,window.DIARY_CONFIG.staticBase+'cover.svg');if(d.id!==currentSpotifyId){currentSpotifyId=d.id;photoURL=d.artist_image||d.image;setArt($('artist-photo'),photoURL,window.DIARY_CONFIG.staticBase+'collage.svg');$('photo-caption').textContent=d.artist+' ♡';if(d.key)chooseSong(d.key,{fromSpotify:true});else{$('article-summary').textContent='Essa faixa está no seu Spotify! Nosso acervo ainda não tem uma edição especial dela. Escolha uma música na lista para ler uma matéria.';}}}catch(err){console.warn('Spotify temporariamente indisponível',err)}}
document.querySelectorAll('[data-tab]').forEach(b=>b.addEventListener('click',()=>{setTab(b.dataset.tab);if(!b.classList.contains('tab'))$('article-window').scrollIntoView({behavior:'smooth',block:'start'})}));document.querySelectorAll('[data-go]').forEach(b=>b.addEventListener('click',()=>$(b.dataset.go).scrollIntoView({behavior:'smooth'})));$('song-search').addEventListener('input',e=>renderSongs(e.target.value));$('restart-quiz').addEventListener('click',resetQuiz);document.querySelectorAll('[data-poll]').forEach(b=>b.addEventListener('click',()=>{$('poll-result').textContent=b.dataset.poll==='sim'?'A gente também! A vida inteira tem trilha sonora ♡':'Também vale! Tem música para cada fase da vida ♫';}));renderSongs();if(active)chooseSong(active.key);setTab('letra');syncSpotify();if(window.DIARY_CONFIG.connected)setInterval(syncSpotify,10000);
})();
