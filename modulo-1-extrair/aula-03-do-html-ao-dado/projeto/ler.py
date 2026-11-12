"""Lê o HTML guardado em disco e tira dele a linha do Acre."""

from pathlib import Path

from bs4 import BeautifulSoup

html = Path("dados/lista.html").read_text(encoding="utf-8")
pagina = BeautifulSoup(html, "html.parser")

print(pagina.title.get_text())

tabelas = pagina.select("table.wikitable.sortable")
print(len(tabelas), "tabela")
tabela = tabelas[0]

linhas = tabela.select("tr")
print(len(linhas), "linhas")

celulas = linhas[1].select("td")
estado = {
    "sigla": celulas[2].get_text(strip=True),
    "estado": celulas[1].get_text(strip=True),
    "capital": celulas[3].get_text(strip=True),
    "area_km2": celulas[4].get_text(strip=True),
    "populacao": celulas[5].get_text(strip=True),
}
print(estado)
