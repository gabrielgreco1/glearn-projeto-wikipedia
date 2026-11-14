"""Testa a medição com um CSV pequeno, escrito pelo próprio teste. Não precisa da pasta dados/."""

from perfil import medir

CSV = """sigla,area_km2,populacao,densidade,latitude
AA,100.0,1000,10.0,-5.0
BB,200.0,1000,9.0,
"""


def test_medir_conta_os_vazios_e_refaz_a_densidade(tmp_path):
    arquivo = tmp_path / "estados.csv"
    arquivo.write_text(CSV, encoding="utf-8")
    medidas = medir(arquivo)
    assert medidas["linhas"] == 2
    assert medidas["vazios"] == {"latitude": 1}
    assert medidas["sem_coordenadas"] == ["BB"]
    assert medidas["densidades_diferentes"] == 1
