# Aula 6 · Quando o site oferece uma API

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pw-06-quando-o-site-oferece-uma-api

O resumo de cada estado pela API da Wikipedia, e os dois caminhos juntos num CSV com a origem de cada parte.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: resumos.py, juntar.py.

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

Comando da aula: `uv run python resumos.py` e `uv run python juntar.py`
