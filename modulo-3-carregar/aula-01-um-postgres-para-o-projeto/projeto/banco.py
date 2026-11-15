"""A conexão com o Postgres do projeto, que roda no Docker (compose.yaml). O endereço vem do .env."""

import os

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


def main():
    with conectar() as conexao:
        versao = conexao.execute("SELECT version()").fetchone()[0]
    registro.info("conectado: %s", versao)


if __name__ == "__main__":
    main()
