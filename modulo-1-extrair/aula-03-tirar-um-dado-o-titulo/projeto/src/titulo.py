"""Aula 3: lê o arquivo que já foi salvo e mostra o título da página.

O arquivo é lido do disco. Nada é baixado de novo.

Uso:
    uv run python src/titulo.py
"""

from pathlib import Path

from bs4 import BeautifulSoup

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO = RAIZ / "dados" / "bronze" / "lista.html"


def main():
    html = ARQUIVO.read_text(encoding="utf-8")
    pagina = BeautifulSoup(html, "html.parser")
    titulo = pagina.select_one("h1#firstHeading")  # o seletor: o h1 com id firstHeading
    if titulo is None:
        print("Não achei o título. A página mudou?")
        return
    print("título:", titulo.get_text(strip=True))


if __name__ == "__main__":
    main()
