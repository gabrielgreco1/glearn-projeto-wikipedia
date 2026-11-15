# Orquestrar · Aula 2 · Uma task por etapa e novas tentativas

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwo-02-uma-task-por-etapa-e-novas

A extração se divide em cinco tasks. As que pedem à Wikipedia são tentadas de novo quando a rede falha, e o erro de rede deixa de ser uma saída do programa.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: fluxo.py, paginas.py, resumos.py, testes/test_paginas.py.

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

Comandos da aula: `uv run python fluxo.py` (com e sem rede) e `uv run pytest`.
