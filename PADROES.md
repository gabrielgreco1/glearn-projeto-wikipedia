# Padrões do Projeto 1

## Código

- Python 3.13, a versão que o `uv init` gravou no `.python-version`.
- Rodamos tudo com `uv`: `uv sync` para instalar, `uv run python arquivo.py` para rodar, `uv run pytest` para testar.
- Os programas ficam na raiz da pasta do projeto, um arquivo por etapa: `baixar.py`, `ler.py`, `paginas.py`, `resumos.py`, `juntar.py`, `conferir.py`, `rodar.py`.
- Nomes de arquivos, funções e variáveis em português.
- Nas aulas 2 a 4 o programa avisa com `print`. A partir da aula 5 ele registra com `logging`.
- Testes com pytest onde há transformação de dado.

## Configuração e segredos

- O contato do `User-Agent` fica no arquivo `.env`. O `.env.example` mostra o campo, sem dado de verdade.
- O `.env` nunca vai para o Git. Ele está no `.gitignore`.
- Nenhuma senha ou chave no código.

## Dados

- Tudo o que o programa baixa ou gera fica em `dados/`: `lista.html`, `estados.csv`, `estados/`, `resumos/`, `estados_completo.csv`.
- A pasta `dados/` não vai para o Git. O programa baixa e gera tudo de novo.
- Rodar duas vezes não repete pedido nem estraga nada: o arquivo que já existe é reaproveitado.

## Banco

- O Postgres do projeto roda no Docker, descrito no `compose.yaml`, na porta 5433 da sua máquina. Suba com `docker compose up -d --wait`.
- A senha e o endereço do banco ficam no `.env` (`POSTGRES_PASSWORD` e `DATABASE_URL`), como o contato. São de treino, e mesmo assim não vão para o Git.
- As tabelas ficam em `schema.sql`. Uma tabela que muda ganha um `ALTER TABLE … IF NOT EXISTS` no fim do arquivo: rodar de novo nunca apaga nada.
- Toda carga é uma transação: entra inteira, conferida contra a silver, ou não entra.
- Rodar a carga duas vezes não muda o banco: upsert pela chave, com o hash só dos valores do estado.

## Educação com o site da Wikipedia

- Todo pedido leva um `User-Agent` com o nome do projeto e um contato de verdade.
- Um pedido de cada vez, com um segundo de espera depois de cada um.
- Se o site recusar o pedido, o programa para e você lê a mensagem. Não tente contornar.

## Git

- O aluno trabalha na pasta dele, `projeto-wikipedia/`, criada na aula 1. Ela é o repositório do aluno.
- Este repositório do curso é a referência.
- Um commit por aula, com push ao fim de cada aula.
