# Aula 2: baixar a página com Python

## O que você vai ter no fim

- Um programa, `src/baixar.py`, que pede a página da Wikipedia ao site.
- O HTML da página salvo no arquivo `dados/bronze/lista.html`, do jeito que chegou.
- Um arquivo `.env` com o seu contato, que o programa envia ao site.

## O que muda em relação à aula anterior

Esta é a primeira aula com código. Arquivos novos:

- `projeto/pyproject.toml`: lista as bibliotecas usadas e a versão de cada uma.
- `projeto/.python-version`: diz que usamos Python 3.12.
- `projeto/.env.example`: modelo do arquivo de configuração.
- `projeto/.gitignore`: lista o que não vai para o Git.
- `projeto/src/baixar.py`: o programa.
- `projeto/uv.lock`: gerado pelo `uv sync`. Guarda a versão exata de cada biblioteca.

## Conceitos desta aula

- **Requisição**: um pedido que o seu programa faz ao site, como um pedido de página em um restaurante.
- **Status**: o número que o site devolve dizendo como foi o pedido. `200` quer dizer "deu certo". Números como `403` ou `500` querem dizer erro.
- **User-Agent**: um texto que diz quem está pedindo. A Wikipedia pede que todo programa se identifique e deixe um contato. Assim, se o seu programa causar algum problema, o dono do site sabe com quem falar.
- **Resposta crua**: os bytes exatamente como o site mandou. Gravamos a resposta antes de mexer nela. Assim, se algo der errado depois, você volta ao arquivo original sem baixar de novo.

## O código, bloco por bloco

Importações e configuração:

```python
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env desta pasta, se ele existir
```

- `requests` é a biblioteca que faz o pedido ao site.
- `load_dotenv()` lê o arquivo `.env` e põe os valores em memória.

Endereço, arquivo de destino e identificação:

```python
URL = "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"
DESTINO = RAIZ / "dados" / "bronze" / "lista.html"
USER_AGENT = os.getenv("WIKI_USER_AGENT", "projeto-de-estudo/0.1 (preencha o .env)")
```

- `URL` é o endereço da página.
- `DESTINO` é o arquivo onde vamos gravar. `RAIZ` é a pasta `projeto/`.
- `os.getenv` pega o valor `WIKI_USER_AGENT` do `.env`.

O pedido e a conferência do status:

```python
resposta = requests.get(URL, headers={"User-Agent": USER_AGENT}, timeout=30)
print("status:", resposta.status_code)
if resposta.status_code != 200:
    print("Não baixei a página. Veja o status acima.")
    return
```

- `requests.get` faz o pedido. `headers` leva a identificação.
- `timeout=30` diz: se o site não responder em 30 segundos, desista. Assim o programa não trava.
- Se o status não for `200`, o programa para e mostra o número.

Gravação:

```python
DESTINO.parent.mkdir(parents=True, exist_ok=True)
DESTINO.write_bytes(resposta.content)  # os bytes como vieram, sem mexer
```

- `mkdir` cria as pastas que faltam. `exist_ok=True` quer dizer: se já existem, tudo bem.
- `write_bytes` grava os bytes sem transformar em texto. Nada é mudado.

## Como rodar

Antes da primeira vez, copie o modelo de configuração e troque o contato pelo seu:

Na sua pasta do projeto (`projeto-wikipedia/`), rode:

```bash
cp .env.example .env
```

Para rodar o gabarito deste curso, entre antes em `modulo-1-extrair/aula-02-baixar-a-pagina-com-python/projeto/` a partir da raiz deste repositório, e use os mesmos comandos.

Abra o `.env` e troque `seu-contato-aqui` pelo seu e-mail ou pelo endereço do seu repositório.

Depois rode:

```bash
uv sync
uv run ruff check .
uv run python src/baixar.py
```

Se você não tem o `uv`, instale antes pelo site oficial dele. O `uv sync` instala o Python 3.12 e as bibliotecas.

## Saída esperada

Saída real desta aula (o caminho completo aparece no seu computador, aqui está abreviado):

```
status: 200
bytes gravados: 413130
arquivo: .../projeto/dados/bronze/lista.html
```

E o `ruff check .` mostra:

```
All checks passed!
```

## Guarde no Git

Seu repositório é a pasta `projeto-wikipedia/`, criada na aula 1. Este repositório do curso é a referência: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar ao fim daquela aula.

Na sua pasta do projeto, confira o `git status`, adicione só os arquivos desta aula e envie:

```bash
git status
git add pyproject.toml uv.lock .python-version .env.example .gitignore src/baixar.py
git commit -m "Aula 2: baixar a página com Python"
git push
```

Confira a lista do `git status` antes do `git add`. O `.env` e a pasta `dados/` não devem aparecer nela.

## Erros comuns

- `status: 403` ou outro número diferente de 200: o site recusou o pedido. Confira o `.env` (o contato precisa estar preenchido). Se continuar, pare e não insista.
- `No such file or directory: .env`: o `.env` não existe. Rode `cp .env.example .env`. O programa funciona mesmo sem ele, mas usa um contato genérico.
- `uv: command not found`: o `uv` não está instalado. Instale e abra um terminal novo.
- Erro de conexão: confira a internet e rode de novo.

Aula anterior: [Aula 1: ver o HTML no navegador](../aula-01-ver-o-html-no-navegador/README.md)

Próxima aula: [Aula 3: tirar um dado, o título](../aula-03-tirar-um-dado-o-titulo/README.md)

Aula na plataforma: (link a definir)
