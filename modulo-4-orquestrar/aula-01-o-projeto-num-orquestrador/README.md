# Orquestrar · Aula 1 · O projeto num orquestrador

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwo-01-o-projeto-num-orquestrador

O projeto vira um flow do Prefect, com uma task para cada etapa, e o registro do projeto aparece no terminal e no painel.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: fluxo.py, prefect.toml, baixar.py, pyproject.toml, uv.lock.

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

Comandos da aula: `uv run prefect server start` (num terminal só dele), `uv run python fluxo.py` e `uv run pytest`.
