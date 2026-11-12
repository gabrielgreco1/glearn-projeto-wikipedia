# Aula 7 · Fechar o projeto: rodar do zero e documentar

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pw-07-fechar-o-projeto-rodar-do-zero

Um comando roda tudo, um programa confere o resultado e o README conta como usar.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: rodar.py, conferir.py, README.md.

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

Comando da aula: `uv run python rodar.py` e `uv run pytest`
