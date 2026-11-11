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

Se o `dados/bronze/lista.html` não está na pasta, copie da aula 2:

```bash
cd modulo-1-extrair/aula-05-todas-as-linhas-em-csv/projeto
mkdir -p dados/bronze
cp ../../aula-02-baixar-a-pagina-com-python/projeto/dados/bronze/lista.html dados/bronze/
```

Depois rode:

```bash
uv sync
uv run ruff check .
uv run python src/tabela.py
uv run pytest
```

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
3 passed in 0.43s
```

As primeiras linhas do CSV:

```
sigla,estado,capital,area_km2,populacao,pagina
AC,Acre,Rio Branco,164122.2,830018,Acre
AL,Alagoas,Maceió,27767.7,3127683,Alagoas
```

## Guarde no Git

```bash
git status
git add modulo-1-extrair/aula-05-todas-as-linhas-em-csv/README.md modulo-1-extrair/aula-05-todas-as-linhas-em-csv/projeto/pyproject.toml modulo-1-extrair/aula-05-todas-as-linhas-em-csv/projeto/uv.lock modulo-1-extrair/aula-05-todas-as-linhas-em-csv/projeto/src/tabela.py modulo-1-extrair/aula-05-todas-as-linhas-em-csv/projeto/testes/test_tabela.py modulo-1-extrair/aula-05-todas-as-linhas-em-csv/projeto/testes/amostras/lista-3-estados.html
git commit -m "Aula 5: todas as linhas da tabela em CSV, com testes"
git push
```

Confira o `git status` antes do `git add`. O `dados/` não entra, por causa do `.gitignore`.

## Erros comuns

- `AssertionError` no pytest: a função `numero` ou a leitura mudou. Compare o seu `tabela.py` com o desta aula.
- `ModuleNotFoundError: tabela`: rode o pytest pelo `uv run pytest` dentro da pasta `projeto/`.
- O CSV tem menos de 27 linhas: confira o `lista.html` copiado.

Aula na plataforma: (link a definir)
