# Transformar · Aula 3 · Do texto ao número

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwt-03-do-texto-ao-numero

O `numeros.py` tira da célula o ranking, a nota e a unidade, e converte área, municípios, PIB per capita, IDH e ano em número.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: numeros.py, testes/test_numeros.py.

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

Comandos da aula, nesta ordem: `uv run python ficha.py`, `uv run python numeros.py` e `uv run pytest`. Cada programa lê o que o anterior gravou em `dados/`.
