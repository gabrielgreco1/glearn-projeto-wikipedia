"""Testa a leitura da ficha com uma página escrita à mão. Não precisa da pasta dados/."""

from pathlib import Path

from ficha import ler_ficha

AMOSTRA = Path(__file__).parent / "amostra_ficha.html"


def test_ler_ficha_guarda_o_texto_como_esta_na_pagina():
    campos = ler_ficha(AMOSTRA.read_text(encoding="utf-8"))
    assert campos["regiao"] == "Norte"
    assert campos["area"] == "100\xa0000,500 km² ( 9 º) [ 1 ]"
    assert campos["pib"] == "12,5 bilhões ( 9º )"


def test_campo_que_a_ficha_nao_tem_fica_de_fora():
    campos = ler_ficha(AMOSTRA.read_text(encoding="utf-8"))
    assert "municipios" not in campos
