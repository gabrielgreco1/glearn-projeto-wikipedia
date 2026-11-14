"""Confere a tabela do PIB contra regras escritas: o que não passar para o programa com a lista dos problemas."""

from pathlib import Path

import pandas as pd
import pandera.pandas as pa

from baixar import registro

REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]

ESQUEMA = pa.DataFrameSchema(
    {
        "sigla": pa.Column(str, pa.Check.str_matches(r"^[A-Z]{2}$"), unique=True),
        "regiao": pa.Column(str, pa.Check.isin(REGIOES)),
        "municipios": pa.Column(float, pa.Check.gt(0), nullable=True, coerce=True),  # vazio no DF; coerce: lê inteiro como decimal
        "area_km2": pa.Column(float, pa.Check.gt(0)),
        "populacao": pa.Column(int, pa.Check.gt(0)),
        "idh": pa.Column(float, pa.Check.in_range(0, 1)),
        "ano_pib": pa.Column(int, pa.Check.in_range(2015, 2026)),
        "pib_reais": pa.Column(float, pa.Check.gt(0), nullable=True, coerce=True),  # vazio quando foi para os rejeitados
    },
    checks=pa.Check(lambda tabela: len(tabela) == 27, error="a tabela precisa ter os 27 estados"),
)


def validar(caminho):
    """Lê o CSV e confere todas as regras de uma vez. Devolve a tabela, ou para com a lista do que falhou."""
    tabela = pd.read_csv(caminho)
    return ESQUEMA.validate(tabela, lazy=True)


def main():
    tabela = validar(Path("dados/pib.csv"))
    registro.info("dados/pib.csv passou nas regras: %s linhas, %s colunas conferidas", len(tabela), len(ESQUEMA.columns))
    registro.info("PIB vazio em %s estados, como a regra permite", int(tabela["pib_reais"].isna().sum()))


if __name__ == "__main__":
    main()
