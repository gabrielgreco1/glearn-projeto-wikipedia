# Aula 2 · O primeiro pedido em Python

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pw-02-o-primeiro-pedido-em-python

Como o Python pede a página? Do pedido de três linhas, que recebe 403, ao `baixar.py` que se identifica, guarda a página em `dados/` e não pede duas vezes.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: baixar.py, .env.example, .gitignore, pyproject.toml, .python-version, uv.lock.

## Como rodar esta pasta

```
cd projeto
cp .env.example .env
```

Abra o `.env` e troque o contato pelo seu (um e-mail ou o endereço do seu repositório). Depois:

```
uv sync
```

Comando da aula: `uv run python baixar.py`
