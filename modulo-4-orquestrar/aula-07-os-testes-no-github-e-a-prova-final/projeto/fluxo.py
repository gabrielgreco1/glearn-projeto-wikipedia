"""O projeto Wikipedia como um flow do Prefect: uma task para cada etapa, na ordem, sobre a coleta do dia. As que
pedem à Wikipedia são tentadas de novo quando falham: o que já está em disco não é pedido outra vez. Se a execução
termina mal, fica um aviso em avisos.log.

Uso: uv run python fluxo.py            roda uma vez, agora
     uv run python fluxo.py agendar    fica ligado e roda todo dia às 6h (Ctrl+C para parar)
"""

import sys
from datetime import date, datetime
from pathlib import Path

from prefect import flow, task
from prefect.schedules import Cron

import carregar as carga
import coleta
import conferir
import juntar
import paginas
import resumos
import transformar as transformacao
from baixar import URL_LISTA, baixar
from ler import gravar_csv, ler_estados


@task
def preparar_coleta(dia):
    return coleta.preparar(dia)


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


def avisar(flow, flow_run, state):
    """O Prefect chama esta função quando a execução termina em Failed ou Crashed. O aviso diz o que olhar primeiro."""
    aviso = f"AVISO: {flow.name}, execução {flow_run.name}, terminou em {state.name}: {state.message}"
    print(aviso)
    with open("avisos.log", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"{datetime.now():%Y-%m-%d %H:%M:%S} {aviso} (o que fazer: runbook.md)\n")


@flow(log_prints=True, on_failure=[avisar], on_crashed=[avisar])
def projeto_wikipedia():
    dia = date.today().isoformat()
    preparar_coleta(dia)
    baixar_lista()
    tabela_em_csv()
    baixar_paginas()
    baixar_resumos()
    juntar_e_conferir()
    transformar()
    impressao = carregar()
    print(f"coleta de {dia} no banco, impressão digital {impressao}")


if __name__ == "__main__":
    if sys.argv[1:] == ["agendar"]:
        # Todo dia às 6h, no horário de Brasília. Sem o timezone, o Prefect lê o cron em UTC: seriam 3h da manhã.
        projeto_wikipedia.serve(name="todo-dia", schedule=Cron("0 6 * * *", timezone="America/Sao_Paulo"))
    else:
        projeto_wikipedia()
