"""Aula 4: acha a tabela dos estados e mostra as células da primeira linha de dados.

Uso:
    uv run python src/tabela.py
"""

from pathlib import Path

from bs4 import BeautifulSoup

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO = RAIZ / "dados" / "bronze" / "lista.html"


def main():
    html = ARQUIVO.read_text(encoding="utf-8")
    pagina = BeautifulSoup(html, "html.parser")
    tabela = pagina.select_one("table.wikitable.sortable")  # a tabela com essas classes
    if tabela is None:
        print("Não achei a tabela. A página mudou?")
        return
    linhas = tabela.select("tr")
    primeira_linha_de_dados = linhas[1]  # a linha 0 é o cabeçalho
    for numero_da_celula, celula in enumerate(primeira_linha_de_dados.select("td")):
        print(numero_da_celula, repr(celula.get_text(" ", strip=True)))


if __name__ == "__main__":
    main()
