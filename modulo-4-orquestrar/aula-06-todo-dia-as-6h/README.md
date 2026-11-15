# Orquestrar · Aula 6 · Todo dia às 6h, no horário de Brasília

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwo-06-todo-dia-as-6h-no-horario

O fluxo.py agendar fica ligado e roda o projeto todo dia às 6h, no horário de Brasília.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: fluxo.py, runbook.md.

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

Comandos da aula: `uv run python fluxo.py agendar` (num terminal que fica aberto) e `uv run prefect deployment run projeto-wikipedia/todo-dia`.
