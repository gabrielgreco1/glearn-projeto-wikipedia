# Projeto Wikipedia (G learn)

Repositório de referência do Projeto 1 do curso G learn: um programa em Python que monta um CSV com os 27 estados do Brasil, a partir da Wikipedia em português. O projeto é construído em sete aulas, e cada aula tem uma pasta aqui.

## Como usar

Você faz o projeto na SUA pasta, `projeto-wikipedia/`, no SEU repositório, seguindo as aulas na plataforma. Este repositório serve para conferir: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar no fim daquela aula. A pasta `final/` é igual à da aula 7.

## As sete aulas

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
| 1 | [Medir o que você coletou antes de mexer](modulo-2-transformar/aula-01-medir-o-que-voce-coletou) | `uv run python perfil.py` e `uv run pytest` |

Em 14 de novembro de 2026, com pandas 3.1.1: a pasta da aula 1 foi rodada numa cópia limpa, depois de `uv run python rodar.py`. O `perfil.py` mostrou 27 linhas, 13 estados sem coordenadas e a densidade diferente da conta nos 27 estados. Os 3 testes passam.

## O que foi rodado

Em 12 de novembro de 2026, com Python 3.13.5, uv 0.10.11, httpx 0.28.1, beautifulsoup4 4.15.0, python-dotenv 1.2.4 e pytest 9.2.0:

- As pastas das aulas 2 a 7 foram rodadas uma a uma, cada uma numa cópia limpa.
- A aula 7 foi rodada do zero (`rm -rf dados` e `uv run python rodar.py`): 55 pedidos, cerca de um minuto, 27 linhas no CSV final. A segunda rodada não fez nenhum pedido.
- Os testes (`uv run pytest`) passam nas aulas 4 a 7: 2 testes. Eles leem `dados/lista.html`, então precisam que a página já tenha sido baixada.

## Regras do projeto

Estão em [PADROES.md](PADROES.md).
