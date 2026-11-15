# Carregar · Aula 2 · A tabela de destino: tipos e regras

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwc-02-a-tabela-de-destino-tipos-e

O `schema.sql` cria a tabela `estados`, com o tipo de cada coluna, a chave e as regras do pandera repetidas no banco.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: schema.sql, banco.py.

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

Comandos da aula: `uv run python banco.py`.
