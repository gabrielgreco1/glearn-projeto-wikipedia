"""Aula 2: baixa a página com a tabela dos estados e guarda a resposta como ela veio.

Uso:
    uv run python src/baixar.py
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()  # lê o arquivo .env desta pasta, se ele existir

URL = "https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil"
RAIZ = Path(__file__).resolve().parents[1]
DESTINO = RAIZ / "dados" / "bronze" / "lista.html"
USER_AGENT = os.getenv("WIKI_USER_AGENT", "projeto-de-estudo/0.1 (preencha o .env)")


def main():
    if DESTINO.exists():
        print("lista.html já está em dados/bronze, não baixo de novo")
        return
    resposta = requests.get(URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    print("status:", resposta.status_code)
    if resposta.status_code != 200:
        print("Não baixei a página. Veja o status acima.")
        return
    DESTINO.parent.mkdir(parents=True, exist_ok=True)
    DESTINO.write_bytes(resposta.content)  # os bytes como vieram, sem mexer
    print("bytes gravados:", len(resposta.content))
    print("arquivo:", DESTINO)


if __name__ == "__main__":
    main()
