# Aula 4 · A tabela inteira em um CSV

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pw-04-a-tabela-inteira-em-um-csv

As 27 linhas, com os números convertidos, gravadas em `dados/estados.csv`, e dois testes.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: ler.py, testes/test_ler.py.

## Como rodar esta pasta

```
cd projeto
cp .env.example .env
```

Abra o `.env` e troque o contato pelo seu (um e-mail ou o endereço do seu repositório). Depois:

```
uv sync
```

As aulas 3 em diante leem `dados/lista.html`. Se a pasta `dados/` ainda não existe, rode antes `uv run python baixar.py`.

Comando da aula: `uv run python ler.py` e `uv run pytest`
