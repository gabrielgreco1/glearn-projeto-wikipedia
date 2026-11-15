"""Pede à API da Wikipedia o resumo de cada estado e guarda o JSON em disco."""

from pathlib import Path

import httpx

from baixar import baixar, registro
from ler import ler_estados

API_RESUMO = "https://pt.wikipedia.org/api/rest_v1/page/summary/"


def titulo(pagina):
    """Do endereço da página, fica só o título: o que vem depois de /wiki/."""
    return pagina.split("/wiki/")[1]


def main():
    html = Path("dados/lista.html").read_text(encoding="utf-8")
    estados = ler_estados(html)
    for estado in estados:
        destino = Path("dados/resumos") / f"{estado['sigla']}.json"
        try:
            baixar(API_RESUMO + titulo(estado["pagina"]), destino)
        except httpx.RequestError as erro:
            registro.error("sem rede no pedido de %s: %s", estado["sigla"], erro)
            registro.error("rode de novo: o programa continua de onde parou")
            raise SystemExit(1)
    registro.info("resumos de %s estados em dados/resumos", len(estados))


if __name__ == "__main__":
    main()
