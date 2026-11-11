# Aula 6: o mesmo dado pela API

## O que você vai ter no fim

- Um programa, `src/api.py`, que pede o resumo do Acre à API oficial da Wikipedia.
- O JSON da resposta salvo em `dados/bronze/resumo-AC.json`, como veio.
- Uma comparação com a linha do Acre que estava na tabela HTML.
- Uma resposta para a pergunta: por que pedir pela API antes de raspar o HTML?

## O que muda em relação à aula anterior

- `projeto/src/api.py`: novo.
- `projeto/src/tabela.py`: igual à aula 5. O `api.py` usa a função `ler_estados` dele.
- `projeto/testes/` e o `pyproject.toml`: as mesmas bibliotecas da aula 5.

## Dois caminhos para o mesmo dado

| | HTML da página (aulas 2 a 5) | API oficial (esta aula) |
|---|---|---|
| O que é | o código inteiro da página | um serviço que devolve só o resumo, em JSON |
| Como achar o dado | seletor no HTML, que pode mudar | campo com nome fixo, como `description` |
| Tamanho | 413 mil bytes por página | 3 mil bytes por estado |
| Dados do Acre | área, população, capital, sigla | descrição curta e coordenadas (quando existem) |

**Por que a API vem antes de raspar**: a API foi feita para ser lida por programas. Os campos têm nome fixo e o formato é JSON, que o Python lê com facilidade. Raspar a página é colher dado do que foi feito para ser visto. Se a página mudar o visual, o seletor quebra. Por isso, quando existe API, use a API. Raspar é o plano B.

## Conceitos desta aula

- **API**: um endereço que devolve dados para programas. Ela responde em JSON.
- **JSON**: um texto com chaves e valores, como `{"description": "..."}`. O Python lê com `json.loads`.
- **Coordenadas**: latitude e longitude, o ponto do estado no mapa.
- **Não ter dado não é erro**: a API pode não ter o campo. Por isso o programa confere `None` antes de usar.

## O código, bloco por bloco

Pedido à API:

```python
url = "https://pt.wikipedia.org/api/rest_v1/page/summary/" + quote(PAGINA, safe="")
resposta = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
```

- O endereço termina com o nome do estado: `.../summary/Acre`.
- `quote` troca espaços e acentos por texto seguro para o endereço.

Guardar sem mexer, e não baixar de novo:

```python
if ARQUIVO_API.exists():
    print("resumo já está em bronze, não baixo de novo")
    return ARQUIVO_API.read_bytes()
...
ARQUIVO_API.write_bytes(resposta.content)
```

- Se o arquivo já existe, o programa usa o que está no disco.
- Se não existe, grava os bytes da resposta antes de ler o conteúdo.

Ler o JSON e conferir as coordenadas:

```python
resumo = json.loads(pegar_resumo().decode("utf-8"))
coordenadas = resumo.get("coordinates")
if coordenadas is None:
    print("coordenadas: a API não devolveu para este estado")
```

- `json.loads` transforma o texto em um dicionário do Python.
- `resumo.get("coordinates")` pega o campo. Se ele não existe, devolve `None`, sem dar erro.

Comparar com a tabela:

```python
estados = ler_estados(ARQUIVO_HTML.read_text(encoding="utf-8"))
acre = next(estado for estado in estados if estado["sigla"] == "AC")
```

- `ler_estados` é a função da aula 5. Ela devolve a lista dos 27 estados.
- `next` pega o primeiro estado cuja sigla é `AC`.

## Como rodar

Esta pasta tem o próprio `baixar.py`. Rode ele primeiro, para ter o `dados/bronze/lista.html` nesta pasta:

Na sua pasta do projeto (`projeto-wikipedia/`), rode:

```bash
cp .env.example .env   # e troque o contato dentro dele
uv sync
uv run python src/baixar.py
uv run python src/api.py
uv run python src/api.py
uv run ruff check .
uv run pytest
```

Para rodar o gabarito deste curso, entre antes em `modulo-1-extrair/aula-06-o-mesmo-dado-pela-api/projeto/` a partir da raiz deste repositório, e use os mesmos comandos.

Rode `api.py` duas vezes para ver a diferença. A primeira pede o resumo à API. A segunda usa o arquivo que ficou em `dados/bronze/`.

## Saída esperada

Primeira execução (pede à API, 1 requisição):

```
status: 200
descrição: unidade federativa do Brasil
coordenadas: a API não devolveu para este estado
na tabela (HTML): Acre | Rio Branco | 164122.2
```

Segunda execução (usa o arquivo que já está em bronze, 0 requisições):

```
resumo já está em bronze, não baixo de novo
descrição: unidade federativa do Brasil
coordenadas: a API não devolveu para este estado
na tabela (HTML): Acre | Rio Branco | 164122.2
```

O `ruff check .` mostra `All checks passed!`. O pytest mostra `3 passed`.

**Fato que vale ver**: a API não devolve coordenadas para o Acre nem para Alagoas. Para São Paulo, ela devolve (`lat -21.82972`, `lon -49.2075`). Não é erro do seu código: é o que a Wikipedia tem. Esse é o motivo de conferir `None`.

## Guarde no Git

Seu repositório é a pasta `projeto-wikipedia/`, criada na aula 1. Este repositório do curso é a referência: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar ao fim daquela aula.

Na sua pasta do projeto, confira o `git status`, adicione só os arquivos desta aula e envie:

```bash
git status
git add pyproject.toml uv.lock src/api.py
git commit -m "Aula 6: resumo de um estado pela API, comparado com a tabela"
git push
```

Confira a lista do `git status` antes do `git add`. O `.env` e a pasta `dados/` não devem aparecer nela.

## Erros comuns

- `status: 404`: o nome da página mudou. Confira o nome do estado no navegador.
- `status: 429` ou outro erro: o site está limitando. Espere alguns minutos e não insista.
- `ValueError` ou `StopIteration` ao buscar o Acre: o `lista.html` não é o certo. Apague `dados/bronze/lista.html` e rode `uv run python src/baixar.py` de novo.

Aula anterior: [Aula 5: todas as linhas em CSV](../aula-05-todas-as-linhas-em-csv/README.md)

Próxima aula: [Aula 7: os 27 estados](../aula-07-os-27-estados/README.md)

Aula na plataforma: https://learn.gabrielgreco.com/trilha/pw-06-o-mesmo-dado-pela-api-oficial
