"""Baixa a página de cada estado: 27 pedidos, um de cada vez, com pausa entre eles."""

from pathlib import Path

import httpx

from baixar import baixar, registro
from ler import ler_estados


def main():
    html = Path("dados/lista.html").read_text(encoding="utf-8")
    estados = ler_estados(html)
    sem_pagina = 0
    for estado in estados:
        destino = Path("dados/estados") / f"{estado['sigla']}.html"
        try:
            arquivo = baixar(estado["pagina"], destino)
        except httpx.RequestError as erro:
            registro.error("sem rede no pedido de %s: %s", estado["sigla"], erro)
            registro.error("rode de novo: o programa continua de onde parou")
            raise  # o mesmo erro segue adiante: no Prefect, a task falha e pode ser tentada de novo
        if arquivo is None:
            sem_pagina += 1
    registro.info("%s estados, %s sem página", len(estados), sem_pagina)


if __name__ == "__main__":
    main()
