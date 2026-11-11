# Projeto Wikipedia: versão final

Coleta a tabela dos 27 estados do Brasil na Wikipedia em português e o resumo de cada estado pela API oficial.

## Como rodar

```bash
cp .env.example .env        # e troque o contato dentro dele
uv sync
uv run python src/coletar.py
uv run python src/extrair.py
uv run pytest
```

## O que sai

- `dados/bronze/coleta=AAAA-MM-DD/`: a página e as 27 respostas da API como vieram, cada uma com um arquivo `.origem.json` (endereço, instante, tamanho e hash).
- `dados/silver/estados.csv`: uma linha por estado.

Rodar `coletar.py` de novo no mesmo dia não baixa nada que já esteja em bronze.
