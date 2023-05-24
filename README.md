# Programa de Publicação de Notícias e Retweet via Twitter

Este é um programa Python para um bot do Twitter que pode ler feeds RSS e postar novos itens no Twitter, além de pesquisar e retuitar tweets com palavras-chave específicas.

# Funcionalidades

- Leitura de RSS e postagem de novos itens no Twitter: O programa lê um feed RSS especificado e posta os novos itens no Twitter.
- Pesquisa e retweet de palavras-chave: O programa realiza uma pesquisa no Twitter com base em palavras-chave especificadas e retuita os tweets encontrados.

# Configuração
Antes de executar o programa, é necessário configurar as seguintes informações nas classes Settings e TwitterAuth:

# Configurações do aplicativo do Twitter (classe TwitterAuth)
- consumer_key: Insira a chave do consumidor do Twitter.
- consumer_secret: Insira o segredo do consumidor do Twitter.
- access_token: Insira o token de acesso do Twitter.
- access_token_secret: Insira o segredo do token de acesso do Twitter.

# Configurações do bot do Twitter (classe Settings)
- feed_url: Insira a URL do feed RSS que deseja postar no Twitter.
- posted_urls_output_file: Insira o nome do arquivo de log para salvar todos os links do feed RSS postados.
- posted_retweets_output_file: Insira o nome do arquivo de log para salvar todos os retweets feitos.
- retweet_include_words: Insira as palavras-chave que deseja incluir ao retuitar.
- retweet_exclude_words: Insira as palavras-chave que deseja excluir ao retuitar.

# Observação
Este programa requer as bibliotecas os, sys, feedparser, twython, datetime e dateutil para serem instaladas.

Certifique-se de ter instalado todas as dependências antes de executar o programa.
