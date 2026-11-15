# Orquestrar · Aula 3 · O aviso de falha e o runbook

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwo-03-o-aviso-de-falha-e-o

Uma execução que termina em Failed ou Crashed deixa uma linha em avisos.log, e o runbook.md diz o que fazer com ela.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: fluxo.py, runbook.md, .gitignore.

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

Comandos da aula: `uv run python fluxo.py` (com o banco desligado, sem rede e normal) e `uv run pytest`.
