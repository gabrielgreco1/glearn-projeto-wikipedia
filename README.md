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
