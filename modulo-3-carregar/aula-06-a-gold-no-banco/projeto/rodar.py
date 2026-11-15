"""Roda o projeto inteiro, na ordem. O que já está em disco não é pedido de novo."""

from pathlib import Path

import conferir
import juntar
import paginas
import resumos
from baixar import URL_LISTA, baixar, registro
from ler import gravar_csv, ler_estados


def main():
    registro.info("etapa 1 de 5: a página com a tabela")
    lista = baixar(URL_LISTA, Path("dados/lista.html"))
    registro.info("etapa 2 de 5: a tabela em CSV")
    gravar_csv(ler_estados(lista.read_text(encoding="utf-8")), Path("dados/estados.csv"))
    registro.info("etapa 3 de 5: a página de cada estado")
    paginas.main()
    registro.info("etapa 4 de 5: o resumo de cada estado, pela API")
    resumos.main()
    registro.info("etapa 5 de 5: juntar e conferir")
    juntar.main()
    conferir.conferir(Path("dados/estados_completo.csv"))


if __name__ == "__main__":
    main()
