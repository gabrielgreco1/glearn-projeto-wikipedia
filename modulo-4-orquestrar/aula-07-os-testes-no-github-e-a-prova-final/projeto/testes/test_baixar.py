"""Testa o baixar.py sem o contato do .env, como nos testes do GitHub: importar o arquivo funciona, e o pedido para
com a mensagem que diz o que falta."""

import pytest

import baixar


def test_sem_contato_o_pedido_para_com_a_mensagem(tmp_path, monkeypatch):
    monkeypatch.delenv("WIKI_USER_AGENT", raising=False)  # tira o contato só durante este teste
    with pytest.raises(SystemExit, match="WIKI_USER_AGENT"):
        baixar.baixar("https://pt.wikipedia.org/wiki/Acre", tmp_path / "AC.html")
