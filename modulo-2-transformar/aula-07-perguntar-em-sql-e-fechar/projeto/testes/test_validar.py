"""Testa as regras com uma cópia pequena da tabela, guardada em testes/. Não precisa da pasta dados/."""

from pathlib import Path

import pandas as pd
import pandera.errors
import pytest

from validar import Estados

AMOSTRA = Path(__file__).parent / "amostra_pib.csv"


def tabela_de_27():
    """A amostra tem um estado; a regra pede 27. Repete a linha com 27 siglas diferentes."""
    linha = pd.read_csv(AMOSTRA)
    tabela = pd.concat([linha] * 27, ignore_index=True)
    tabela["sigla"] = [chr(65 + i // 26) + chr(65 + i % 26) for i in range(27)]
    return tabela


def test_tabela_certa_passa():
    Estados.validate(tabela_de_27(), lazy=True)


def test_idh_maior_que_um_falha_com_o_nome_da_regra():
    tabela = tabela_de_27()
    tabela.loc[0, "idh"] = 7.54  # a vírgula do 0,754 lida no lugar errado
    with pytest.raises(pandera.errors.SchemaErrors) as erro:
        Estados.validate(tabela, lazy=True)
    assert "less_than_or_equal_to(1)" in str(erro.value)


def test_regiao_escrita_errado_falha():
    tabela = tabela_de_27()
    tabela.loc[0, "regiao"] = "Centro Oeste"
    with pytest.raises(pandera.errors.SchemaErrors):
        Estados.validate(tabela, lazy=True)
