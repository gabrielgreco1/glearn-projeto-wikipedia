"""Testa a impressão do arquivo com a amostra da ficha, guardada em testes/."""

from pathlib import Path

from camadas import impressao

AMOSTRA = Path(__file__).parent / "amostra_ficha.html"


def test_impressao_e_sempre_a_mesma_para_o_mesmo_arquivo():
    assert impressao(AMOSTRA) == impressao(AMOSTRA)
    assert len(impressao(AMOSTRA)) == 64
