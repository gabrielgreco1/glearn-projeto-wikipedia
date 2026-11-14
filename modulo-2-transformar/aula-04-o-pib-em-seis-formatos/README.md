# Transformar · Aula 4 · O PIB em seis formatos

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwt-04-o-pib-em-seis-formatos

O `pib.py` lê o PIB de cada jeito possível e fica com a leitura que bate com PIB per capita × população. O resto vai para `dados/rejeitados.csv`, com o motivo.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: pib.py, testes/test_pib.py.

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

Comandos da aula, nesta ordem: `uv run python ficha.py`, `uv run python numeros.py`, `uv run python pib.py` e `uv run pytest`. Cada programa lê o que o anterior gravou em `dados/`.
