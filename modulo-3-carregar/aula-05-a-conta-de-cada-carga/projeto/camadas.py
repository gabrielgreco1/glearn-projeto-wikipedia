"""Organiza o projeto em camadas: o bronze é o que veio do site, sem mudança; o silver é a tabela limpa, em Parquet,
com a origem de cada linha. Nada no bronze é alterado."""

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from baixar import registro
from validar import validar

BRONZE = [Path("dados/lista.html"), *sorted(Path("dados/estados").glob("*.html")), *sorted(Path("dados/resumos").glob("*.json"))]
SILVER = Path("dados/silver/estados.parquet")


def impressao(arquivo):
    """O sha256 do arquivo: se um byte mudar, a impressão muda."""
    return hashlib.sha256(arquivo.read_bytes()).hexdigest()


def inventario():
    """Uma linha por arquivo do bronze: caminho, tamanho e impressão. É o que permite provar que o bronze não mudou."""
    return pd.DataFrame([
        {"arquivo": str(arquivo), "bytes": arquivo.stat().st_size, "sha256": impressao(arquivo)} for arquivo in BRONZE
    ])


def origem_do_resumo(sigla):
    """A revisão e o instante da página na Wikipedia, que vieram dentro do resumo da API."""
    resumo = json.loads((Path("dados/resumos") / f"{sigla}.json").read_text(encoding="utf-8"))
    return {"revisao": resumo.get("revision"), "revisao_em": resumo.get("timestamp")}


def montar_silver():
    tabela = validar(Path("dados/pib.csv"))
    coordenadas = pd.read_csv("dados/estados_completo.csv")[["sigla", "estado", "latitude", "longitude"]]
    tabela = tabela.merge(coordenadas, on="sigla", how="left", validate="one_to_one")
    origem = pd.DataFrame([{"sigla": sigla, **origem_do_resumo(sigla)} for sigla in tabela["sigla"]])
    tabela = tabela.merge(origem, on="sigla", validate="one_to_one")
    tabela["sha256_ficha"] = [impressao(Path(arquivo)) for arquivo in tabela["arquivo"]]
    tabela["transformado_em"] = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    return tabela


def main():
    Path("dados/bronze").mkdir(parents=True, exist_ok=True)
    bronze = inventario()
    bronze.to_csv("dados/bronze/inventario.csv", index=False)
    registro.info("bronze: %s arquivos, %s bytes, inventário em dados/bronze/inventario.csv", len(bronze), int(bronze["bytes"].sum()))
    SILVER.parent.mkdir(parents=True, exist_ok=True)
    silver = montar_silver()
    silver.to_parquet(SILVER, index=False)
    registro.info("silver: %s linhas e %s colunas em %s", len(silver), len(silver.columns), SILVER)


if __name__ == "__main__":
    main()
