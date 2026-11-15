"""Confere a tabela do PIB contra regras escritas: o que não passar para o programa com a lista dos problemas."""

from pathlib import Path

import pandas as pd
import pandera.pandas as pa

from baixar import registro

REGIOES = ["Norte", "Nordeste", "Centro-Oeste", "Sudeste", "Sul"]


class Estados(pa.DataFrameModel):
    """Uma linha por estado. Cada coluna é uma regra escrita; o pandera confere todas."""

    sigla: str = pa.Field(str_matches=r"^[A-Z]{2}$", unique=True)
    regiao: str = pa.Field(isin=REGIOES)
    municipios: float = pa.Field(gt=0, nullable=True, coerce=True)  # vazio no DF; coerce: lê inteiro como decimal
    area_km2: float = pa.Field(gt=0)
    populacao: int = pa.Field(gt=0)
    idh: float = pa.Field(ge=0, le=1)
    ano_pib: int = pa.Field(ge=2015, le=2026)
    pib_reais: float = pa.Field(gt=0, nullable=True, coerce=True)  # vazio quando foi para os rejeitados

    @pa.dataframe_check
    def tem_os_27_estados(cls, tabela):
        return len(tabela) == 27


def validar(caminho):
    """Lê o CSV e confere todas as regras de uma vez. Devolve a tabela, ou para com a lista do que falhou."""
    tabela = pd.read_csv(caminho)
    return Estados.validate(tabela, lazy=True)


def main():
    tabela = validar(Path("dados/pib.csv"))
    colunas = len(Estados.to_schema().columns)
    registro.info("dados/pib.csv passou nas regras: %s linhas, %s colunas conferidas", len(tabela), colunas)
    registro.info("PIB vazio em %s estados, como a regra permite", int(tabela["pib_reais"].isna().sum()))


if __name__ == "__main__":
    main()
