"""Lê a ficha de cada estado nas 27 páginas que a PW-05 guardou e grava o texto de cada campo como está na página."""

import csv
from pathlib import Path

from bs4 import BeautifulSoup

from baixar import registro

# O rótulo da linha na ficha da Wikipedia e o nome da coluna no CSV.
CAMPOS = {
    "• Região": "regiao",
    "• Municípios": "municipios",
    "• Área total": "area",
    "• PIB total": "pib",
    "• PIB per capita": "pib_per_capita",
    "• IDH (2024)": "idh",
    "Economia": "ano_pib",
}
COLUNAS = ["sigla", *CAMPOS.values(), "arquivo"]


def ler_ficha(html):
    """Devolve um dicionário com o texto de cada campo da ficha. Campo que a ficha não tem fica de fora."""
    pagina = BeautifulSoup(html, "html.parser")
    ficha = pagina.select_one("table.infobox")
    campos = {}
    for linha in ficha.select("tr"):
        celulas = linha.find_all(["th", "td"], recursive=False)
        if len(celulas) < 2:
            continue
        rotulo = celulas[0].get_text(" ", strip=True)
        if rotulo in CAMPOS and CAMPOS[rotulo] not in campos:
            campos[CAMPOS[rotulo]] = celulas[1].get_text(" ", strip=True)
    return campos


def main():
    linhas = []
    for arquivo in sorted(Path("dados/estados").glob("*.html")):
        campos = ler_ficha(arquivo.read_text(encoding="utf-8"))
        linhas.append({"sigla": arquivo.stem, **campos, "arquivo": str(arquivo)})
    destino = Path("dados/fichas.csv")
    with destino.open("w", newline="", encoding="utf-8") as saida:
        escritor = csv.DictWriter(saida, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(linhas)
    faltando = [linha["sigla"] for linha in linhas if len(linha) < len(COLUNAS)]
    registro.info("%s fichas lidas, sem nenhum pedido, gravadas em %s", len(linhas), destino)
    registro.info("fichas com campo faltando: %s", ", ".join(faltando) or "nenhuma")


if __name__ == "__main__":
    main()
