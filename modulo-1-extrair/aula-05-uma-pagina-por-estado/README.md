# Aula 5 · Uma página por estado, sem sobrecarregar o site

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pw-05-uma-pagina-por-estado-sem-sobrecarregar

27 pedidos, um de cada vez, com pausa, registro, retomada e tratamento de erro.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: baixar.py, paginas.py.

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

Comando da aula: `uv run python paginas.py`
