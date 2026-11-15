# Orquestrar · Aula 4 · A coleta do dia e a retomada

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwo-04-a-coleta-do-dia-e-a

Cada dia tem a sua coleta em dados/, a anterior fica em dados_anterior/, e uma coleta interrompida continua de onde parou. A carga grava a impressão digital do banco.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: coleta.py, fluxo.py, baixar.py, carregar.py, schema.sql, .gitignore, testes/test_coleta.py.

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

Comandos da aula: `uv run python fluxo.py` (com Ctrl+C no meio, de novo, e do zero) e `uv run pytest`.
