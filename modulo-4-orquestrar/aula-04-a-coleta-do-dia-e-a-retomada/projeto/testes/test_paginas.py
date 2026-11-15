"""Testa o que o paginas.py faz quando a rede falha, sem pedir nada à Wikipedia: o pedido de verdade é trocado
por uma função que falha como falharia sem internet."""

from pathlib import Path

import httpx
import pytest

import paginas


def test_sem_rede_o_erro_segue_adiante(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # o main lê dados/lista.html da pasta atual: aqui, uma pasta vazia do teste
    Path("dados").mkdir()
    Path("dados/lista.html").write_text("<html></html>", encoding="utf-8")
    monkeypatch.setattr(paginas, "ler_estados", lambda html: [{"sigla": "AC", "pagina": "https://pt.wikipedia.org/wiki/Acre"}])

    def sem_rede(url, destino):
        raise httpx.ConnectError("sem rede")

    monkeypatch.setattr(paginas, "baixar", sem_rede)
    with pytest.raises(httpx.ConnectError):  # e não SystemExit: o Prefect tenta de novo um erro, e não uma saída
        paginas.main()
