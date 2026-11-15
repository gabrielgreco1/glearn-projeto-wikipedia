"""O projeto Wikipedia como um flow do Prefect: uma task para cada etapa, na ordem. As que pedem à Wikipedia são
tentadas de novo quando falham: o que já está em disco não é pedido outra vez."""

from pathlib import Path

from prefect import flow, task

import carregar as carga
import conferir
import juntar
import paginas
import resumos
import transformar as transformacao
from baixar import URL_LISTA, baixar
from ler import gravar_csv, ler_estados


@task(retries=3, retry_delay_seconds=10, timeout_seconds=60)
def baixar_lista():
    baixar(URL_LISTA, Path("dados/lista.html"))


@task
def tabela_em_csv():
    lista = Path("dados/lista.html").read_text(encoding="utf-8")
    gravar_csv(ler_estados(lista), Path("dados/estados.csv"))


baixar_paginas = task(paginas.main, name="paginas", retries=3, retry_delay_seconds=10, timeout_seconds=300)
baixar_resumos = task(resumos.main, name="resumos", retries=3, retry_delay_seconds=10, timeout_seconds=300)


@task
def juntar_e_conferir():
    juntar.main()
    conferir.conferir(Path("dados/estados_completo.csv"))


transformar = task(transformacao.main, name="transformar")
carregar = task(carga.main, name="carregar")


@flow(log_prints=True)
def projeto_wikipedia():
    baixar_lista()
    tabela_em_csv()
    baixar_paginas()
    baixar_resumos()
    juntar_e_conferir()
    transformar()
    carregar()


if __name__ == "__main__":
    projeto_wikipedia()
