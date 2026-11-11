"""Etapa 1: baixa as páginas e as respostas da API e guarda tudo em bronze, como veio.

Uso:
    uv run python src/coletar.py            a lista de estados e os 27 estados
    uv run python src/coletar.py --so-lista só a página com a tabela
"""

import sys
from urllib.parse import quote

from comum import SITE, gravar_bronze, pasta_bronze, pedir, registro
from extrair import ler_estados

PAGINA_LISTA = "Unidades_federativas_do_Brasil"


def coletar_lista(pasta):
    """Baixa o HTML da página que tem a tabela dos estados."""
    destino = pasta / "lista.html"
    if destino.exists():
        registro.info("lista.html já está em bronze, não baixo de novo")
        return destino
    resposta = pedir(f"{SITE}/wiki/{PAGINA_LISTA}")
    registro.info("lista baixada: %s bytes", len(resposta.content))
    return gravar_bronze(resposta, "lista.html", pasta)


def coletar_resumos(pasta, estados):
    """Para cada estado, pede o resumo à API oficial e guarda o JSON."""
    baixados = 0
    for estado in estados:
        nome = f"resumo-{estado['sigla']}.json"
        if (pasta / nome).exists():
            continue
        titulo = quote(estado["pagina"], safe="")
        resposta = pedir(f"{SITE}/api/rest_v1/page/summary/{titulo}")
        gravar_bronze(resposta, nome, pasta)
        baixados += 1
        registro.info("resumo %s (%s de %s)", estado["sigla"], baixados, len(estados))
    registro.info("resumos novos: %s; já existiam: %s", baixados, len(estados) - baixados)


def main():
    pasta = pasta_bronze()
    lista = coletar_lista(pasta)
    if "--so-lista" in sys.argv:
        return
    estados = ler_estados(lista.read_text(encoding="utf-8"))
    coletar_resumos(pasta, estados)


if __name__ == "__main__":
    main()
