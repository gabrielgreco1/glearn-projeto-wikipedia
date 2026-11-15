# Runbook: o projeto não carregou

O que fazer quando chega um aviso. Siga as checagens na ordem: a primeira que explicar o aviso é a causa.

## Sintoma

Uma linha nova em `avisos.log`, com a execução terminada em `Failed` ou `Crashed`. No painel do Prefect (http://127.0.0.1:4200), a mesma execução aparece em vermelho, com o log de cada task.

## Impacto

O banco continua com a última carga que deu certo, inteira: a carga é uma transação, e a que falha não grava nada. Quem lê o banco vê os dados da coleta anterior. Nada se perde; falta só a coleta de hoje.

## Checagens, nesta ordem

1. **`Crashed` com `Python system exit call`.** O programa parou de propósito. A mensagem do que fazer não vai para o painel: ela sai no fim do terminal onde o projeto rodou, depois do aviso. "O banco não respondeu": suba o banco com `docker compose up -d --wait`. "Falta ... no arquivo .env": copie a linha do `.env.example` para o `.env`. Tentar de novo sem resolver não adianta.
2. **`Failed` numa task que pede à Wikipedia (`baixar_lista`, `paginas` ou `resumos`), depois das tentativas.** É a internet ou a Wikipedia. Abra https://pt.wikipedia.org no navegador. Quando ela responder, rode de novo: o que já foi baixado não é pedido outra vez.
3. **`Failed` em `juntar_e_conferir` ou em `transformar`.** A página mudou de formato e uma regra barrou: a mensagem diz qual. O banco não foi tocado. Abra a página no navegador e compare com o que o código espera.
4. **`Failed` em `carregar`, com `a auditoria barrou a carga`.** Um valor mudou mais do que a regra aceita, e a mensagem diz qual regra e quais estados. Nada foi publicado. Abra a página do estado e veja o valor: se a página está errada (uma edição que alguém ainda vai desfazer), espere e rode de novo mais tarde; se o valor mudou de verdade (um censo novo), mude a regra em `carregar.py`, com um commit que diga por quê.
5. **`Crashed` com `interrupt signal`.** Alguém apertou Ctrl+C ou a máquina desligou no meio. Rode de novo.

Para rodar de novo: `uv run python fluxo.py`.
