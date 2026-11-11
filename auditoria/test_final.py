"""Auditoria de final/ (igual à aula 7): pedido, gravação em bronze, retomada, leitura da tabela e CSV."""

import csv
import hashlib
import json

import pytest
import requests
from conftest import AMOSTRA, Resposta

TABELA = '<table class="wikitable sortable"><tbody><tr><th>a</th></tr>{linhas}</tbody></table>'
LINHA = "<tr><td></td><td><a href=\"{href}\">{nome}</a></td><td>{sigla}</td><td>{capital}</td><td>{area}</td><td>{pop}</td></tr>"


class Rede:
    """Conta os pedidos e responde: a lista com a amostra de três estados, e um resumo por estado."""

    def __init__(self, falha_em=None, status=200):
        self.pedidos, self.falha_em, self.status = [], falha_em, status

    def get(self, url, timeout=None):
        self.pedidos.append((url, timeout))
        if self.falha_em and self.falha_em in url:
            return Resposta(b"", self.status, url)
        if "/api/" in url:
            return Resposta('{"description": "descrição com acento ã"}'.encode("utf-8"), 200, url, "application/json")
        return Resposta(AMOSTRA.read_bytes(), 200, url)


@pytest.fixture
def projeto(carregar, tmp_path, monkeypatch):
    comum = carregar("final/src", "comum")
    coletar = __import__("coletar")
    extrair = __import__("extrair")
    monkeypatch.setattr(comum, "DADOS", tmp_path / "dados")
    monkeypatch.setattr(extrair, "DADOS", tmp_path / "dados")
    monkeypatch.setattr(comum, "PAUSA", 0)
    rede = Rede()
    monkeypatch.setattr(comum, "_sessao", rede)
    monkeypatch.setattr("sys.argv", ["coletar.py"])
    return comum, coletar, extrair, rede, tmp_path / "dados"


def test_user_agent_identificavel_e_timeout(carregar):
    comum = carregar("final/src", "comum")
    assert comum._sessao.headers["User-Agent"] == "auditoria/0.1 (teste local)"
    assert "python-requests" not in comum._sessao.headers["User-Agent"]


def test_pedir_passa_timeout_e_espera_a_pausa(projeto, monkeypatch):
    comum, _, _, rede, _ = projeto
    esperas = []
    monkeypatch.setattr(comum, "PAUSA", 1.0)
    monkeypatch.setattr(comum.time, "sleep", esperas.append)
    comum.pedir("https://exemplo.test/x")
    assert rede.pedidos == [("https://exemplo.test/x", 30)]
    assert esperas == [1.0]


@pytest.mark.parametrize("status", [403, 404, 429, 500])
def test_pedir_erro_http_vira_excecao(projeto, status):
    comum, _, _, rede, _ = projeto
    rede.falha_em, rede.status = "x", status
    with pytest.raises(requests.HTTPError):
        comum.pedir("https://exemplo.test/x")


def test_rede_fora_do_ar_nao_e_engolida_e_nada_e_gravado(projeto, monkeypatch):
    comum, coletar, _, _, dados = projeto

    class SemRede:
        def get(self, url, timeout=None):
            raise requests.ConnectionError("sem rede")

    monkeypatch.setattr(comum, "_sessao", SemRede())
    with pytest.raises(requests.ConnectionError):
        coletar.main()
    assert not list(dados.rglob("*.html"))


def test_gravar_bronze_guarda_os_bytes_e_a_origem(projeto, tmp_path):
    comum = projeto[0]
    conteudo = "ação, São Paulo".encode("utf-8")
    arquivo = comum.gravar_bronze(Resposta(conteudo, 200, "https://exemplo.test/p"), "p.html", tmp_path / "b")
    assert arquivo.read_bytes() == conteudo
    origem = json.loads((tmp_path / "b" / "p.html.origem.json").read_text(encoding="utf-8"))
    assert origem["url"] == "https://exemplo.test/p" and origem["status"] == 200
    assert origem["bytes"] == len(conteudo)
    assert origem["sha256"] == hashlib.sha256(conteudo).hexdigest()
    assert origem["coletado_em"].endswith("+00:00")


