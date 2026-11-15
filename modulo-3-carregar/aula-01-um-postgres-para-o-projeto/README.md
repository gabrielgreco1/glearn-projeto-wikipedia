# Carregar · Aula 1 · Um Postgres para o projeto

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwc-01-um-postgres-para-o-projeto

O Postgres do projeto sobe no Docker, com o `compose.yaml`, e o `banco.py` abre a primeira conexão.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: compose.yaml, .env.example, banco.py, pyproject.toml, uv.lock.

## Como rodar esta pasta

Você precisa do Docker instalado e aberto (no Windows e no Mac, o Docker Desktop).

```
cd projeto
cp .env.example .env
```

Abra o `.env` e troque o contato pelo seu (um e-mail ou o endereço do seu repositório). Depois:

```
docker compose up -d --wait
uv sync
uv run python rodar.py
```

O `rodar.py` cria a pasta `dados/`, com as 27 páginas dos estados; depois, `uv run python transformar.py` grava a silver e a gold. Se `dados/` já existe, nada é pedido de novo.

Comandos da aula: `docker compose up -d --wait`, `uv run python banco.py` e `uv run pytest`.
