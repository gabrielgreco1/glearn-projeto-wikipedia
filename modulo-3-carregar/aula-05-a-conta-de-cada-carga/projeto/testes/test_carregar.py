"""Testa a preparação das linhas para o COPY e o hash do conteúdo, sem banco: linhas da silver, com os vazios de verdade."""

import pandas as pd
import pytest

from carregar import DADOS, com_hash, conferir, linhas

AMOSTRA = pd.DataFrame({
    "sigla": ["AC", "DF"],
    "municipios": pd.array([22, None], dtype="Int64"),  # o DF não tem municípios
    "latitude": [float("nan"), float("nan")],  # 13 estados vêm sem coordenadas
    "idh": [0.754, 0.866],
})

# O Acre na silver de 15/11/2026: as colunas de DADOS e duas de origem.
ACRE = pd.DataFrame([{
    "sigla": "AC", "estado": "Acre", "regiao": "Norte", "municipios": 22, "area_km2": 164123.738, "populacao": 830018,
    "idh": 0.754, "pib_per_capita": 23569.31, "ano_pib": 2021, "pib_reais": 21374000000.0, "latitude": float("nan"),
    "longitude": float("nan"), "sha256_ficha": "896b0ed0", "transformado_em": "2026-11-15T07:14:38+00:00",
}]).astype({"municipios": "Int64"})


def test_vazio_vira_none_e_nao_nan():
    acre, df = linhas(AMOSTRA, ["sigla", "municipios", "latitude", "idh"])
    assert acre == ("AC", 22, None, 0.754)
    assert df == ("DF", None, None, 0.866)


def test_municipios_sai_inteiro():
    acre, _ = linhas(AMOSTRA, ["municipios"])
    assert isinstance(acre[0], int)


def test_hash_nao_olha_a_origem():
    outra_coleta = ACRE.assign(sha256_ficha="9f86d0", transformado_em="2026-11-16T07:00:00+00:00")
    assert com_hash(ACRE)["hash_conteudo"][0] == com_hash(outra_coleta)["hash_conteudo"][0]


def test_hash_muda_quando_um_dado_muda():
    for coluna, valor in [("idh", 0.755), ("populacao", 830019), ("latitude", -9.0)]:
        assert coluna in DADOS
        mudou = ACRE.assign(**{coluna: valor})
        assert com_hash(ACRE)["hash_conteudo"][0] != com_hash(mudou)["hash_conteudo"][0]


def test_conferir_para_quando_a_conta_nao_fecha():
    conferir((27, 204060756), (27, 204060756))
    with pytest.raises(ValueError, match="não fecha"):
        conferir((27, 204060756), (27, 203230739))
