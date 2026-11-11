"""Testes da leitura da tabela. A amostra é um pedaço real da página, com três estados."""

from pathlib import Path

from tabela import ler_estados, numero

AMOSTRA = Path(__file__).parent / "amostras" / "lista-3-estados.html"


def test_numero_com_espaco_e_virgula():
    assert numero("164\xa0122,2") == 164122.2
    assert numero("830 018") == 830018
    assert numero("") is None


def test_le_os_tres_estados_da_amostra():
    estados = ler_estados(AMOSTRA.read_text(encoding="utf-8"))
    assert [e["sigla"] for e in estados] == ["AC", "AL", "AP"]
    assert estados[0] == {
        "sigla": "AC",
        "estado": "Acre",
        "capital": "Rio Branco",
        "area_km2": 164122.2,
        "populacao": 830018,
        "pagina": "Acre",
    }


def test_pagina_sem_tabela_avisa():
    try:
        ler_estados("<html><body><p>nada</p></body></html>")
    except ValueError as erro:
        assert "tabela" in str(erro)
    else:
        raise AssertionError("devia ter avisado")
