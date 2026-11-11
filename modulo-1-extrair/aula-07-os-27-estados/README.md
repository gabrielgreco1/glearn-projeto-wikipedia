# Aula 7: os 27 estados

## O que você vai ter no fim

- O projeto completo, igual ao da pasta `final/` do repositório.
- Um CSV, `dados/silver/estados.csv`, com os 27 estados, a descrição de cada um e as coordenadas quando a API tem.
- Uma pasta de bronze por dia, com cada resposta guardada como veio e um arquivo de origem ao lado.
- Testes que conferem a leitura da tabela.

## O que muda em relação à aula anterior

- `src/comum.py`: novo. Configuração, pedido ao site com pausa, gravação em bronze.
- `src/coletar.py`: novo. Baixa a lista e os 27 resumos, sem baixar de novo o que já existe.
- `src/extrair.py`: novo. Lê o bronze e grava o CSV final.
- `testes/`: os testes da leitura da tabela.
- `.env.example`: agora tem a pausa (`WIKI_PAUSA`) além do contato.
- `pyproject.toml`: as mesmas bibliotecas da aula 5, com a versão travada.
- O `src/baixar.py` e o `src/tabela.py` das aulas anteriores não fazem parte deste projeto. Você troca pelo código desta aula.

## Conceitos desta aula

- **Pausa**: um tempo de espera entre um pedido e o próximo. Com `WIKI_PAUSA=1`, o programa faz no máximo um pedido por segundo.
- **Não baixar de novo**: antes de pedir, o programa confere se o arquivo já está na pasta do dia. Rodar duas vezes não pede nada que já existe.
- **Bronze, silver**: bronze é a resposta crua, que nunca muda. Silver é o dado limpo, em CSV.
- **Arquivo de origem**: um `.origem.json` ao lado de cada arquivo, com o endereço, o horário, o tamanho e o `sha256` (uma impressão digital do conteúdo).
- **logging**: a forma de registrar mensagens com data e nível, no lugar do `print`.

## O código, bloco por bloco

Configuração (`comum.py`):

```python
load_dotenv()
USER_AGENT = os.getenv("WIKI_USER_AGENT", "projeto-de-estudo/0.1 (preencha o .env)")
PAUSA = float(os.getenv("WIKI_PAUSA", "1"))
```

- A configuração vem do `.env`. Nenhum contato fica escrito no código.

Pedido com pausa (`comum.py`):

```python
def pedir(url: str) -> requests.Response:
    resposta = _sessao.get(url, timeout=30)
    time.sleep(PAUSA)
    resposta.raise_for_status()
    return resposta
```

- `_sessao` leva o `User-Agent` em todos os pedidos.
- `time.sleep(PAUSA)` espera antes de seguir. É isso que limita o ritmo.
- `raise_for_status` gera erro se o status não for de sucesso.

Gravar em bronze com origem (`comum.py`):

```python
arquivo.write_bytes(resposta.content)
origem = {"url": resposta.url, "status": resposta.status_code, "sha256": ..., "bytes": ...}
```

- Os bytes são gravados sem mudança.
- Ao lado, o arquivo `.origem.json` diz de onde veio e quando.

Não baixar de novo (`coletar.py`):

```python
if (pasta / nome).exists():
    continue
```

- Se o arquivo do estado já está na pasta do dia, o laço pula para o próximo.

Montar o CSV (`extrair.py`):

```python
coordenadas = resumo.get("coordinates", {})
return {**estado, "descricao": resumo.get("description"), "latitude": coordenadas.get("lat"), ...}
```

- Junta a linha da tabela com o que a API devolveu. Quando a API não tem coordenadas, a coluna fica vazia.

## Como rodar

Na sua pasta do projeto (`projeto-wikipedia/`), rode:

```bash
cp .env.example .env     # e troque o contato dentro dele
uv sync
uv run python src/coletar.py
uv run python src/extrair.py
uv run pytest
uv run ruff check .
```

Para rodar o gabarito deste curso, entre antes em `modulo-1-extrair/aula-07-os-27-estados/projeto/` a partir da raiz deste repositório, e use os mesmos comandos.

Na primeira vez, `coletar.py` faz 28 pedidos (a lista e os 27 estados), com uma pausa de 1 segundo entre eles. Leva cerca de 30 segundos.

Para rodar de novo no mesmo dia, sem pedir nada: `uv run python src/coletar.py` e `uv run python src/extrair.py`.

## Saída esperada

Primeira execução do `coletar.py` (faz 28 pedidos: a lista e os 27 estados):

```
... INFO lista baixada: 413130 bytes
... INFO resumo AC (1 de 27)
... INFO resumo AL (2 de 27)
... INFO resumo AP (3 de 27)
...
... INFO resumo TO (27 de 27)
... INFO resumos novos: 27; já existiam: 0
```

Segunda execução do `coletar.py` (mesmo dia):

```
... INFO lista.html já está em bronze, não baixo de novo
... INFO resumos novos: 0; já existiam: 27
```

Execução do `extrair.py`:

```
... INFO 27 estados gravados em .../dados/silver/estados.csv (bronze: coleta=2026-11-11)
```

O pytest mostra `3 passed`. O `ruff check .` mostra `All checks passed!`.

Primeiras linhas do CSV:

```
sigla,estado,capital,area_km2,populacao,pagina,descricao,latitude,longitude
AC,Acre,Rio Branco,164122.2,830018,Acre,unidade federativa do Brasil,,
AL,Alagoas,Maceió,27767.7,3127683,Alagoas,unidade federativa do Brasil,,
```

As colunas `latitude` e `longitude` ficam vazias para o Acre e para Alagoas, porque a API não devolve esses dados para eles.

## Guarde no Git

Seu repositório é a pasta `projeto-wikipedia/`, criada na aula 1. Este repositório do curso é a referência: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar ao fim daquela aula.

Na sua pasta do projeto, confira o `git status`, adicione só os arquivos desta aula e envie:

```bash
git status
git add README.md pyproject.toml uv.lock .env.example .gitignore .python-version src/comum.py src/coletar.py src/extrair.py testes/test_extrair.py testes/amostras/lista-3-estados.html
git commit -m "Aula 7: os 27 estados, com pausa, origem e testes"
git push
```

Confira a lista do `git status` antes do `git add`. O `.env` e a pasta `dados/` não devem aparecer nela.

## Erros comuns

- `Não há bronze. Rode antes: uv run python src/coletar.py`: você rodou o `extrair.py` antes do `coletar.py`. Rode o `coletar.py` primeiro.
- `Não achei a tabela dos estados. A página mudou?`: a página mudou ou a lista não foi baixada direito. Apague a pasta do dia em `dados/bronze/` e rode de novo.
- Status diferente de 200 no log: o site recusou. Pare e espere. Não insista.
- O `coletar.py` no dia seguinte cria outra pasta de bronze e baixa tudo de novo. Isso é o esperado.

Aula anterior: [Aula 6: o mesmo dado pela API](../aula-06-o-mesmo-dado-pela-api/README.md)

Projeto pronto: [final/](../../final/README.md)

Aula na plataforma: (link a definir)
