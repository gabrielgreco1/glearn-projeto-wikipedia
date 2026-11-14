"""Junta os dois caminhos num CSV só: a tabela, que veio do HTML, e o resumo, que veio da API."""

import csv
import json
from pathlib import Path

from baixar import registro
from ler import COLUNAS, ler_estados

COLUNAS_COMPLETAS = COLUNAS + ["descricao", "latitude", "longitude", "origem_tabela", "origem_resumo"]


def juntar(estado):
    """Acrescenta ao estado o que a API devolveu e diz de onde veio cada parte."""
    arquivo = Path("dados/resumos") / f"{estado['sigla']}.json"
    resumo = json.loads(arquivo.read_text(encoding="utf-8")) if arquivo.exists() else {}
    coordenadas = resumo.get("coordinates", {})
    return {
        **estado,
        "descricao": resumo.get("description"),
        "latitude": coordenadas.get("lat"),
        "longitude": coordenadas.get("lon"),
        "origem_tabela": "html",
        "origem_resumo": "api" if resumo else None,
    }


def main():
    html = Path("dados/lista.html").read_text(encoding="utf-8")
    linhas = [juntar(estado) for estado in ler_estados(html)]
    destino = Path("dados/estados_completo.csv")
    with destino.open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=COLUNAS_COMPLETAS)
        escritor.writeheader()
        escritor.writerows(linhas)
    registro.info("%s estados gravados em %s", len(linhas), destino)


if __name__ == "__main__":
    main()
