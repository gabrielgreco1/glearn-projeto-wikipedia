"""Testes da leitura da tabela. Usam a tabela da página de 15/11/2026, guardada em testes/amostra_lista.html: não
precisam da pasta dados/, que só existe depois de rodar o projeto."""

from pathlib import Path

from ler import ler_estados, numero

AMOSTRA = Path(__file__).parent / "amostra_lista.html"


def test_numero_troca_o_espaco_e_a_virgula():
    assert numero("164\xa0122,2") == 164122.2
    assert numero("4,30") == 4.3
    assert numero("") is None


def test_a_tabela_tem_27_estados_com_os_tipos_certos():
    html = AMOSTRA.read_text(encoding="utf-8")
    estados = ler_estados(html)
    assert len(estados) == 27
    for estado in estados:
        assert len(estado["sigla"]) == 2
        assert isinstance(estado["area_km2"], float)
        assert isinstance(estado["populacao"], int)
        assert estado["pagina"].startswith("https://pt.wikipedia.org/wiki/")
