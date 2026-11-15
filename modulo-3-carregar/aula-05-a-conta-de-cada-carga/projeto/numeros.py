"""Transforma o texto da ficha em número: área, municípios, PIB per capita, IDH e o ano do PIB."""

import csv
import re
from decimal import Decimal
from pathlib import Path

from baixar import registro

COLUNAS = ["sigla", "regiao", "municipios", "area_km2", "pib_per_capita", "idh", "ano_pib", "pib", "arquivo"]


def limpar(texto):
    """Tira da célula o que não é o valor: a posição no ranking, a nota de rodapé, a unidade e a classificação."""
    texto = texto.replace("\xa0", " ")
    texto = re.sub(r"\(.*?\)", "", texto)  # ( 16 º), a posição entre os estados
    texto = re.sub(r"\[.*?\]", "", texto)  # [ 3 ], a nota de rodapé
    texto = re.sub(r"–.*$", "", texto)  # – alto, a classificação do IDH
    texto = texto.replace("km²", "").replace("R$", "")
    return texto.strip()


def numero(texto):
    """'164 123,738' vira Decimal('164123.738'). Ponto e espaço separam milhar; a vírgula separa os decimais."""
    limpo = limpar(texto).replace(" ", "").replace(".", "").replace(",", ".")
    if not re.fullmatch(r"\d+(\.\d+)?", limpo):
        return None
    return Decimal(limpo)


def inteiro(texto):
    valor = numero(texto)
    return int(valor) if valor is not None else None


def converter(ficha):
    """Recebe uma linha do fichas.csv e devolve a mesma linha com números. O PIB fica como texto: é a próxima aula."""
    return {
        "sigla": ficha["sigla"],
        "regiao": ficha["regiao"],
        "municipios": inteiro(ficha["municipios"]),
        "area_km2": numero(ficha["area"]),
        "pib_per_capita": numero(ficha["pib_per_capita"]),
        "idh": numero(ficha["idh"]),
        "ano_pib": inteiro(ficha["ano_pib"].split()[0]),
        "pib": ficha["pib"],
        "arquivo": ficha["arquivo"],
    }


def main():
    with Path("dados/fichas.csv").open(newline="", encoding="utf-8") as entrada:
        linhas = [converter(ficha) for ficha in csv.DictReader(entrada)]
    destino = Path("dados/numeros.csv")
    with destino.open("w", newline="", encoding="utf-8") as saida:
        escritor = csv.DictWriter(saida, fieldnames=COLUNAS)
        escritor.writeheader()
        escritor.writerows(linhas)
    for coluna in ["municipios", "area_km2", "pib_per_capita", "idh", "ano_pib"]:
        vazios = [linha["sigla"] for linha in linhas if linha[coluna] is None]
        registro.info("%s: %s convertidos, vazios: %s", coluna, 27 - len(vazios), ", ".join(vazios) or "nenhum")
    registro.info("gravei %s linhas em %s", len(linhas), destino)


if __name__ == "__main__":
    main()
