# Padrões do Projeto 1

Estas regras valem para todo código do curso. Cada aula segue todas.

## Código

- Python 3.12. Está no `.python-version` e no `requires-python` do `pyproject.toml`.
- Bibliotecas com versão travada no `pyproject.toml`, por exemplo `requests==2.32.5`. As versões são as mesmas em todas as aulas.
- Rodamos tudo com `uv`: `uv sync` para instalar, `uv run python src/...` para rodar, `uv run pytest` para testar, `uv run ruff check .` para conferir o estilo.
- Nomes de arquivos, funções e variáveis em português.
- A partir da aula 7 usamos `logging` no lugar de `print`. Nas aulas 2 a 6 usamos `print`, para não ensinar dois conceitos ao mesmo tempo.
- `ruff check .` não pode mostrar apontamentos.
- Testes com pytest onde há transformação de dado.

## Configuração e segredos

- Configuração fica no arquivo `.env`. O `.env.example` mostra os campos, sem valor real.
- O `.env` nunca vai para o Git. Ele é listado no `.gitignore`.
- Nenhum segredo, senha ou chave no código.
- O `User-Agent` (quem está pedindo a página) fica no `.env`. Ponha o seu contato.

## Dados

- `dados/bronze/`: a resposta guardada como veio. Nunca é alterada depois de gravada.
- `dados/silver/`: os dados limpos, em CSV.
- A pasta `dados/` não vai para o Git. Ela é gerada quando você roda o código.
- Rodar uma etapa duas vezes não duplica nem estraga nada.

## Educação com o site da Wikipedia

- No máximo uma requisição por segundo.
- Baixe o mínimo. Se o arquivo já está no disco, use o arquivo e não peça de novo.
- Se o site recusar o pedido, pare e veja o status. Não tente contornar.

## Git

- O aluno trabalha na pasta dele, `projeto-wikipedia/`, criada na aula 1. Ela é o repositório do aluno.
- Este repositório do curso é a referência. A pasta `projeto/` de cada aula mostra como a pasta do aluno deve estar ao fim daquela aula.
- Um commit por aula, com push ao fim de cada aula.
- Os caminhos do `git add` são relativos à pasta do aluno, e listam só os arquivos novos ou alterados daquela aula.
- Antes de cada `git add`, rode `git status` e confira a lista.
- Adicione os arquivos pelo nome. Não use `git add .` sem olhar antes.
- Mensagem do commit: "Aula N: título da aula".
