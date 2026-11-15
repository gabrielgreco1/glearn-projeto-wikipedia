"""Mede o CSV final antes de qualquer limpeza: tamanho, células vazias e uma conta de conferência."""

from pathlib import Path

import pandas as pd

from baixar import registro


def medir(caminho):
    """Lê o CSV e devolve as medidas num dicionário. Não muda o arquivo."""
    estados = pd.read_csv(caminho)
    vazios = estados.isna().sum()
    conta = (estados["populacao"] / estados["area_km2"]).round(2)
    diferenca = (conta - estados["densidade"]).abs()
    return {
        "linhas": len(estados),
        "colunas": len(estados.columns),
        "vazios": vazios[vazios > 0].to_dict(),
        "sem_coordenadas": estados[estados["latitude"].isna()]["sigla"].tolist(),
        "densidades_diferentes": int((diferenca > 0.01).sum()),
    }


def main():
    medidas = medir(Path("dados/estados_completo.csv"))
    registro.info("%s linhas e %s colunas", medidas["linhas"], medidas["colunas"])
    registro.info("colunas com célula vazia: %s", medidas["vazios"])
    registro.info("sem coordenadas: %s", ", ".join(medidas["sem_coordenadas"]))
    registro.info("densidade da tabela diferente da conta em %s de %s estados", medidas["densidades_diferentes"], medidas["linhas"])


if __name__ == "__main__":
    main()
