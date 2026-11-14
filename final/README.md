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
uv run python transformar.py
uv run pytest
```

O `rodar.py` coleta: a primeira rodada faz 55 pedidos e leva cerca de um minuto, e a segunda não faz pedido nenhum. O `transformar.py` só lê o que já está em `dados/` e não faz pedido nenhum.

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

## A transformação

O `transformar.py` roda cinco etapas, na ordem:

| Etapa | Programa | Grava |
|---|---|---|
| Ler a ficha de cada estado nas páginas guardadas | `ficha.py` | `dados/fichas.csv`, o texto como está na página |
| Texto em número | `numeros.py` | `dados/numeros.csv` |
| O PIB em reais, conferido com per capita × população | `pib.py` | `dados/pib.csv` e `dados/rejeitados.csv` |
| Validar as regras e gravar as camadas | `validar.py`, `camadas.py` | `dados/bronze/inventario.csv`, `dados/silver/estados.parquet` |
| Perguntas em SQL | `consultar.py` | `dados/gold/regioes.parquet` |

## Camadas

- **Bronze**: o que veio do site, sem nenhuma mudança: `lista.html`, `estados/` e `resumos/`. O `inventario.csv` guarda o sha256 de cada arquivo.
- **Silver**: a tabela limpa e validada, uma linha por estado, com o arquivo de origem, a revisão da página na Wikipedia e o sha256 da ficha.
- **Gold**: a resposta das perguntas, por região.

## O que a rodada de 14 de novembro de 2026 mostrou

- A coluna `densidade` da tabela não bate com `populacao / area_km2`: a população é do Censo 2022 e a densidade, de 2005. A transformação não usa essa coluna.
- O PIB aparece em seis formatos nas fichas. Em 23 estados ele bateu com o PIB per capita × população. Em 4 foi para `rejeitados.csv`, com o motivo: MA, PE, RJ e SP.
- O PIB per capita de PE está escrito `27,139`, mil vezes menor que o real. Foi rejeitado pela regra de faixa.
- Latitude e longitude estão vazias em 13 estados. Ficaram vazias: nada foi inventado.
- O DF não tem municípios, e a regra aceita o vazio.

## O que este projeto ainda não tem

- Histórico de coletas: cada rodada sobrescreve a tabela.
- Agendamento: ele roda quando você manda.
