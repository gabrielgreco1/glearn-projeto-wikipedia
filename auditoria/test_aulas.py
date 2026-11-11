"""Auditoria dos programas das aulas 2 a 6, sem rede: cada um é carregado da pasta da própria aula."""

import csv

import pytest
import requests
from conftest import AMOSTRA, Resposta, pasta_da_aula


class Get:
    def __init__(self, resposta):
        self.resposta, self.chamadas = resposta, []

    def __call__(self, url, **opcoes):
        self.chamadas.append((url, opcoes))
        if isinstance(self.resposta, Exception):
            raise self.resposta
        return self.resposta


@pytest.mark.parametrize("aula", [2, 3, 4, 5, 6])
def test_baixar_grava_uma_vez_com_user_agent_e_timeout(carregar, tmp_path, monkeypatch, capsys, aula):
    baixar = carregar(pasta_da_aula(aula), "baixar")
    destino = tmp_path / "dados" / "bronze" / "lista.html"
    get = Get(Resposta("página com ação".encode("utf-8")))
    monkeypatch.setattr(baixar, "DESTINO", destino)
    monkeypatch.setattr(baixar.requests, "get", get)
    baixar.main()
    baixar.main()
    assert destino.read_bytes() == "página com ação".encode("utf-8")
    assert len(get.chamadas) == 1  # a segunda execução usa o arquivo
    url, opcoes = get.chamadas[0]
    assert url == "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"
    assert opcoes == {"headers": {"User-Agent": "auditoria/0.1 (teste local)"}, "timeout": 30}
    assert "não baixo de novo" in capsys.readouterr().out


@pytest.mark.parametrize("status", [403, 404, 429, 500])
def test_baixar_status_de_erro_nao_grava(carregar, tmp_path, monkeypatch, capsys, status):
    baixar = carregar(pasta_da_aula(2), "baixar")
    monkeypatch.setattr(baixar, "DESTINO", tmp_path / "lista.html")
    monkeypatch.setattr(baixar.requests, "get", Get(Resposta(b"recusado", status)))
    baixar.main()
    assert not (tmp_path / "lista.html").exists()
    assert f"status: {status}" in capsys.readouterr().out


def test_baixar_rede_fora_do_ar_nao_e_engolida(carregar, tmp_path, monkeypatch):
    baixar = carregar(pasta_da_aula(2), "baixar")
    monkeypatch.setattr(baixar, "DESTINO", tmp_path / "lista.html")
    monkeypatch.setattr(baixar.requests, "get", Get(requests.ConnectionError("sem rede")))
    with pytest.raises(requests.ConnectionError):
        baixar.main()
    assert not (tmp_path / "lista.html").exists()


def test_titulo_acha_e_avisa_quando_nao_acha(carregar, tmp_path, monkeypatch, capsys):
    titulo = carregar(pasta_da_aula(3), "titulo")
    arquivo = tmp_path / "lista.html"
    monkeypatch.setattr(titulo, "ARQUIVO", arquivo)
    arquivo.write_text('<h1 id="firstHeading"> Título com ação </h1>', encoding="utf-8")
    titulo.main()
    arquivo.write_text("<h1>sem id</h1>", encoding="utf-8")
    titulo.main()
    assert capsys.readouterr().out == "título: Título com ação\nNão achei o título. A página mudou?\n"


def test_tabela_da_aula_4_mostra_as_celulas_e_avisa_sem_tabela(carregar, tmp_path, monkeypatch, capsys):
    tabela = carregar(pasta_da_aula(4), "tabela")
    arquivo = tmp_path / "lista.html"
    monkeypatch.setattr(tabela, "ARQUIVO", arquivo)
    arquivo.write_bytes(AMOSTRA.read_bytes())
    tabela.main()
    saida = capsys.readouterr().out.splitlines()
    assert saida[:5] == ["0 ''", "1 'Acre'", "2 'AC'", "3 'Rio Branco'", "4 '164\\xa0122,2'"]
    arquivo.write_text("<p>nada</p>", encoding="utf-8")
    tabela.main()
    assert capsys.readouterr().out == "Não achei a tabela. A página mudou?\n"


@pytest.mark.parametrize("aula", [5, 6])
def test_tabela_grava_csv_e_rodar_de_novo_nao_duplica(carregar, tmp_path, monkeypatch, aula):
    tabela = carregar(pasta_da_aula(aula), "tabela")
    monkeypatch.setattr(tabela, "ARQUIVO", AMOSTRA)
    monkeypatch.setattr(tabela, "SAIDA", tmp_path / "silver" / "estados.csv")
    tabela.main()
    primeira = tabela.SAIDA.read_bytes()
    tabela.main()
    assert tabela.SAIDA.read_bytes() == primeira
    linhas = list(csv.DictReader(tabela.SAIDA.open(encoding="utf-8")))
    assert list(linhas[0]) == ["sigla", "estado", "capital", "area_km2", "populacao", "pagina"]
    assert [linha["sigla"] for linha in linhas] == ["AC", "AL", "AP"]
    assert linhas[2]["estado"] == "Amapá" and linhas[1]["capital"] == "Maceió"


def test_api_guarda_usa_o_arquivo_e_404_vira_excecao(carregar, tmp_path, monkeypatch, capsys):
    api = carregar(pasta_da_aula(6), "api")
    monkeypatch.setattr(api, "BRONZE", tmp_path)
    monkeypatch.setattr(api, "ARQUIVO_API", tmp_path / "resumo-AC.json")
    monkeypatch.setattr(api, "ARQUIVO_HTML", AMOSTRA)
    monkeypatch.setattr(api.requests, "get", Get(Resposta(b"{}", 404)))
    with pytest.raises(requests.HTTPError):
        api.main()
    assert not (tmp_path / "resumo-AC.json").exists()
    get = Get(Resposta('{"description": "unidade federativa do Brasil"}'.encode("utf-8")))
    monkeypatch.setattr(api.requests, "get", get)
    api.main()
    api.main()
    assert len(get.chamadas) == 1
    url, opcoes = get.chamadas[0]
    assert url == "https://pt.wikipedia.org/api/rest_v1/page/summary/Acre" and opcoes["timeout"] == 30
    saida = capsys.readouterr().out
    assert "coordenadas: a API não devolveu para este estado" in saida
    assert "na tabela (HTML): Acre | Rio Branco | 164122.2" in saida
    assert "resumo já está em bronze, não baixo de novo" in saida
