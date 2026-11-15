"""A conexão com o Postgres do projeto, que roda no Docker (compose.yaml). O endereço vem do .env."""

import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

from baixar import registro

load_dotenv()


def conectar():
    """Abre uma conexão com o banco. Use com with: no fim do bloco, ela confirma o que foi feito, ou desfaz se deu erro."""
    url = os.getenv("DATABASE_URL")
    if not url:
        raise SystemExit("Falta DATABASE_URL no arquivo .env. Copie as linhas do banco do .env.example.")
    try:
        return psycopg.connect(url)
    except psycopg.OperationalError as erro:
        raise SystemExit(f"O banco não respondeu. Ele está de pé? Rode: docker compose up -d --wait\n{erro}")


def criar_tabelas(conexao):
    """Roda o schema.sql: cria as tabelas que ainda não existem. As que já existem ficam como estão."""
    conexao.execute(Path("schema.sql").read_text(encoding="utf-8"))


def main():
    with conectar() as conexao:
        criar_tabelas(conexao)
        colunas = conexao.execute(
            "SELECT column_name, data_type FROM information_schema.columns"
            " WHERE table_name = 'estados' ORDER BY ordinal_position"
        ).fetchall()
    registro.info("a tabela estados tem %s colunas", len(colunas))
    for nome, tipo in colunas:
        registro.info("  %-15s %s", nome, tipo)


if __name__ == "__main__":
    main()
