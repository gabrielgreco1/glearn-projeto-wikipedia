"""Apoio aos testes de auditoria: carrega o código de uma pasta do repositório e troca a rede por respostas de mentira.

Nenhum teste desta pasta faz pedido à Wikipedia.
"""

import importlib
import sys
from pathlib import Path

import pytest
import requests

RAIZ = Path(__file__).resolve().parents[1]
AMOSTRA = RAIZ / "final" / "testes" / "amostras" / "lista-3-estados.html"
MODULOS = ["baixar", "titulo", "tabela", "api", "comum", "coletar", "extrair"]


class Resposta:
    """Uma resposta de mentira, com o que o código do projeto usa de requests.Response."""

    def __init__(self, conteudo=b"", status=200, url="https://exemplo.test/", tipo="text/html; charset=UTF-8"):
        self.content = conteudo
        self.status_code = status
        self.url = url
        self.headers = {"Content-Type": tipo}

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(f"{self.status_code} para {self.url}", response=self)


@pytest.fixture
def carregar(monkeypatch):
    """Importa um módulo de uma pasta src do repositório, sem sobras de outra pasta."""

    def _carregar(pasta_src: str, nome: str):
        for modulo in MODULOS:
            sys.modules.pop(modulo, None)
        monkeypatch.syspath_prepend(str(RAIZ / pasta_src))
        monkeypatch.setenv("WIKI_USER_AGENT", "auditoria/0.1 (teste local)")
        monkeypatch.setenv("WIKI_PAUSA", "0")
        return importlib.import_module(nome)

    yield _carregar
    for modulo in MODULOS:
        sys.modules.pop(modulo, None)


def pasta_da_aula(numero: int) -> str:
    achadas = sorted((RAIZ / "modulo-1-extrair").glob(f"aula-0{numero}-*"))
    return str(achadas[0].relative_to(RAIZ) / "projeto" / "src")
