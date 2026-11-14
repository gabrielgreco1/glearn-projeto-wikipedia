# Transformar · Aula 2 · Ler a ficha de cada estado, sem pedir de novo

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwt-02-ler-a-ficha-de-cada-estado

O `ficha.py` lê a ficha das 27 páginas que a PW-05 guardou e grava o texto de cada campo, como está na página, em `dados/fichas.csv`. Nenhum pedido ao site.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: ficha.py, testes/test_ficha.py, testes/amostra_ficha.html.

## Como rodar esta pasta

```
cd projeto
cp .env.example .env
```

Abra o `.env` e troque o contato pelo seu (um e-mail ou o endereço do seu repositório). Depois:

```
uv sync
uv run python rodar.py
```

O `rodar.py` cria a pasta `dados/`, com as 27 páginas dos estados. Se ela já existe, ele não faz pedido nenhum.

Comandos da aula, nesta ordem: `uv run python ficha.py` e `uv run pytest`. Cada programa lê o que o anterior gravou em `dados/`.
