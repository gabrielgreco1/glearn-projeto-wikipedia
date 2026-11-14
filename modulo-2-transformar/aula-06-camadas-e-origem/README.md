# Transformar · Aula 6 · Camadas e a origem de cada valor

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwt-06-camadas-e-a-origem-de-cada

O `camadas.py` faz o inventário do bronze, com o sha256 de cada arquivo, e grava o silver em Parquet com a origem de cada linha.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: camadas.py, testes/test_camadas.py, pyproject.toml, uv.lock.

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

Comandos da aula, nesta ordem: `uv run python ficha.py`, `uv run python numeros.py`, `uv run python pib.py`, `uv run python camadas.py` e `uv run pytest`. Cada programa lê o que o anterior gravou em `dados/`.
