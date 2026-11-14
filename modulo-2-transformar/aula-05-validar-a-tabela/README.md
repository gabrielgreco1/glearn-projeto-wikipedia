# Transformar · Aula 5 · Validar a tabela com regras escritas

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwt-05-validar-a-tabela-com-regras-escritas

O `validar.py` escreve as regras da tabela com o pandera e confere todas de uma vez.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: validar.py, testes/test_validar.py, testes/amostra_pib.csv, pyproject.toml, uv.lock.

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

Comandos da aula, nesta ordem: `uv run python ficha.py`, `uv run python numeros.py`, `uv run python pib.py`, `uv run python validar.py` e `uv run pytest`. Cada programa lê o que o anterior gravou em `dados/`.
