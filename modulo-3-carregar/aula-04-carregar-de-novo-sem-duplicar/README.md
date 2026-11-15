# Carregar · Aula 4 · Carregar de novo sem duplicar

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwc-04-carregar-de-novo-sem-duplicar

A carga passa a ser um upsert pela sigla, com um hash só dos valores do estado: rodar de novo não duplica e não reescreve o que não mudou.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: carregar.py, schema.sql, testes/test_carregar.py.

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

Se o banco não estiver de pé (depois de desligar o computador, por exemplo), suba de novo com `docker compose up -d --wait`.

O `rodar.py` cria a pasta `dados/`, com as 27 páginas dos estados; depois, `uv run python transformar.py` grava a silver e a gold. Se `dados/` já existe, nada é pedido de novo.

Comandos da aula: `uv run python carregar.py` (duas vezes) e `uv run pytest`.
