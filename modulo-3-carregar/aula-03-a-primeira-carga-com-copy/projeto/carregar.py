"""Carrega a silver no Postgres: as linhas de dados/silver/estados.parquet vão para a tabela estados, numa transação."""

from pathlib import Path

import pandas as pd

from baixar import registro
from banco import conectar, criar_tabelas

SILVER = Path("dados/silver/estados.parquet")
COLUNAS = [
    "sigla", "estado", "regiao", "municipios", "area_km2", "populacao", "idh", "pib_per_capita", "ano_pib",
    "pib_reais", "latitude", "longitude", "arquivo", "revisao", "revisao_em", "sha256_ficha", "transformado_em",
]


def ler_silver():
    """A silver, com municipios como inteiro: no Parquet ele é decimal (22.0), porque o DF não tem municípios."""
    return pd.read_parquet(SILVER).astype({"municipios": "Int64"})


def linhas(tabela, colunas):
    """Cada linha da tabela vira uma tupla, na ordem das colunas. Vazio vira None, que o Postgres grava como NULL."""
    tabela = tabela[colunas].astype(object)
    tabela = tabela.where(tabela.notna(), None)
    return list(tabela.itertuples(index=False, name=None))


def main():
    tabela = ler_silver()
    with conectar() as conexao:
        criar_tabelas(conexao)
        with conexao.cursor() as cursor, cursor.copy(f"COPY estados ({', '.join(COLUNAS)}) FROM STDIN") as copia:
            for linha in linhas(tabela, COLUNAS):
                copia.write_row(linha)
        total = conexao.execute("SELECT count(*) FROM estados").fetchone()[0]
    registro.info("carreguei %s linhas da silver; a tabela estados tem %s", len(tabela), total)


if __name__ == "__main__":
    main()
