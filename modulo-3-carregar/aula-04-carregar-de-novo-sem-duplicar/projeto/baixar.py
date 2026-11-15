"""Baixa uma página e guarda em disco. Se o arquivo já existe, não pede de novo."""

import logging
import os
import time
from pathlib import Path

import httpx
from dotenv import load_dotenv

load_dotenv()

USER_AGENT = os.getenv("WIKI_USER_AGENT")
if not USER_AGENT:
    raise SystemExit("Falta WIKI_USER_AGENT no arquivo .env. Copie o .env.example para .env e preencha.")

URL_LISTA = "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"
CABECALHOS = {"User-Agent": USER_AGENT}
PAUSA = 1.0  # segundos de espera depois de cada pedido

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s", datefmt="%H:%M:%S")
logging.getLogger("httpx").setLevel(logging.WARNING)  # o httpx também registra cada pedido; aqui basta o nosso registro
registro = logging.getLogger("wikipedia")


def baixar(url, destino):
    """Pede a página e grava no arquivo de destino. Devolve o caminho, ou None se a página não existe."""
    if destino.exists():
        registro.info("já tenho %s, não peço de novo", destino)
        return destino
    resposta = httpx.get(url, headers=CABECALHOS, timeout=30)
    time.sleep(PAUSA)
    if resposta.status_code == 404:
        registro.warning("a página não existe: %s", url)
        return None
    if resposta.status_code != 200:
        raise RuntimeError(f"{url} respondeu {resposta.status_code}")
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(resposta.content)
    registro.info("baixei %s: %s bytes em %s", url, len(resposta.content), destino)
    return destino


if __name__ == "__main__":
    baixar(URL_LISTA, Path("dados/lista.html"))
