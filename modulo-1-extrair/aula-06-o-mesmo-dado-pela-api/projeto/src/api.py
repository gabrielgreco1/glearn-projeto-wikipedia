"""Aula 6: pede o resumo do Acre pela API oficial e compara com a linha da tabela.

Uso:
    uv run python src/api.py
"""

import json
import os
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv

from tabela import ler_estados

load_dotenv()

RAIZ = Path(__file__).resolve().parents[1]
BRONZE = RAIZ / "dados" / "bronze"
ARQUIVO_HTML = BRONZE / "lista.html"
ARQUIVO_API = BRONZE / "resumo-AC.json"
USER_AGENT = os.getenv("WIKI_USER_AGENT", "projeto-de-estudo/0.1 (preencha o .env)")
PAGINA = "Acre"


def pegar_resumo() -> bytes:
    """Se o JSON já está em bronze, usa ele. Senão, pede à API e guarda a resposta como veio."""
    if ARQUIVO_API.exists():
        print("resumo já está em bronze, não baixo de novo")
        return ARQUIVO_API.read_bytes()
    url = "https://pt.wikipedia.org/api/rest_v1/page/summary/" + quote(PAGINA, safe="")
    resposta = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    print("status:", resposta.status_code)
    resposta.raise_for_status()
    BRONZE.mkdir(parents=True, exist_ok=True)
    ARQUIVO_API.write_bytes(resposta.content)
    return resposta.content


def main():
    resumo = json.loads(pegar_resumo().decode("utf-8"))
    print("descrição:", resumo.get("description"))
    coordenadas = resumo.get("coordinates")
    if coordenadas is None:
        print("coordenadas: a API não devolveu para este estado")
    else:
        print("coordenadas:", coordenadas["lat"], coordenadas["lon"])

    estados = ler_estados(ARQUIVO_HTML.read_text(encoding="utf-8"))
    acre = next(estado for estado in estados if estado["sigla"] == "AC")
    print("na tabela (HTML):", acre["estado"], "|", acre["capital"], "|", acre["area_km2"])


if __name__ == "__main__":
    main()
