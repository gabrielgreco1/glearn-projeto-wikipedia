"""Baixa a página dos estados e guarda em disco. Se o arquivo já existe, não pede de novo."""

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv("WIKI_USER_AGENT")
if not USER_AGENT:
    raise SystemExit("Falta WIKI_USER_AGENT no arquivo .env. Copie o .env.example para .env e preencha.")

URL_LISTA = "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"
CABECALHOS = {"User-Agent": USER_AGENT}


def baixar(url, destino):
    """Pede a página e grava no arquivo de destino. Devolve o caminho do arquivo."""
    if destino.exists():
        print(f"já tenho {destino}, não peço de novo")
        return destino
    resposta = httpx.get(url, headers=CABECALHOS, timeout=30)
    if resposta.status_code != 200:
        raise RuntimeError(f"{url} respondeu {resposta.status_code}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(resposta.content)
    print(f"baixei {url}: {len(resposta.content)} bytes em {destino}")
    return destino


if __name__ == "__main__":
    baixar(URL_LISTA, Path("dados/lista.html"))
