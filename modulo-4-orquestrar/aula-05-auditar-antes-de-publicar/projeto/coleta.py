"""A coleta de cada dia. A pasta dados/ guarda uma coleta só, marcada com o dia em dados/coleta.txt. Num dia novo,
a coleta que estava lá vai inteira para dados_anterior/, e a de hoje começa do zero. Uma coleta de hoje interrompida
no meio continua de onde parou: o que já está em disco não é pedido de novo."""

import shutil
from pathlib import Path

from baixar import registro

DADOS = Path("dados")
ANTERIOR = Path("dados_anterior")
MARCA = DADOS / "coleta.txt"


def dia_da_coleta():
    """O dia da coleta que está em dados/, ou None se a pasta não tem marca."""
    return MARCA.read_text(encoding="utf-8").strip() if MARCA.exists() else None


def preparar(dia):
    """Deixa dados/ pronta para a coleta do dia. Devolve True se a coleta começa agora, e False se ela continua."""
    marcado = dia_da_coleta()
    if marcado == dia:
        registro.info("a coleta de %s já começou: continua de onde parou", dia)
        return False
    if DADOS.exists():
        shutil.rmtree(ANTERIOR, ignore_errors=True)  # a penúltima coleta sai; fica só a anterior
        DADOS.rename(ANTERIOR)
        registro.info("a coleta que estava em dados/ (%s) foi para %s", marcado or "sem marca", ANTERIOR)
    DADOS.mkdir()
    MARCA.write_text(dia, encoding="utf-8")
    registro.info("coleta de %s: começa do zero", dia)
    return True
