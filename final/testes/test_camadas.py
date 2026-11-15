"""Testa a impressão do arquivo, com a amostra da ficha guardada em testes/, e a lista dos arquivos do bronze."""

from pathlib import Path

from camadas import arquivos_do_bronze, impressao

AMOSTRA = Path(__file__).parent / "amostra_ficha.html"


def test_impressao_e_sempre_a_mesma_para_o_mesmo_arquivo():
    assert impressao(AMOSTRA) == impressao(AMOSTRA)
    assert len(impressao(AMOSTRA)) == 64


def test_bronze_listado_na_hora(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)  # o camadas.py já foi importado; os arquivos aparecem só agora
    Path("dados/estados").mkdir(parents=True)
    Path("dados/estados/AC.html").write_text("<html></html>", encoding="utf-8")
    assert Path("dados/estados/AC.html") in arquivos_do_bronze()
