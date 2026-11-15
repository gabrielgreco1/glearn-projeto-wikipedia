# Projeto Wikipedia (G learn)

Repositório de referência do Projeto 1 do curso G learn: um programa em Python que monta uma tabela com os 27 estados do Brasil, a partir da Wikipedia em português, carrega o resultado num banco Postgres e roda sozinho todo dia, orquestrado pelo Prefect. O projeto é construído em quatro etapas de sete aulas cada, extrair, transformar, carregar e orquestrar, e cada aula tem uma pasta aqui.

## Como usar

Você faz o projeto na SUA pasta, `projeto-wikipedia/`, no SEU repositório, seguindo as aulas na plataforma. Este repositório serve para conferir: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar no fim daquela aula. A pasta `final/` é igual à da aula 7 da orquestração.

## Etapa 1: extrair

| Aula | Pasta | O que roda |
|---|---|---|
| 1 | [Reconhecer a página antes de programar](modulo-1-extrair/aula-01-reconhecer-a-pagina) | Nada para rodar. Só o `README.md` com o plano. |
| 2 | [O primeiro pedido em Python](modulo-1-extrair/aula-02-o-primeiro-pedido-em-python) | `uv run python baixar.py` |
| 3 | [Do HTML ao dado: ler a tabela](modulo-1-extrair/aula-03-do-html-ao-dado) | `uv run python ler.py` |
| 4 | [A tabela inteira em um CSV](modulo-1-extrair/aula-04-a-tabela-inteira-em-csv) | `uv run python ler.py` e `uv run pytest` |
| 5 | [Uma página por estado, sem sobrecarregar o site](modulo-1-extrair/aula-05-uma-pagina-por-estado) | `uv run python paginas.py` |
| 6 | [Quando o site oferece uma API](modulo-1-extrair/aula-06-quando-o-site-oferece-uma-api) | `uv run python resumos.py` e `uv run python juntar.py` |
| 7 | [Fechar o projeto: rodar do zero e documentar](modulo-1-extrair/aula-07-fechar-o-projeto) | `uv run python rodar.py` e `uv run pytest` |

## Etapa 2: transformar

A segunda etapa parte do CSV final da extração. As pastas ficam em `modulo-2-transformar/`.

| Aula | Pasta | O que roda |
|---|---|---|
| 1 | [Medir o que você coletou](modulo-2-transformar/aula-01-medir-o-que-voce-coletou) | `uv run python perfil.py` |
| 2 | [Ler a ficha de cada estado](modulo-2-transformar/aula-02-ler-a-ficha-de-cada-estado) | `uv run python ficha.py` |
| 3 | [Do texto ao número](modulo-2-transformar/aula-03-do-texto-ao-numero) | `uv run python numeros.py` |
| 4 | [O PIB em seis formatos](modulo-2-transformar/aula-04-o-pib-em-seis-formatos) | `uv run python pib.py` |
| 5 | [Validar a tabela](modulo-2-transformar/aula-05-validar-a-tabela) | `uv run python validar.py` |
| 6 | [Camadas e origem](modulo-2-transformar/aula-06-camadas-e-origem) | `uv run python camadas.py` |
| 7 | [Perguntar em SQL e fechar](modulo-2-transformar/aula-07-perguntar-em-sql-e-fechar) | `uv run python transformar.py` |

Cada programa lê o que o anterior gravou em `dados/`, então numa pasta limpa os comandos rodam na ordem das aulas: `rodar.py`, `ficha.py`, `numeros.py`, `pib.py`, `validar.py`, `camadas.py` e `consultar.py` (ou só `transformar.py`, na aula 7).

Em 14 de novembro de 2026, cada pasta da transformação foi copiada para uma pasta limpa e rodada do zero: `rodar.py` (55 pedidos) e depois os comandos da aula. Os testes passam em todas: 3, 5, 11, 17, 20, 21 e 21. Em 14 de novembro de 2026, à tarde, a validação da aula 5 passou a usar a forma de classe do pandera (`DataFrameModel`), a mesma da aula T02-01 do curso; as pastas 5, 6, 7 e `final/` foram rodadas de novo, com os mesmos números.

## Etapa 3: carregar

A terceira etapa leva a silver e a gold para um Postgres que roda no Docker, na sua máquina. As pastas ficam em `modulo-3-carregar/`. Antes dos comandos de cada aula: `docker compose up -d --wait`.

