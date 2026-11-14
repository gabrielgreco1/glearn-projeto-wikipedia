# Transformar · Aula 7 · Perguntar em SQL e fechar a etapa

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwt-07-perguntar-em-sql-e-fechar-a

O `consultar.py` pergunta em SQL, com o DuckDB, direto no Parquet do silver e grava a resposta no gold. O `transformar.py` roda a etapa inteira com um comando.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: consultar.py, transformar.py, README.md, pyproject.toml, uv.lock.

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

Comandos da aula, nesta ordem: `uv run python transformar.py` e `uv run pytest`. Cada programa lê o que o anterior gravou em `dados/`.
