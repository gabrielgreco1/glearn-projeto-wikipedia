# Orquestrar · Aula 7 · Os testes no GitHub e a prova final

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwo-07-os-testes-no-github-e-a

Os testes rodam no GitHub a cada push, sem o .env e sem dados/. A prova final é numa cópia limpa, com uma queda no meio e a mesma impressão digital.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: .github/workflows/testes.yml, baixar.py, testes/test_baixar.py, testes/test_ler.py, testes/amostra_lista.html, README.md.

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
```

Num terminal só dele, deixe o servidor do Prefect ligado: `uv run prefect server start`. Uma vez na sua máquina: `uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api`. O painel fica em http://127.0.0.1:4200.

Comandos da aula: `uv run pytest` (sem o `.env` e sem `dados/`), `git push`, e a prova numa cópia limpa com `uv run python fluxo.py`.
