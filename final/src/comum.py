"""Peças usadas por todas as etapas: configuração, pedido ao site e gravação em bronze."""

import hashlib
import json
import logging
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

RAIZ = Path(__file__).resolve().parents[1]
DADOS = RAIZ / "dados"
SITE = "https://pt.wikipedia.org"
USER_AGENT = os.getenv("WIKI_USER_AGENT", "projeto-de-estudo/0.1 (preencha o .env)")
PAUSA = float(os.getenv("WIKI_PAUSA", "1"))

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
registro = logging.getLogger("wikipedia")

_sessao = requests.Session()
_sessao.headers["User-Agent"] = USER_AGENT


def pedir(url: str) -> requests.Response:
    """Faz um GET, espera a pausa combinada e devolve a resposta. Erro HTTP vira exceção."""
    resposta = _sessao.get(url, timeout=30)
    time.sleep(PAUSA)
    resposta.raise_for_status()
    return resposta


def pasta_bronze(dia: str | None = None) -> Path:
    """Pasta do bronze de um dia de coleta. Sem dia, usa a data de hoje (UTC)."""
    dia = dia or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    return DADOS / "bronze" / f"coleta={dia}"


def ultimo_bronze() -> Path:
    """A pasta de bronze mais recente que existe no disco."""
    pastas = sorted((DADOS / "bronze").glob("coleta=*"))
    if not pastas:
        raise FileNotFoundError("Não há bronze. Rode antes: uv run python src/coletar.py")
    return pastas[-1]


def gravar_bronze(resposta: requests.Response, nome: str, pasta: Path) -> Path:
    """Grava os bytes da resposta sem mexer em nada, e ao lado um arquivo com a origem."""
    pasta.mkdir(parents=True, exist_ok=True)
    arquivo = pasta / nome
    arquivo.write_bytes(resposta.content)
    origem = {
        "url": resposta.url,
        "status": resposta.status_code,
        "tipo": resposta.headers.get("Content-Type"),
        "coletado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sha256": hashlib.sha256(resposta.content).hexdigest(),
        "bytes": len(resposta.content),
    }
    (pasta / f"{nome}.origem.json").write_text(
        json.dumps(origem, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return arquivo
