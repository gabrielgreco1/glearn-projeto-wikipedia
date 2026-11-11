# Aula 5: todas as linhas em CSV

## O que você vai ter no fim

- Um programa, `src/tabela.py`, que lê as 27 linhas da tabela, converte os números e grava um arquivo CSV.
- O arquivo `dados/silver/estados.csv`, com uma linha por estado.
- Um teste, em `testes/test_tabela.py`, que confere a leitura.

## O que muda em relação à aula anterior

- `projeto/src/tabela.py`: alterado. Agora lê todas as linhas, tem a função `numero` e grava o CSV.
- `projeto/testes/test_tabela.py`: novo. Testes com pytest.
- `projeto/testes/amostras/lista-3-estados.html`: novo. Um pedaço real da página, com três estados, só para o teste. Ele é o único dado de exemplo que vai para o Git.
- `projeto/pyproject.toml`: alterado. Entrou o `pytest`, que roda os testes.

## Conceitos desta aula

- **CSV**: um arquivo de texto em que cada linha é um registro e as colunas são separadas por vírgula. Planilhas abrem CSV.
- **Conversão de número**: a Wikipedia escreve `164 122,2` (com espaço para milhares e vírgula para decimal). O Python precisa de `164122.2`. A função `numero` faz essa troca.
- **Teste**: um código que confere se outro código faz a conta certa. Com ele, você mexe no programa com segurança.
- **Nota de rodapé**: a Wikipedia põe números como `[1]` no texto. A função `texto` tira essas notas.

## O código, bloco por bloco

Converter número:

```python
def numero(valor: str) -> float | None:
    limpo = valor.replace("\xa0", "").replace(" ", "").replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return None
```

- Primeiro tira os espaços (comuns e os especiais `\xa0`).
- Depois tira o ponto de milhar e troca a vírgula por ponto, que o Python entende.
- `float` converte o texto em número. Se não der, `try` e `except` devolvem `None`, que quer dizer "sem valor".

Ler todas as linhas:

```python
for linha in tabela.select("tr"):
    celulas = linha.select("td")
    if len(celulas) < 6:
        continue  # cabeçalho ou linha de total
```

- `continue` pula a linha. O cabeçalho usa `<th>` e não tem seis células de dados, então sai da conta.

Gravar o CSV:

```python
with SAIDA.open("w", newline="", encoding="utf-8") as arquivo:
    escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
    escritor.writeheader()
    escritor.writerows(estados)
```

- `with` abre o arquivo e fecha no fim, mesmo se der erro.
- `"w"` apaga o que estava e escreve de novo. Por isso rodar duas vezes não duplica nada.
- `DictWriter` escreve cada dicionário como uma linha, na ordem de `COLUNAS`.

Testes:

```python
def test_numero_com_espaco_e_virgula():
    assert numero("164\xa0122,2") == 164122.2
```

- Cada função que começa com `test_` é um teste.
- `assert` confere uma afirmação. Se for falsa, o teste falha.

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
uv run pytest
```

Para rodar o gabarito deste curso, entre antes em `modulo-1-extrair/aula-05-todas-as-linhas-em-csv/projeto/` a partir da raiz deste repositório, e use os mesmos comandos.

Se o `dados/bronze/lista.html` já existe, o `baixar.py` avisa e não pede a página de novo.

## Saída esperada

```
27 estados gravados em .../projeto/dados/silver/estados.csv
```

O `ruff check .` mostra:

```
All checks passed!
```

O `pytest` mostra:

```
testes/test_tabela.py ...                                                [100%]
3 passed in 0.13s
```

As primeiras linhas do CSV:

```
sigla,estado,capital,area_km2,populacao,pagina
AC,Acre,Rio Branco,164122.2,830018,Acre
AL,Alagoas,Maceió,27767.7,3127683,Alagoas
```

## Guarde no Git

Seu repositório é a pasta `projeto-wikipedia/`, criada na aula 1. Este repositório do curso é a referência: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar ao fim daquela aula.

Na sua pasta do projeto, confira o `git status`, adicione só os arquivos desta aula e envie:

```bash
git status
git add pyproject.toml uv.lock src/tabela.py testes/test_tabela.py testes/amostras/lista-3-estados.html
git commit -m "Aula 5: todas as linhas da tabela em CSV, com testes"
git push
```

Confira a lista do `git status` antes do `git add`. O `.env` e a pasta `dados/` não devem aparecer nela.

## Erros comuns

- `AssertionError` no pytest: a função `numero` ou a leitura mudou. Compare o seu `tabela.py` com o desta aula.
- `ModuleNotFoundError: tabela`: rode o pytest pelo `uv run pytest` dentro da pasta `projeto/`.
- O CSV tem menos de 27 linhas: apague `dados/bronze/lista.html`, rode `uv run python src/baixar.py` e tente de novo.

Aula anterior: [Aula 4: achar a tabela e ler uma linha](../aula-04-achar-a-tabela-e-ler-uma-linha/README.md)

Próxima aula: [Aula 6: o mesmo dado pela API](../aula-06-o-mesmo-dado-pela-api/README.md)

Aula na plataforma: https://learn.gabrielgreco.com/trilha/pw-05-todas-as-linhas-em-csv
