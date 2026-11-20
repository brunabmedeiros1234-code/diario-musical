# ♡ XOXO My Music Diary

Revista musical com visual inspirado nas revistas teen brasileiras de 2013–2014: capas, colagens, tradução, curiosidades, análise psicológica, quiz interativo, pesquisa e integração opcional com Spotify.

## O que já funciona
- **Abre sem Spotify**, já com uma edição de *drop dead* e 22 faixas cadastradas.
- Navegação por três páginas (tradução, bastidores e psicologia).
- Quiz interativo com quatro perguntas e resultados personalizados.
- Busca das faixas, cards de recomendações, enquete interativa e visual responsivo.
- Ilustrações SVG originais já incluídas. Quando conectado, as capas de álbum e imagens disponibilizadas pela API do Spotify aparecem automaticamente.
- Traduções e análises originalmente cadastradas foram preservadas; a tradução de *drop dead* foi completada com o texto fornecido na conversa. Alguns outros textos já eram resumos no original.

## Publicar sem editar o código

**1.** No GitHub, crie um repositório e envie **todos os arquivos e pastas deste ZIP**, preservando `templates/` e `static/`.

**2.** O GitHub **guarda o código, mas não executa aplicativos Python Flask** pelo GitHub Pages. Para colocar o site no ar, entre em https://render.com/ e selecione `New` → `Blueprint`, conecte seu repositório e aplique o `render.yaml` que já está aqui. O plano e disponibilidade gratuitos podem mudar.

**3.** Depois do primeiro deploy, o site abre **em modo revista**, mesmo sem configurar o Spotify. Para sincronizar com sua conta, crie um app no https://developer.spotify.com/dashboard e configure as três variáveis abaixo **no painel do Render**, sem colar chaves no GitHub:

| Variável | O que preencher |
|---|---|
| `SPOTIPY_CLIENT_ID` | Client ID do Spotify Developer |
| `SPOTIPY_CLIENT_SECRET` | Client Secret do Spotify Developer |
| `SPOTIPY_REDIRECT_URI` | `https://SEU-ENDERECO.onrender.com/callback` |

Cadastre **exatamente a mesma redirect URI** nas configurações do app do Spotify. Depois reinicie/redeploy o serviço se necessário. Spotify pode restringir quais contas podem autenticar em apps em modo de desenvolvimento.

> Importante: o arquivo original enviado continha uma chave secreta. **Revogue/regenere essa chave no painel do Spotify antes de publicar**. Este projeto não inclui a chave antiga.

## Usar no computador (opcional)

`pip install -r requirements.txt` e `python app.py`. Abra http://127.0.0.1:5000 . Sem credenciais, funciona em modo revista.

## Limites conhecidos
- O projeto **não reproduz áudio diretamente**: mostra o status da música que está tocando no seu Spotify e oferece um link para abrir a faixa. Reprodução e pausa continuam no app Spotify.
- Sem conexão com Spotify, usa ilustrações originais em vez de fingir que são fotos de artistas. As imagens reais dependem dos dados disponibilizados pela API.
- O conteúdo manual está no `content.json`; textos já resumidos no código original continuam resumidos e não foram inventados trechos para completar.
- Tokens Spotify ficam em memória do servidor: adequados para uma versão pessoal com um único worker, não para uma rede social de alta escala.
- O quiz é recreativo e não constitui teste psicológico científico.
