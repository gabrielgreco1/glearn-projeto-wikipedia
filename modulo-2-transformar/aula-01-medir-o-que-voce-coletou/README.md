# Transformar · Aula 1 · Medir o que você coletou antes de mexer

Aula na plataforma: https://learn.gabrielgreco.com/learn/trilha/pwt-01-medir-o-que-voce-coletou-antes

O pandas entra no projeto e um programa novo mede o CSV final: tamanho, tipos, células vazias e uma conta de conferência.

A pasta `projeto/` mostra como a sua pasta `projeto-wikipedia/` deve estar no fim desta aula. Arquivos novos ou alterados nesta aula: perfil.py, testes/test_perfil.py, pyproject.toml, uv.lock, README.md.

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

O `rodar.py` cria a pasta `dados/` com o `estados_completo.csv`. Se ela já existe, ele não faz pedido nenhum.

Comando da aula: `uv run python perfil.py` e `uv run pytest`
