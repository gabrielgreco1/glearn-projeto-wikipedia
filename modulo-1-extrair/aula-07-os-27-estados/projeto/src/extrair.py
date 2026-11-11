"""Etapa 2: lê o bronze e monta a tabela dos estados em CSV, na camada silver.

Uso:
    uv run python src/extrair.py
"""

import csv
import json
from urllib.parse import unquote

from bs4 import BeautifulSoup

from comum import DADOS, registro, ultimo_bronze

COLUNAS = [
    "sigla",
    "estado",
    "capital",
    "area_km2",
    "populacao",
    "pagina",
    "descricao",
    "latitude",
    "longitude",
]


def texto(celula) -> str:
    """O texto de uma célula, sem as notas de rodapé como [1]."""
    for nota in celula.select("sup"):
        nota.decompose()
    return celula.get_text(" ", strip=True)


def numero(valor: str) -> float | None:
    """'1 521 306' ou '164 173,4' viram número. Vazio vira None."""
    limpo = valor.replace("\xa0", "").replace(" ", "").replace(".", "").replace(",", ".")
    try:
        return float(limpo)
    except ValueError:
        return None


def ler_estados(html: str) -> list[dict]:
    """Acha a tabela dos estados no HTML e devolve uma linha por estado."""
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


def juntar_resumo(estado: dict, pasta) -> dict:
    """Acrescenta ao estado o que a API devolveu: descrição curta e coordenadas."""
    arquivo = pasta / f"resumo-{estado['sigla']}.json"
    resumo = json.loads(arquivo.read_text(encoding="utf-8")) if arquivo.exists() else {}
    coordenadas = resumo.get("coordinates", {})
    return {
        **estado,
        "descricao": resumo.get("description"),
        "latitude": coordenadas.get("lat"),
        "longitude": coordenadas.get("lon"),
    }


def main():
    pasta = ultimo_bronze()
    estados = ler_estados((pasta / "lista.html").read_text(encoding="utf-8"))
    linhas = [juntar_resumo(estado, pasta) for estado in estados]
    destino = DADOS / "silver" / "estados.csv"
    destino.parent.mkdir(parents=True, exist_ok=True)
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(linhas)
    registro.info("%s estados gravados em %s (bronze: %s)", len(linhas), destino, pasta.name)


if __name__ == "__main__":
    main()
