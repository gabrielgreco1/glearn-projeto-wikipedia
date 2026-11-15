"""Carrega a silver no Postgres: as linhas de dados/silver/estados.parquet vão para a tabela estados, numa transação.
Rodar de novo não duplica nada: a linha nova entra, a que mudou é atualizada e a igual fica como está."""

import hashlib
from pathlib import Path

import pandas as pd

from baixar import registro
from banco import conectar, criar_tabelas

SILVER = Path("dados/silver/estados.parquet")
# O que a linha diz sobre o estado: se um destes valores muda, a linha mudou.
DADOS = [
    "estado", "regiao", "municipios", "area_km2", "populacao", "idh", "pib_per_capita", "ano_pib", "pib_reais",
    "latitude", "longitude",
]
# De onde e quando a linha veio: muda a cada coleta ou transformação, mesmo com o dado igual.
ORIGEM = ["arquivo", "revisao", "revisao_em", "sha256_ficha", "transformado_em"]
COLUNAS = ["sigla", *DADOS, *ORIGEM, "hash_conteudo"]

UPSERT = f"""
INSERT INTO estados AS e ({", ".join(COLUNAS)})
SELECT {", ".join(COLUNAS)} FROM chegando ORDER BY sigla
ON CONFLICT (sigla) DO UPDATE
    SET {", ".join(f"{coluna} = EXCLUDED.{coluna}" for coluna in COLUNAS[1:])}, carregado_em = now()
    WHERE e.hash_conteudo IS DISTINCT FROM EXCLUDED.hash_conteudo
RETURNING (xmax = 0) AS inserido
"""


def ler_silver():
    """A silver, com municipios como inteiro: no Parquet ele é decimal (22.0), porque o DF não tem municípios."""
    return pd.read_parquet(SILVER).astype({"municipios": "Int64"})


def linhas(tabela, colunas):
    """Cada linha da tabela vira uma tupla, na ordem das colunas. Vazio vira None, que o Postgres grava como NULL."""
    tabela = tabela[colunas].astype(object)
    tabela = tabela.where(tabela.notna(), None)
    return list(tabela.itertuples(index=False, name=None))


def hash_conteudo(valores):
    """O sha256 dos valores, em texto, separados por |. Mesmos valores, mesmo hash, em qualquer dia."""
    texto = "|".join("" if valor is None else str(valor) for valor in valores)
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def com_hash(tabela):
    """Acrescenta a coluna hash_conteudo, calculada só com as colunas de DADOS."""
    tabela = tabela.copy()
    tabela["hash_conteudo"] = [hash_conteudo(valores) for valores in linhas(tabela, DADOS)]
    return tabela


def carregar_estados(conexao, tabela):
    """COPY para uma tabela temporária e, de lá, um upsert pela sigla. Devolve quantas linhas entraram, quantas
    foram atualizadas e quantas ficaram iguais."""
    conexao.execute("CREATE TEMP TABLE chegando (LIKE estados INCLUDING DEFAULTS) ON COMMIT DROP")
    with conexao.cursor() as cursor:
        with cursor.copy(f"COPY chegando ({', '.join(COLUNAS)}) FROM STDIN") as copia:
            for linha in linhas(tabela, COLUNAS):
                copia.write_row(linha)
        tocadas = cursor.execute(UPSERT).fetchall()
    inseridos = sum(1 for (inserido,) in tocadas if inserido)
    return inseridos, len(tocadas) - inseridos, len(tabela) - len(tocadas)


def conferir(silver, banco):
    """A conta da carga: o banco tem de ter as mesmas linhas e a mesma soma da população que a silver. Se não
    fecha, para com erro, e o with da conexão desfaz a carga inteira."""
    if silver != banco:
        raise ValueError(f"a carga não fecha: a silver tem (linhas, população) = {silver} e o banco tem {banco}")


def main():
    tabela = com_hash(ler_silver())
    silver = (len(tabela), int(tabela["populacao"].sum()))
    with conectar() as conexao:
        criar_tabelas(conexao)
        inseridos, atualizados, iguais = carregar_estados(conexao, tabela)
        banco = conexao.execute("SELECT count(*), sum(populacao)::bigint FROM estados").fetchone()
        conferir(silver, banco)
        conexao.execute(
            "INSERT INTO cargas (tentados, inseridos, atualizados, iguais, populacao, revisao_ate)"
            " VALUES (%s, %s, %s, %s, %s, %s)",
            [len(tabela), inseridos, atualizados, iguais, silver[1], tabela["revisao_em"].max()],
        )
    registro.info("estados: %s linhas da silver; novas %s, atualizadas %s, iguais %s", len(tabela), inseridos, atualizados, iguais)
    registro.info("conferido: %s linhas e %s habitantes, na silver e no banco", *silver)


if __name__ == "__main__":
    main()
