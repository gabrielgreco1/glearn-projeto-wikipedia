"""Roda a etapa Transformar inteira, na ordem, sobre o que já está em dados/. Não faz pedido nenhum ao site."""

import camadas
import consultar
import ficha
import numeros
import pib
from baixar import registro


def main():
    registro.info("etapa 1 de 5: ler a ficha de cada estado")
    ficha.main()
    registro.info("etapa 2 de 5: texto em número")
    numeros.main()
    registro.info("etapa 3 de 5: o PIB e os rejeitados")
    pib.main()
    registro.info("etapa 4 de 5: validar e gravar as camadas")
    camadas.main()
    registro.info("etapa 5 de 5: perguntas em SQL")
    consultar.main()


if __name__ == "__main__":
    main()
