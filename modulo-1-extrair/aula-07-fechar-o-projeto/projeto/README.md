# Projeto Wikipedia

Um programa em Python que monta um arquivo CSV com os 27 estados do Brasil, a partir da Wikipedia em português.

## O que ele faz

1. Baixa a página [Unidades federativas do Brasil](https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil) e guarda o HTML em `dados/lista.html`.
2. Lê a tabela dos estados nesse HTML e grava `dados/estados.csv`.
3. Baixa a página de cada estado em `dados/estados/`.
4. Pede à API da Wikipedia o resumo de cada estado e guarda em `dados/resumos/`.
5. Junta a tabela e os resumos em `dados/estados_completo.csv` e confere o resultado.

## Como rodar

Você precisa do [uv](https://docs.astral.sh/uv/) instalado.

```
cp .env.example .env
```

Abra o `.env` e troque o contato pelo seu. Depois:

```
uv sync
uv run python rodar.py
uv run pytest
```

A primeira rodada faz 55 pedidos e leva cerca de um minuto. A segunda não faz pedido nenhum: o que já está em `dados/` não é baixado de novo.

## De onde vem o dado

| Arquivo | Origem | Caminho |
|---|---|---|
| `dados/lista.html` | página da Wikipedia, em HTML | pedido HTTP simples (a página é SSR) |
| `dados/estados/*.html` | página de cada estado, em HTML | pedido HTTP simples |
| `dados/resumos/*.json` | API REST da Wikipedia, resumo da página | `/api/rest_v1/page/summary/` |
| `dados/estados_completo.csv` | a tabela (HTML) e o resumo (API) | colunas `origem_tabela` e `origem_resumo` |

O texto da Wikipedia é publicado sob a licença CC BY-SA 4.0.

## Cuidados com o site

- Todo pedido leva um `User-Agent` com o nome do projeto e um contato, como a Wikimedia pede.
- Um pedido por vez, com um segundo de pausa depois de cada um.
- Nada é pedido duas vezes: o arquivo que já existe em disco é reaproveitado.

## O que este projeto ainda não tem

- Camadas de dados (bronze, silver, gold) e histórico de coletas.
- Agendamento: ele roda quando você manda.
- As páginas dos estados ficam guardadas, mas nada é lido delas ainda.
