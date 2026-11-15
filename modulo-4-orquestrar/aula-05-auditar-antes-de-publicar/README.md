# Orquestrar · Aula 5 · Auditar antes de publicar

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwo-05-auditar-antes-de-publicar

A carga grava numa tabela temporária, audita contra o que o banco já publica e só então publica.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: carregar.py, runbook.md.

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
```

Num terminal só dele, deixe o servidor do Prefect ligado: `uv run prefect server start`. Uma vez na sua máquina: `uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`. O painel fica em http://127.0.0.1:4200.

Comandos da aula: `uv run python fluxo.py` (com a lista estragada de propósito e de novo) e `uv run pytest`.
