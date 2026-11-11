# Projeto 1 do G learn: extrair dados da Wikipedia

Este repositório é o Projeto 1 do curso G learn de engenharia de dados. Você aprende a tirar dados de uma página da Wikipedia em português. No fim, tem um projeto que baixa a tabela dos 27 estados do Brasil e o resumo de cada estado, e grava tudo em arquivos.

Você não precisa saber programar para começar. A primeira aula é só no navegador.

## Como usar

1. Faça as aulas em ordem, da aula 1 à 7.
2. Em cada aula, leia o `README.md` da pasta e siga os passos.
3. Você trabalha na sua pasta `projeto-wikipedia/`, criada na aula 1. Ela é o seu repositório no Git.
4. Um commit e um push por aula. Os comandos estão no fim de cada README.
5. Este repositório é a referência: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar ao fim daquela aula.

## Aulas

| Aula | Pasta | O que você faz |
|---|---|---|
| 1 | `modulo-1-extrair/aula-01-ver-o-html-no-navegador/` | Vê o código da página no navegador, sem Python |
| 2 | `modulo-1-extrair/aula-02-baixar-a-pagina-com-python/` | Baixa a página e guarda o arquivo |
| 3 | `modulo-1-extrair/aula-03-tirar-um-dado-o-titulo/` | Tira o título da página com um seletor |
| 4 | `modulo-1-extrair/aula-04-achar-a-tabela-e-ler-uma-linha/` | Acha a tabela dos estados e lê uma linha |
| 5 | `modulo-1-extrair/aula-05-todas-as-linhas-em-csv/` | Lê as 27 linhas e grava um CSV, com testes |
| 6 | `modulo-1-extrair/aula-06-o-mesmo-dado-pela-api/` | Pega o resumo de um estado pela API e compara com a tabela |
| 7 | `modulo-1-extrair/aula-07-os-27-estados/` | Junta tudo: 27 estados, pausa, origem e testes |

O projeto pronto, com as mesmas etapas da aula 7, fica em `final/`.

## Para ler antes de começar

- [`PADROES.md`](PADROES.md): as regras de código e de Git usadas em todas as aulas.

## Requisitos

Confira cada item no terminal antes da aula 2.

- Um navegador (Chrome, Edge ou Firefox), para a aula 1.
- Git, para salvar o seu trabalho a partir da aula 1. Confira com `git --version`. Deve aparecer `git version` seguido de um número.
- Python 3.12, a partir da aula 2. Confira com `python3.12 --version`. Se não aparecer, não precisa instalar à mão: o `uv` instala o Python 3.12 quando você roda `uv sync`.
- `uv`, a partir da aula 2. Confira com `uv --version`. Se não aparecer, instale pelo site oficial do `uv`.
- Uma conta no GitHub, para guardar o seu repositório.

## Auditoria (2026-11-11)

Cada pasta foi copiada para uma pasta vazia, instalada com `uv sync` e rodada do zero contra a Wikipedia real, com os comandos do README dela. Pausa de um pedido por segundo, User-Agent com contato.

| Pasta | O que foi rodado | Resultado |
|---|---|---|
| aula 1 | sem código (só navegador) | conferida nos prints da aula na plataforma |
| aula 2 | `ruff check .`, `baixar.py` duas vezes | status 200, 413130 bytes gravados; na segunda vez não baixa de novo |
| aula 3 | `baixar.py`, `ruff check .`, `titulo.py` | `título: Unidades federativas do Brasil` |
| aula 4 | `baixar.py`, `ruff check .`, `tabela.py` | as 14 células do Acre, iguais às do README |
| aula 5 | `baixar.py`, `ruff check .`, `tabela.py`, `pytest` | 27 estados no CSV (28 linhas com o cabeçalho), 6 colunas, 3 testes passam |
| aula 6 | `baixar.py`, `api.py` duas vezes, `ruff check .`, `pytest` | 1 pedido à API na primeira vez e nenhum na segunda; Acre sem coordenadas; 3 testes passam |
| aula 7 | `coletar.py` duas vezes, `extrair.py`, `pytest`, `ruff check .` | 28 pedidos na primeira vez e nenhum na segunda; 56 arquivos em bronze; CSV com 27 estados e 9 colunas; 3 testes passam |
| `final/` | os mesmos comandos da aula 7 | o mesmo resultado; `final/` é idêntica à pasta da aula 7 (`diff -r` sem diferença) |

Entre uma aula e a seguinte, a diferença das pastas `projeto/` é só o que a aula seguinte ensina (conferido com `diff -r`).

### Testes de auditoria, sem rede

A pasta `auditoria/` tem 31 testes que carregam o código de cada aula e de `final/` e trocam a rede por respostas de mentira. Eles não fazem pedido a site nenhum. Para rodar, na raiz do repositório:

```bash
uv run --project final pytest auditoria
```

O que eles cobrem:

- status 403, 404, 429 e 500: o programa não grava nada e avisa (aulas 2 a 6) ou para com erro (API e aula 7);
- rede fora do ar: o erro aparece, nada é gravado;
- rodar duas vezes: nenhum pedido novo, nenhum arquivo duplicado, CSV idêntico;
- retomada: depois de uma falha no meio, só o que falta é pedido;
- `User-Agent` vindo do `.env` e `timeout=30` em todo pedido; pausa depois de cada pedido;
- tabela sem linhas, célula vazia, linha de total, nota de rodapé, link absoluto e relativo, nomes com acento e parênteses;
- arquivo de origem com endereço, status, tamanho e `sha256` corretos.

Não testado: comportamento do site sob bloqueio real (não se provoca erro em site dos outros) e outros sistemas além do macOS.
