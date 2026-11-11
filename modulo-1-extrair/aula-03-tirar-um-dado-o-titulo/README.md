# Aula 3: tirar um dado, o título

## O que você vai ter no fim

- Um programa, `src/titulo.py`, que lê o HTML que já está no disco e mostra o título da página.
- A ideia de seletor: uma forma de apontar para uma parte exata do HTML.

## O que muda em relação à aula anterior

Arquivos novos e alterados:

- `projeto/src/titulo.py`: novo. Lê o arquivo e mostra o título.
- `projeto/pyproject.toml`: alterado. Entrou a biblioteca `beautifulsoup4`.
- `projeto/src/baixar.py`: igual à aula 2, continua no projeto.

## Conceitos desta aula

- **Seletor**: um texto que aponta para uma parte do HTML. Ele funciona como um endereço. Por exemplo, `h1#firstHeading` quer dizer: "um `h1` (título grande) cujo `id` é `firstHeading`".
- **BeautifulSoup**: a biblioteca que lê o HTML e acha as partes usando seletores. Ela transforma o HTML em uma árvore que o Python consegue navegar.
- **Ler do disco**: o programa abre `dados/bronze/lista.html`, que você salvou na aula 2. Ele não pede nada ao site. Assim, você não sobrecarrega a Wikipedia enquanto aprende.

## O código, bloco por bloco

Leitura do arquivo salvo:

```python
ARQUIVO = RAIZ / "dados" / "bronze" / "lista.html"
html = ARQUIVO.read_text(encoding="utf-8")
```

- `ARQUIVO` aponta para o HTML salvo na aula 2.
- `read_text` lê o arquivo inteiro como texto. `encoding="utf-8"` diz em qual codificação ele está gravado, para as letras com acento saírem certas.

Criação da árvore e uso do seletor:

```python
pagina = BeautifulSoup(html, "html.parser")
titulo = pagina.select_one("h1#firstHeading")
```

- `BeautifulSoup(html, "html.parser")` lê o HTML com o leitor embutido do Python.
- `select_one` devolve a primeira parte que bate com o seletor. Se nenhuma bater, devolve `None`.

Conferência e impressão:

```python
if titulo is None:
    print("Não achei o título. A página mudou?")
    return
print("título:", titulo.get_text(strip=True))
```

- Se o seletor não achou nada, o programa avisa e para. Sempre confira antes de usar o resultado.
- `get_text(strip=True)` pega só o texto, sem as marcas, e tira espaços sobrando nas pontas.

## Como rodar

Esta pasta tem o próprio `baixar.py`. Ele pede a página à Wikipedia e guarda o HTML em `dados/bronze/lista.html`. Rode ele antes das outras etapas desta aula.

Na sua pasta do projeto (`projeto-wikipedia/`), rode:

```bash
cp .env.example .env   # e troque o contato dentro dele
uv sync
uv run python src/baixar.py
uv sync
uv run ruff check .
uv run python src/titulo.py
```

Para rodar o gabarito deste curso, entre antes em `modulo-1-extrair/aula-03-tirar-um-dado-o-titulo/projeto/` a partir da raiz deste repositório, e use os mesmos comandos.

Se o `dados/bronze/lista.html` já existe, o `baixar.py` avisa e não pede a página de novo.

## Saída esperada

```
título: Unidades federativas do Brasil
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
git add pyproject.toml uv.lock src/titulo.py
git commit -m "Aula 3: tirar o título da página com um seletor"
git push
```

Confira a lista do `git status` antes do `git add`. O `.env` e a pasta `dados/` não devem aparecer nela.

## Erros comuns

- `FileNotFoundError` com `lista.html`: o arquivo não está em `dados/bronze/`. Rode o `baixar.py` do passo acima.
- `Não achei o título`: o arquivo copiado não é a página certa. Confira se ele começa com `<!DOCTYPE html>`.
- `ModuleNotFoundError: bs4`: você não rodou o `uv sync`. Rode e tente de novo com `uv run`.

Aula anterior: [Aula 2: baixar a página com Python](../aula-02-baixar-a-pagina-com-python/README.md)

Próxima aula: [Aula 4: achar a tabela e ler uma linha](../aula-04-achar-a-tabela-e-ler-uma-linha/README.md)

Aula na plataforma: (link a definir)
