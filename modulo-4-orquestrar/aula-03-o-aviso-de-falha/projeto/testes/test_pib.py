"""Testa a leitura do PIB com textos copiados das fichas reais, como estavam em 14 de novembro de 2026."""

from decimal import Decimal

from pib import avaliar, conferir_pib, leituras

BILHAO = Decimal(10) ** 9


def test_ponto_ambiguo_gera_duas_leituras():
    assert leituras("21.374 bilhões ( 25º )") == [21374 * BILHAO, Decimal("21.374") * BILHAO]


def test_virgula_nao_e_ambigua():
    assert leituras("131,531 bilhões ( 16º )") == [Decimal("131.531") * BILHAO]


def test_numero_sem_unidade_fica_como_esta():
    assert leituras("402\xa0646\xa0605\xa0640 ( 7º )") == [Decimal("402646605640")]


def test_conferencia_aceita_perto_e_recusa_mil_vezes_maior():
    assert conferir_pib(Decimal(100), Decimal(10), 10) is None
    assert "vezes o esperado" in conferir_pib(Decimal(100_000), Decimal(10), 10)


def test_acre_fica_com_a_leitura_que_bate():
    acre = {"sigla": "AC", "pib": "21.374 bilhões ( 25º )", "pib_per_capita": "23569.31"}
    linha, rejeitados = avaliar(acre, 830_018)
    assert linha["pib_reais"] == Decimal("21374000000")
    assert rejeitados == []


def test_per_capita_impossivel_vai_para_os_rejeitados():
    pernambuco = {"sigla": "PE", "pib": "245,828 bilhões ( 11º )", "pib_per_capita": "27.139"}
    linha, rejeitados = avaliar(pernambuco, 9_058_931)
    assert linha is None
    assert [r["coluna"] for r in rejeitados] == ["pib_per_capita", "pib"]
