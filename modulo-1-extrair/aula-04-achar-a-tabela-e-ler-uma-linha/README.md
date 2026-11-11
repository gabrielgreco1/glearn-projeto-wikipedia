# Aula 4: achar a tabela e ler uma linha

## O que você vai ter no fim

- Um programa, `src/tabela.py`, que acha a tabela dos estados no HTML.
- A primeira linha de dados da tabela, com cada célula numerada.

## O que muda em relação à aula anterior

- `projeto/src/tabela.py`: novo. Acha a tabela e mostra uma linha.
- O restante do projeto é igual à aula 3.

## Conceitos desta aula

- **Tabela no HTML**: uma tabela é uma marca `<table>`. Dentro dela, cada linha é um `<tr>` e cada célula é um `<td>`. O cabeçalho usa `<th>`.
- **Classe**: um nome que o site põe em uma marca para estilizar. A tabela dos estados tem as classes `wikitable` e `sortable`. Um seletor pode pedir uma marca com essas classes: `table.wikitable.sortable`.
- **Índice**: a posição de um item numa lista. Python começa a contar do zero. A primeira linha é a de índice `0`.

## O código, bloco por bloco

Achar a tabela:

```python
tabela = pagina.select_one("table.wikitable.sortable")
```

- `table.wikitable.sortable` quer dizer: "uma `table` que tenha as classes `wikitable` e `sortable`".

Pegar as linhas:

```python
linhas = tabela.select("tr")
primeira_linha_de_dados = linhas[1]
```

- `select` (sem `_one`) devolve todas as partes que batem, em uma lista.
- `linhas[0]` é o cabeçalho, com os nomes das colunas. `linhas[1]` é o Acre, a primeira linha de dados.

Ler as células:

```python
for numero_da_celula, celula in enumerate(primeira_linha_de_dados.select("td")):
    print(numero_da_celula, repr(celula.get_text(" ", strip=True)))
```

- `enumerate` numera cada célula, começando em 0.
- `repr` mostra o texto entre aspas. Espaços especiais aparecem como `\xa0`. Esse é o espaço que a Wikipedia usa para separar milhares. Vamos tratar isso na aula 5.

## Como rodar

Esta pasta tem o próprio `baixar.py`. Ele pede a página à Wikipedia e guarda o HTML em `dados/bronze/lista.html`. Rode ele antes das outras etapas desta aula.

Na sua pasta do projeto (`projeto-wikipedia/`), rode:

```bash
cp .env.example .env   # e troque o contato dentro dele
uv sync
uv run python src/baixar.py
uv sync
uv run ruff check .
uv run python src/tabela.py
```

Para rodar o gabarito deste curso, entre antes em `modulo-1-extrair/aula-04-achar-a-tabela-e-ler-uma-linha/projeto/` a partir da raiz deste repositório, e use os mesmos comandos.

Se o `dados/bronze/lista.html` já existe, o `baixar.py` avisa e não pede a página de novo.

## Saída esperada

```
0 ''
1 'Acre'
2 'AC'
3 'Rio Branco'
4 '164\xa0122,2'
5 '830\xa0018'
6 '4,30'
7 '13\xa0622\xa0000'
8 '0,2'
9 '16\xa0953,46'
10 '0,663'
11 '86,9%'
12 '17,0‰'
13 '73,9 anos'
```

A célula 0 está vazia porque é a bandeira, que é uma imagem. E o `ruff check .` mostra `All checks passed!`.

## Guarde no Git

Seu repositório é a pasta `projeto-wikipedia/`, criada na aula 1. Este repositório do curso é a referência: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar ao fim daquela aula.

Na sua pasta do projeto, confira o `git status`, adicione só os arquivos desta aula e envie:

```bash
git status
git add pyproject.toml uv.lock src/tabela.py
git commit -m "Aula 4: achar a tabela dos estados e ler uma linha"
git push
```

Confira a lista do `git status` antes do `git add`. O `.env` e a pasta `dados/` não devem aparecer nela.

## Erros comuns

- `IndexError: list index out of range`: a tabela tem menos linhas do que o esperado. Confira o arquivo `lista.html`.
- Aparece "Não achei a tabela": a página mudou. Abra a página no navegador (aula 1) e veja de novo a classe da tabela.
- Os valores saem com `\xa0`: é normal nesta aula. A aula 5 resolve.

Aula anterior: [Aula 3: tirar um dado, o título](../aula-03-tirar-um-dado-o-titulo/README.md)

Próxima aula: [Aula 5: todas as linhas em CSV](../aula-05-todas-as-linhas-em-csv/README.md)

Aula na plataforma: (link a definir)
