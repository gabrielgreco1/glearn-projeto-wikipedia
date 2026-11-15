"""Testa a medição com um CSV pequeno, guardado em testes/. Não precisa da pasta dados/."""

from pathlib import Path

from perfil import medir

AMOSTRA = Path(__file__).parent / "amostra_estados.csv"


def test_medir_conta_os_vazios_e_refaz_a_densidade():
    medidas = medir(AMOSTRA)
    assert medidas["linhas"] == 2
    assert medidas["vazios"] == {"latitude": 1}
    assert medidas["sem_coordenadas"] == ["BB"]
    assert medidas["densidades_diferentes"] == 1
