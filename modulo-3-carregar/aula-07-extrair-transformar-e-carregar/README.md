# Carregar · Aula 7 · Extrair, transformar e carregar num comando

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwc-07-extrair-transformar-e-carregar-num-comando

O `rodar.py` faz as três etapas, na ordem. A prova é numa cópia limpa: do zero, e de novo sem mudar nada.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: rodar.py, camadas.py, testes/test_camadas.py, README.md.

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

O `rodar.py` desta pasta faz as três etapas: extrair, transformar e carregar.

Comandos da aula: `uv run python rodar.py` (duas vezes) e `uv run pytest`.
