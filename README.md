# Projeto Wikipedia (G learn)

Repositório de referência do Projeto 1 do curso G learn: um programa em Python que monta um CSV com os 27 estados do Brasil, a partir da Wikipedia em português. O projeto é construído em duas etapas de sete aulas cada, extrair e transformar, e cada aula tem uma pasta aqui.

## Como usar

Você faz o projeto na SUA pasta, `projeto-wikipedia/`, no SEU repositório, seguindo as aulas na plataforma. Este repositório serve para conferir: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar no fim daquela aula. A pasta `final/` é igual à da aula 7 da transformação.

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

Cada programa lê o que o anterior gravou em `dados/`, então numa pasta limpa os comandos rodam na ordem das aulas: `rodar.py`, `ficha.py`, `numeros.py`, `pib.py`, `validar.py`, `camadas.py` e `consultar.py` (ou só `transformar.py`, na aula 7). A pasta `final/` é igual à da aula 7 da transformação.

Em 14 de novembro de 2026, cada pasta da transformação foi copiada para uma pasta limpa e rodada do zero: `rodar.py` (55 pedidos) e depois os comandos da aula. Os testes passam em todas: 3, 5, 11, 17, 20, 21 e 21. Em 14 de novembro de 2026, à tarde, a validação da aula 5 passou a usar a forma de classe do pandera (`DataFrameModel`), a mesma da aula T02-01 do curso; as pastas 5, 6, 7 e `final/` foram rodadas de novo, com os mesmos números.

## O que foi rodado

Em 12 de novembro de 2026, com Python 3.13.5, uv 0.10.11, httpx 0.28.1, beautifulsoup4 4.15.0, python-dotenv 1.2.4 e pytest 9.2.0:

- As pastas das aulas 2 a 7 foram rodadas uma a uma, cada uma numa cópia limpa.
- A aula 7 foi rodada do zero (`rm -rf dados` e `uv run python rodar.py`): 55 pedidos, cerca de um minuto, 27 linhas no CSV final. A segunda rodada não fez nenhum pedido.
- Os testes (`uv run pytest`) passam nas aulas 4 a 7: 2 testes. Eles leem `dados/lista.html`, então precisam que a página já tenha sido baixada.

## Regras do projeto

Estão em [PADROES.md](PADROES.md).
