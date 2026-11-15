"""Testa a conversão com textos copiados das fichas reais, como estavam em 14 de novembro de 2026."""

from decimal import Decimal

from numeros import inteiro, limpar, numero


def test_limpar_tira_ranking_nota_e_unidade():
    assert limpar("164\xa0123,738 km² ( 16 º) [ 3 ]") == "164 123,738"
    assert limpar("0,866 ( 1º ) – muito alto [ 7 ]") == "0,866"


def test_area_com_espaco_especial_e_virgula():
    assert numero("1\xa0559\xa0167,878 km² ( 1 º) [ 2 ]") == Decimal("1559167.878")


def test_pib_per_capita_com_ponto_de_milhar():
    assert numero("23.569,31 ( 17º )") == Decimal("23569.31")


def test_pib_per_capita_com_real_na_frente():
    assert numero("R$ 20.663 ( 27º )") == Decimal("20663")


def test_idh_e_municipios():
    assert numero("0,754 ( 25º ) – alto [ 9 ]") == Decimal("0.754")
    assert inteiro("853") == 853


def test_celula_vazia_vira_none_e_nao_zero():
    assert numero("") is None
    assert inteiro("") is None
