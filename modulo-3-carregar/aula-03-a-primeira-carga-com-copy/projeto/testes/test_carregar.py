"""Testa a preparação das linhas para o COPY, sem banco: duas linhas da silver, com os vazios de verdade."""

import pandas as pd

from carregar import linhas

AMOSTRA = pd.DataFrame({
    "sigla": ["AC", "DF"],
    "municipios": pd.array([22, None], dtype="Int64"),  # o DF não tem municípios
    "latitude": [float("nan"), float("nan")],  # 13 estados vêm sem coordenadas
    "idh": [0.754, 0.866],
})


def test_vazio_vira_none_e_nao_nan():
    acre, df = linhas(AMOSTRA, ["sigla", "municipios", "latitude", "idh"])
    assert acre == ("AC", 22, None, 0.754)
    assert df == ("DF", None, None, 0.866)


def test_municipios_sai_inteiro():
    acre, _ = linhas(AMOSTRA, ["municipios"])
    assert isinstance(acre[0], int)
