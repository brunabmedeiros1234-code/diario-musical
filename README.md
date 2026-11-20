# XOXO My Music Diary ♡ — edição revista 2013/2014

Projeto completo, pronto para ser enviado ao GitHub e publicado no Render.

## Colocar a nova versão no GitHub (sem editar código)

1. Extraia o ZIP e **abra a pasta extraída**. Os arquivos `app.py`, `tradutor_spotify.py`, `content.json`, `render.yaml` e `requirements.txt` e as pastas `templates` e `static` devem ficar **na raiz** do repositório, sem uma pasta adicional ao redor deles.
2. No GitHub, abra seu repositório → **Add file → Upload files**. Arraste os arquivos **e as duas pastas**, aceitando substituir os arquivos existentes, e faça **Commit changes**.
3. No Render, mantenha **Settings → Root Directory** vazio, se os arquivos estão na raiz do GitHub. Vá em **Manual Deploy → Deploy latest commit**.
4. Acesse o site. O acervo, a busca, as análises e o teste funcionam sem entrar no Spotify.

## O que foi mudado

- Layout largo no computador (até 1720 px), adaptado a tablets e celulares.
- Letra/tradução em duas colunas no computador, mantendo os versos e as estrofes.
- Área editorial com fotografias e capas vinculadas à música: capas de álbuns consultadas no catálogo público do iTunes e, quando houver credenciais, também imagens dos artistas fornecidas pelo Spotify.
- Player incorporado do Spotify quando o Spotify fornece a identificação da faixa. Ele pode ter limitações de reprodução conforme a conta/região do ouvinte.
- Integração anterior com Spotify continua: a página acompanha a música tocada na conta conectada.
- Mantidos os conteúdos e testes do projeto anterior.

## Conectar Spotify — feito no painel, não no código

**Atenção: enviar ao GitHub NÃO conecta automaticamente uma conta Spotify.** Para autenticar sua conta, entre em https://developer.spotify.com/dashboard e crie um aplicativo do Spotify. Nas configurações desse aplicativo, cadastre a Redirect URI exata `https://SEU-SITE.onrender.com/callback`, trocando o domínio pelo endereço real do site.

No **Render → seu serviço → Environment**, crie estas variáveis, uma por vez:

- `SPOTIPY_CLIENT_ID` = Client ID do Spotify Developer
- `SPOTIPY_CLIENT_SECRET` = Client Secret do Spotify Developer
- `SPOTIPY_REDIRECT_URI` = URL exata de callback cadastrada no Spotify Developer, incluindo `https://` e `/callback`.

Salve as variáveis e faça um deploy. No site, clique em **Conectar meu Spotify**. A conexão usa o fluxo OAuth; somente usuários permitidos pelas regras do app Spotify podem ser autorizados. O Spotify pode exigir cadastro de usuários de teste no modo de desenvolvimento. O player incorporado só aparece para faixas encontradas no Spotify.

**Segurança:** o código original tinha um Client Secret fixo. Revogue essa credencial antiga no Spotify Developer. Não compartilhe o novo segredo nem o adicione em arquivos no GitHub.

## Notas

- A importação de imagens depende de serviços externos (Apple/iTunes/Spotify) e pode não encontrar determinada música. Nesse caso aparece uma colagem original, sem imagens quebradas.
- A reprodução de áudio não é controlada pelo site: o player Spotify incorporado e o app Spotify controlam seu próprio áudio. A barra da música em execução é um monitor visual da API.
- O Render pode reiniciar o serviço, invalidando sessões temporárias. Isso não impede usar o modo revista.
- O conteúdo de algumas músicas já estava resumido no código original. Não foram inventados versos para completá-las.