| Aula | Pasta | O que roda |
|---|---|---|
| 1 | [Um Postgres para o projeto](modulo-3-carregar/aula-01-um-postgres-para-o-projeto) | `uv run python banco.py` |
| 2 | [A tabela de destino: tipos e regras](modulo-3-carregar/aula-02-a-tabela-de-destino) | `uv run python banco.py` |
| 3 | [A primeira carga, com COPY](modulo-3-carregar/aula-03-a-primeira-carga-com-copy) | `uv run python carregar.py` |
| 4 | [Carregar de novo sem duplicar](modulo-3-carregar/aula-04-carregar-de-novo-sem-duplicar) | `uv run python carregar.py` |
| 5 | [A conta de cada carga](modulo-3-carregar/aula-05-a-conta-de-cada-carga) | `uv run python carregar.py` |
| 6 | [A gold no banco, trocada inteira](modulo-3-carregar/aula-06-a-gold-no-banco) | `uv run python carregar.py` |
| 7 | [Extrair, transformar e carregar num comando](modulo-3-carregar/aula-07-extrair-transformar-e-carregar) | `uv run python rodar.py` |

Em 15 de novembro de 2026, com Docker 29.5.2, postgres:18 (18.7) e psycopg 3.3.9, cada pasta da carga foi copiada para uma pasta limpa, com o banco zerado e o mesmo `dados/` (a coleta das 4h03 desse dia), e rodada com `transformar.py` e os comandos da aula. Os testes passam em todas: 21, 21, 23, 25, 26, 27 e 28; nenhum deles precisa do banco. A pasta `final/` foi rodada do zero numa pasta nova, contra a Wikipedia ao vivo: a primeira rodada do `rodar.py` fez os 55 pedidos e inseriu 27 estados (cerca de 1min15s); a segunda não fez pedido nenhum e deixou as 27 linhas iguais.

## Etapa 4: orquestrar

A quarta etapa põe o projeto num orquestrador, o Prefect, que roda na sua máquina, de graça. As pastas ficam em `modulo-4-orquestrar/`. Antes dos comandos de cada aula: `docker compose up -d --wait` e, num terminal só dele, `uv run prefect server start`.

| Aula | Pasta | O que roda |
|---|---|---|
| 1 | [O projeto num orquestrador](modulo-4-orquestrar/aula-01-o-projeto-num-orquestrador) | `uv run python fluxo.py` |
| 2 | [Uma task por etapa e novas tentativas](modulo-4-orquestrar/aula-02-uma-task-por-etapa) | `uv run python fluxo.py` |
| 3 | [O aviso de falha e o runbook](modulo-4-orquestrar/aula-03-o-aviso-de-falha) | `uv run python fluxo.py` |
| 4 | [A coleta do dia e a retomada](modulo-4-orquestrar/aula-04-a-coleta-do-dia-e-a-retomada) | `uv run python fluxo.py` |
| 5 | [Auditar antes de publicar](modulo-4-orquestrar/aula-05-auditar-antes-de-publicar) | `uv run python fluxo.py` |
| 6 | [Todo dia às 6h, no horário de Brasília](modulo-4-orquestrar/aula-06-todo-dia-as-6h) | `uv run python fluxo.py agendar` |
| 7 | [Os testes no GitHub e a prova final](modulo-4-orquestrar/aula-07-os-testes-no-github-e-a-prova-final) | `uv run pytest` e `uv run python fluxo.py` |

Em 15 de novembro de 2026, com Prefect 3.9.3, Docker 29.5.2, postgres:18 (18.7) e Python 3.13.5, as sete aulas foram feitas em ordem numa pasta de aluno que vinha do fim da carga, contra a Wikipedia ao vivo, com as falhas de cada aula provocadas de verdade (rede desligada por um proxy que não existe, banco desligado, Ctrl+C no meio da coleta, a lista estragada de propósito). Os testes passam em todas: 28, 29, 29, 31, 31, 31 e 32. A agenda das 6h foi conferida com um cron de dois em dois minutos, numa cópia: a execução marcada rodou sozinha. Os testes da aula 7 rodaram no GitHub Actions, numa branch deste repositório com a pasta do projeto na raiz (`prova-ci-orquestracao`): vermelho sem o `.env`, vermelho sem `dados/`, verde com os dois consertos. A pasta `final/` foi clonada para uma pasta nova, com um banco vazio: a coleta interrompida com Ctrl+C continuou de onde parou, inseriu os 27 estados e deu a mesma impressão digital da pasta do aluno, `8fe1eb3a6701bcc3`.

## O que foi rodado

Em 12 de novembro de 2026, com Python 3.13.5, uv 0.10.11, httpx 0.28.1, beautifulsoup4 4.15.0, python-dotenv 1.2.4 e pytest 9.2.0:

- As pastas das aulas 2 a 7 foram rodadas uma a uma, cada uma numa cópia limpa.
- A aula 7 foi rodada do zero (`rm -rf dados` e `uv run python rodar.py`): 55 pedidos, cerca de um minuto, 27 linhas no CSV final. A segunda rodada não fez nenhum pedido.
- Os testes (`uv run pytest`) passam nas aulas 4 a 7: 2 testes. Eles leem `dados/lista.html`, então precisam que a página já tenha sido baixada.

## Regras do projeto

Estão em [PADROES.md](PADROES.md).
