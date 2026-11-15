"""O projeto Wikipedia como um flow do Prefect: extrair, transformar e carregar, cada etapa uma task, na ordem."""

from prefect import flow, task

import carregar as carga
import rodar
import transformar as transformacao

extrair = task(rodar.extrair, name="extrair")
transformar = task(transformacao.main, name="transformar")
carregar = task(carga.main, name="carregar")


@flow(log_prints=True)
def projeto_wikipedia():
    extrair()
    transformar()
    carregar()


if __name__ == "__main__":
    projeto_wikipedia()