def test_coletar_duas_vezes_nao_pede_nem_duplica(projeto):
    _, coletar, _, rede, dados = projeto
    coletar.main()
    assert len(rede.pedidos) == 4  # a lista e os três estados da amostra
    arquivos = sorted(p.name for p in dados.rglob("*") if p.is_file())
    coletar.main()
    assert len(rede.pedidos) == 4
    assert sorted(p.name for p in dados.rglob("*") if p.is_file()) == arquivos
    assert len(arquivos) == 8  # 4 respostas e 4 arquivos de origem


def test_retomada_pede_so_o_que_falta(projeto):
    comum, coletar, _, rede, _ = projeto
    rede.falha_em, rede.status = "Alagoas", 429
    with pytest.raises(requests.HTTPError):
        coletar.main()
    pasta = comum.pasta_bronze()
    assert (pasta / "resumo-AC.json").exists() and not (pasta / "resumo-AL.json").exists()
    rede.falha_em, antes = None, len(rede.pedidos)
    coletar.main()
    novos = [url for url, _ in rede.pedidos[antes:]]
    assert [u.rsplit("/", 1)[-1] for u in novos] == ["Alagoas", "Amap%C3%A1"]


def test_so_lista_nao_pede_resumos(projeto, monkeypatch):
    _, coletar, _, rede, _ = projeto
    monkeypatch.setattr("sys.argv", ["coletar.py", "--so-lista"])
    coletar.main()
    assert len(rede.pedidos) == 1


def test_nome_com_acento_e_parenteses_vai_codificado(projeto):
    _, coletar, _, rede, tmp = projeto
    coletar.coletar_resumos(tmp, [{"sigla": "SP", "pagina": "São_Paulo_(estado)"}])
    assert rede.pedidos[0][0].endswith("/api/rest_v1/page/summary/S%C3%A3o_Paulo_%28estado%29")


def test_tabela_sem_linhas_devolve_lista_vazia(projeto):
    assert projeto[2].ler_estados(TABELA.format(linhas="")) == []


def test_link_absoluto_relativo_acento_celula_vazia_e_nota(projeto):
    linhas = "".join(
        [
            LINHA.format(href="https://pt.wikipedia.org/wiki/S%C3%A3o_Paulo_(estado)", nome="São Paulo", sigla="SP", capital="São Paulo<sup>[1]</sup>", area="248\xa0209,4", pop="44\xa0411\xa0238"),
            LINHA.format(href="/wiki/Acre", nome="Acre", sigla="AC", capital="Rio Branco", area="", pop=""),
            "<tr><td></td><td>Total</td><td></td><td></td><td></td><td></td></tr>",
        ]
    )
    estados = projeto[2].ler_estados(TABELA.format(linhas=linhas))
    assert [e["pagina"] for e in estados] == ["São_Paulo_(estado)", "Acre"]
    assert estados[0]["capital"] == "São Paulo" and estados[0]["area_km2"] == 248209.4
    assert estados[0]["populacao"] == 44411238
    assert estados[1]["area_km2"] is None and estados[1]["populacao"] is None


def test_extrair_grava_csv_e_rodar_de_novo_nao_duplica(projeto):
    _, coletar, extrair, _, dados = projeto
    coletar.main()
    (next((dados / "bronze").iterdir()) / "resumo-AP.json").unlink()  # um resumo que faltou
    extrair.main()
    destino = dados / "silver" / "estados.csv"
    primeira = destino.read_bytes()
    extrair.main()
    assert destino.read_bytes() == primeira
    linhas = list(csv.DictReader(destino.open(encoding="utf-8")))
    assert list(linhas[0]) == extrair.COLUNAS and len(linhas) == 3
    assert linhas[0]["descricao"] == "descrição com acento ã" and linhas[0]["latitude"] == ""
    assert linhas[2]["sigla"] == "AP" and linhas[2]["descricao"] == ""


def test_extrair_sem_bronze_avisa(projeto):
    with pytest.raises(FileNotFoundError, match="coletar.py"):
        projeto[2].main()
