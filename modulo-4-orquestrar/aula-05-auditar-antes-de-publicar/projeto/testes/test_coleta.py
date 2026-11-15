"""Testa a coleta de cada dia numa pasta vazia do teste, sem pedir nada à Wikipedia."""

from pathlib import Path

from coleta import preparar


def test_dia_novo_guarda_a_coleta_anterior(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("dados/estados").mkdir(parents=True)
    Path("dados/coleta.txt").write_text("2026-11-15", encoding="utf-8")
    Path("dados/estados/AC.html").write_text("<html>de ontem</html>", encoding="utf-8")
    assert preparar("2026-11-16") is True
    assert Path("dados_anterior/estados/AC.html").exists()  # a coleta de ontem, inteira
    assert not Path("dados/estados").exists()  # a de hoje começa vazia
    assert Path("dados/coleta.txt").read_text(encoding="utf-8") == "2026-11-16"


def test_mesmo_dia_continua_de_onde_parou(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    Path("dados/estados").mkdir(parents=True)
    Path("dados/coleta.txt").write_text("2026-11-16", encoding="utf-8")
    Path("dados/estados/AC.html").write_text("<html>de hoje</html>", encoding="utf-8")
    assert preparar("2026-11-16") is False
    assert Path("dados/estados/AC.html").exists()  # o que já foi baixado hoje fica
    assert not Path("dados_anterior").exists()
