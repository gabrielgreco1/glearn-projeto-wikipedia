# Projeto Wikipedia

Um programa em Python que monta uma tabela com os 27 estados do Brasil, a partir da Wikipedia em português, carrega o resultado num banco Postgres e roda sozinho todo dia, orquestrado pelo [Prefect](https://docs.prefect.io/).

## O que ele faz

1. Baixa a página [Unidades federativas do Brasil](https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil) e guarda o HTML em `dados/lista.html`.
2. Lê a tabela dos estados nesse HTML e grava `dados/estados.csv`.
3. Baixa a página de cada estado em `dados/estados/`.
4. Pede à API da Wikipedia o resumo de cada estado e guarda em `dados/resumos/`.
5. Junta a tabela e os resumos em `dados/estados_completo.csv` e confere o resultado.
6. Transforma o texto das fichas em números limpos e validados (`transformar.py`).
7. Carrega a tabela limpa e a resposta por região no Postgres (`carregar.py`), depois de uma auditoria.
8. Roda tudo isso como um flow do Prefect, todo dia às 6h, com novas tentativas, aviso de falha e retomada (`fluxo.py`).

## Como rodar

Você precisa do [uv](https://docs.astral.sh/uv/) e do [Docker](https://docs.docker.com/get-started/get-docker/) instalados.

```
cp .env.example .env
```

Abra o `.env` e troque o contato pelo seu. Depois:

```
docker compose up -d --wait
uv sync
uv run pytest
```

O `docker compose up` sobe o Postgres do projeto, na porta 5433 da sua máquina. Os testes não precisam do banco, do `.env` nem da pasta `dados/`: é assim que eles rodam no GitHub.

O projeto roda de três jeitos. Os dois primeiros precisam do servidor do Prefect ligado, num terminal só dele: `uv run prefect server start`, com `uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api` feito uma vez.

| Comando | O que faz |
|---|---|
| `uv run python fluxo.py agendar` | fica ligado e roda o projeto todo dia às 6h, no horário de Brasília. Para rodar agora, noutro terminal: `uv run prefect deployment run projeto-wikipedia/todo-dia` |
| `uv run python fluxo.py` | roda uma vez, agora, como um flow do Prefect |
| `uv run python rodar.py` | roda as três etapas sem o Prefect, com o que já estiver em `dados/` |

A primeira rodada de um dia faz 55 pedidos à Wikipedia e leva cerca de um minuto e meio. As seguintes, no mesmo dia, não fazem pedido nenhum e não mudam nenhuma linha do banco. O painel do Prefect fica em http://127.0.0.1:4200.

Para desligar o banco, `docker compose down`. Os dados ficam no volume `banco` e voltam no próximo `up`; `docker compose down -v` apaga o volume também.

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

## A carga

O `carregar.py` leva a silver e a gold para o Postgres, numa transação só:

| Tabela | De onde | Como |
|---|---|---|
| `estados` | `dados/silver/estados.parquet` | COPY para uma tabela temporária e upsert pela `sigla`: a linha nova entra, a que mudou é atualizada, a igual fica como está |
| `regioes` | `dados/gold/regioes.parquet` | trocada inteira a cada carga |
| `cargas` | o próprio `carregar.py` | uma linha por carga: quantas linhas vieram, novas, atualizadas, iguais e a soma da população |

- O `hash_conteudo` de cada estado é o sha256 só dos valores do estado. A origem (`sha256_ficha`, `transformado_em`) muda a cada coleta mesmo com o dado igual, e por isso fica de fora do hash.
- Antes de confirmar, a carga confere o banco contra a silver: o mesmo número de linhas e a mesma soma da população. Se não bate, nada é gravado.
- As tabelas estão em `schema.sql`, que o `banco.py` roda antes de cada carga.

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

## A orquestração

O `fluxo.py` é o projeto como um flow do Prefect. O trabalho continua nos mesmos arquivos de cada etapa; o `fluxo.py` só diz a ordem, as novas tentativas, o horário e o aviso.

| Task | O que chama | Se falhar |
|---|---|---|
| `preparar_coleta` | `coleta.py`: a coleta do dia em `dados/`; a de outro dia vai para `dados_anterior/` | |
| `baixar_lista` | `baixar.py`, a página com a tabela | mais 3 tentativas, 10 s entre elas |
| `tabela_em_csv` | `ler.py` | |
| `paginas` | `paginas.py`, uma página por estado | mais 3 tentativas; o que já foi baixado não é pedido de novo |
| `resumos` | `resumos.py`, a API de resumos | mais 3 tentativas, como a `paginas` |
| `juntar_e_conferir` | `juntar.py` e `conferir.py` | |
| `transformar` | `transformar.py` | |
| `carregar` | `carregar.py`: grava, audita e só então publica | a auditoria barra, e nada é publicado |

- **Retomada.** A coleta de hoje interrompida no meio (Ctrl+C, a máquina desligou, a rede caiu) continua de onde parou na próxima execução. Cada arquivo é gravado inteiro, de uma vez (`.parcial` e depois o nome certo).
- **Auditoria antes de publicar.** A silver vai para uma tabela temporária; as regras de `REGRAS`, no `carregar.py`, comparam com o que o banco já publica (população que muda mais de 10%, área que muda mais de 1%). Se uma regra quebra, a carga inteira é desfeita.
- **Impressão digital.** Cada carga grava em `cargas.impressao` o sha256 do que o banco publica. Mesmo resultado, mesma impressão, com ou sem queda no caminho.
- **Aviso.** Uma execução que termina em `Failed` ou `Crashed` deixa uma linha em `avisos.log`. O `runbook.md` diz o que fazer com ela.
- **Testes no GitHub.** `.github/workflows/testes.yml` roda os testes a cada push, numa máquina nova, sem o `.env` e sem o banco.

## O que este projeto ainda não tem

- Histórico dos valores: o banco guarda o valor atual de cada estado e, na tabela `cargas`, o que cada carga mudou, mas não o valor de antes.
- Uma máquina sempre ligada: o agendamento só roda se o computador, o Docker, o servidor do Prefect e o `fluxo.py agendar` estiverem ligados às 6h. Uma execução perdida não é refeita sozinha; a do dia seguinte coleta tudo de novo.
- Aviso que chega até você: o aviso fica em `avisos.log`, na sua máquina.
