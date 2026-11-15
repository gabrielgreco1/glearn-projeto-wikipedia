"""Confere o CSV final: 27 linhas, nenhuma sigla repetida e os tipos certos."""

import csv
from pathlib import Path

from baixar import registro


def conferir(caminho):
    with caminho.open(newline="", encoding="utf-8") as arquivo:
        linhas = list(csv.DictReader(arquivo))
    siglas = [linha["sigla"] for linha in linhas]
    assert len(linhas) == 27, f"esperava 27 linhas, achei {len(linhas)}"
    assert len(set(siglas)) == 27, "tem sigla repetida"
    for linha in linhas:
        float(linha["area_km2"])  # dá erro se não for número
        int(linha["populacao"])
        assert linha["origem_tabela"] == "html"
    com_resumo = sum(1 for linha in linhas if linha["origem_resumo"] == "api")
    com_coordenadas = sum(1 for linha in linhas if linha["latitude"])
    registro.info("conferido: 27 linhas, 27 siglas diferentes, %s com resumo, %s com coordenadas", com_resumo, com_coordenadas)


if __name__ == "__main__":
    conferir(Path("dados/estados_completo.csv"))
