"""Responde perguntas em SQL direto sobre o Parquet do silver e grava a resposta na camada gold."""

from pathlib import Path

import duckdb

from baixar import registro

POR_REGIAO = """
SELECT
    regiao,
    count(*) AS estados,
    sum(populacao) AS populacao,
    count(pib_reais) AS estados_com_pib,
    round(sum(pib_reais) / 1e9, 1) AS pib_bilhoes,
    round(sum(pib_reais) / sum(populacao) FILTER (WHERE pib_reais IS NOT NULL), 0) AS pib_por_pessoa
FROM 'dados/silver/estados.parquet'
GROUP BY regiao
ORDER BY populacao DESC
"""

MAIOR_IDH_POR_REGIAO = """
SELECT regiao, sigla, idh
FROM (
    SELECT regiao, sigla, idh, row_number() OVER (PARTITION BY regiao ORDER BY idh DESC) AS posicao
    FROM 'dados/silver/estados.parquet'
)
WHERE posicao = 1
ORDER BY idh DESC
"""

SEM_COORDENADAS = "SELECT sigla FROM 'dados/silver/estados.parquet' WHERE latitude IS NULL ORDER BY sigla"


def main():
    Path("dados/gold").mkdir(parents=True, exist_ok=True)
    regioes = duckdb.sql(POR_REGIAO)
    regioes.show()
    regioes.write_parquet("dados/gold/regioes.parquet")
    duckdb.sql(MAIOR_IDH_POR_REGIAO).show()
    sem = [linha[0] for linha in duckdb.sql(SEM_COORDENADAS).fetchall()]
    registro.info("gold: dados/gold/regioes.parquet; sem coordenadas: %s estados (%s)", len(sem), ", ".join(sem))


if __name__ == "__main__":
    main()
