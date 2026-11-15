"""Lê a tabela dos estados no HTML guardado em disco e grava um CSV."""

import csv
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup

SITE = "https://pt.wikipedia.org"
COLUNAS = ["sigla", "estado", "capital", "area_km2", "populacao", "densidade", "pagina"]


def numero(texto):
    """'164\xa0122,2' vira 164122.2. Texto vazio vira None."""
    limpo = texto.replace("\xa0", "").replace(" ", "").replace(".", "").replace(",", ".")
    if not limpo:
        return None
    return float(limpo)


def ler_linha(linha):
    """Recebe a linha (tr) de um estado e devolve um dicionário com os campos."""
    celulas = linha.select("td")
    populacao = numero(celulas[5].get_text(strip=True))
    return {
        "sigla": celulas[2].get_text(strip=True),
        "estado": celulas[1].get_text(strip=True),
        "capital": celulas[3].get_text(strip=True),
        "area_km2": numero(celulas[4].get_text(strip=True)),
        "populacao": int(populacao) if populacao is not None else None,
        "densidade": numero(celulas[6].get_text(strip=True)),
        "pagina": urljoin(SITE, celulas[1].select_one("a")["href"]),
    }


def ler_estados(html):
    """Acha a tabela dos estados no HTML e devolve uma lista com um dicionário por estado."""
    pagina = BeautifulSoup(html, "html.parser")
    tabela = pagina.select_one("table.wikitable.sortable")
    if tabela is None:
        raise ValueError("Não achei a tabela dos estados. A página mudou?")
    estados = []
    for linha in tabela.select("tr"):
        if not linha.select("td"):
            continue  # a linha do cabeçalho só tem th
        estados.append(ler_linha(linha))
    return estados


def gravar_csv(estados, destino):
    """Grava a lista de estados num arquivo CSV, com uma linha de cabeçalho."""
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(estados)


if __name__ == "__main__":
    html = Path("dados/lista.html").read_text(encoding="utf-8")
    estados = ler_estados(html)
    gravar_csv(estados, Path("dados/estados.csv"))
    print(f"{len(estados)} estados gravados em dados/estados.csv")
