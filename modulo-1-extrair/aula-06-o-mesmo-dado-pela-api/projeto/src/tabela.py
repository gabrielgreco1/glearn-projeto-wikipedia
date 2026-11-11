"""Aula 5: lê todas as linhas da tabela e grava um CSV em dados/silver.

Uso:
    uv run python src/tabela.py
"""

import csv
from pathlib import Path
from urllib.parse import unquote

from bs4 import BeautifulSoup

RAIZ = Path(__file__).resolve().parents[1]
ARQUIVO = RAIZ / "dados" / "bronze" / "lista.html"
SAIDA = RAIZ / "dados" / "silver" / "estados.csv"
COLUNAS = ["sigla", "estado", "capital", "area_km2", "populacao", "pagina"]


def texto(celula) -> str:
    """O texto de uma célula, sem as notas de rodapé como [1]."""
    for nota in celula.select("sup"):
        nota.decompose()
    return celula.get_text(" ", strip=True)


def numero(valor: str) -> float | None:
    """'164 122,2' vira 164122.2. '830 018' vira 830018. Vazio vira None."""
    limpo = valor.replace("\xa0", "").replace(" ", "").replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return None


def ler_estados(html: str) -> list[dict]:
    """Acha a tabela dos estados e devolve uma linha por estado."""
    pagina = BeautifulSoup(html, "html.parser")
    tabela = pagina.select_one("table.wikitable.sortable")
    if tabela is None:
        raise ValueError("Não achei a tabela dos estados. A página mudou?")
    estados = []
    for linha in tabela.select("tr"):
        celulas = linha.select("td")
        if len(celulas) < 6:
            continue  # cabeçalho ou linha de total
        link = celulas[1].select_one("a[href*='/wiki/']")
        if link is None:
            continue
        populacao = numero(texto(celulas[5]))
        estados.append(
            {
                "sigla": texto(celulas[2]),
                "estado": texto(celulas[1]),
                "capital": texto(celulas[3]),
                "area_km2": numero(texto(celulas[4])),
                "populacao": int(populacao) if populacao is not None else None,
                "pagina": unquote(link["href"].split("/wiki/")[-1]),
            }
        )
    return estados


def main():
    estados = ler_estados(ARQUIVO.read_text(encoding="utf-8"))
    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    with SAIDA.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(estados)
    print(f"{len(estados)} estados gravados em {SAIDA}")


if __name__ == "__main__":
    main()
