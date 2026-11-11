# Aula 1: ver o HTML no navegador

## O que você vai ter no fim

- Ter visto o código da página da Wikipedia com os seus próprios olhos.
- Ter achado a tabela dos estados no código.
- Saber o que é HTML, de forma simples.

Esta aula não tem Python. Só o navegador.

## O que muda em relação à aula anterior

Esta é a primeira aula. Ela cria a sua pasta de trabalho, `projeto-wikipedia/`, com um `README.md` de uma linha. É o seu repositório no Git.

## O que é HTML

HTML é o código por trás de qualquer página da internet. O navegador lê esse código e desenha a página. Uma tabela, por exemplo, aparece no HTML como texto com marcas, como `<table>` e `<td>`. Essas marcas dizem onde começa e termina cada parte.

Nesta aula você só lê o HTML. Não muda nada.

## Passo a passo

1. Abra o navegador e entre no endereço
   `https://pt.wikipedia.org/wiki/Unidades_federativas_do_Brasil`
2. Você deve ver o título "Unidades federativas do Brasil" e uma tabela grande, com uma linha para cada estado.
3. Ver o código-fonte. Ele é o HTML que o navegador recebeu.
   - No Windows ou Linux, aperte `Ctrl + U`.
   - No Mac, aperte `Cmd + Option + U`.
   - Uma aba nova abre com um texto cheio de marcas. Esse é o HTML.
4. Procurar a palavra "Acre" no código. Use `Ctrl + F` (ou `Cmd + F` no Mac) e digite `Acre`.
   - Você deve ver algumas ocorrências. Uma delas está dentro de uma linha da tabela, perto de "AC" e "Rio Branco".
5. Abrir as ferramentas de desenvolvedor (DevTools). Elas mostram o HTML organizado em árvore.
   - No Windows ou Linux, aperte `F12`.
   - No Mac, aperte `Cmd + Option + I`.
6. Apontar para a tabela no DevTools.
   - Clique no ícone de seta com o quadrado (no canto superior esquerdo do painel, ou aperte `Cmd + Shift + C` ou `Ctrl + Shift + C`).
   - Passe o mouse sobre a tabela na página. Ela fica destacada.
   - Clique nela. O código correspondente aparece no painel.
7. Olhar a linha do Acre no painel. Você deve ver algo como `<tr>` (uma linha), dentro dela várias `<td>` (uma célula cada), com o texto "Acre", "AC", "Rio Branco".

## O que você deve enxergar no fim

- A tabela está no HTML, dentro de uma marca `<table>`.
- Cada estado é uma linha `<tr>`. Cada dado do estado é uma célula `<td>`.
- A tabela tem uma classe chamada `wikitable sortable`. Vamos usar esse nome na aula 4.

Nas próximas aulas, o Python faz estes mesmos passos sozinho.

## Guarde no Git

Seu repositório é uma pasta de trabalho sua, só do seu projeto. Este repositório do curso é a referência: a pasta `projeto/` de cada aula mostra como a sua pasta deve estar ao fim daquela aula.

1. Crie uma pasta nova, `projeto-wikipedia/`, e entre nela.
2. Dentro dela, crie um `README.md` com uma linha: `# Projeto Wikipedia`.
3. No GitHub, crie um repositório novo e vazio, sem README e sem `.gitignore`. Anote o endereço, no formato `https://github.com/<seu-usuario>/<seu-repositorio>.git`.
4. Na pasta `projeto-wikipedia/`, rode:

```bash
git init -b main
git status
git add README.md
git commit -m "Aula 1: ver o HTML no navegador"
git remote add origin https://github.com/<seu-usuario>/<seu-repositorio>.git
git push -u origin main
```

Troque `<seu-usuario>` e `<seu-repositorio>` pelos seus dados. Depois do `git push`, a página do repositório no GitHub mostra o `README.md`.

## Erros comuns

- A página não abre. Confira o endereço. Ele tem "pt" (português) e "Unidades_federativas_do_Brasil" com sublinhado.
- O atalho não abre o código-fonte. Clique com o botão direito na página e escolha "Ver código-fonte" (ou "View page source").
- Não acho "Acre" no código. Use `Ctrl + F` dentro da aba do código-fonte, não na página normal.

Próxima aula: [Aula 2: baixar a página com Python](../aula-02-baixar-a-pagina-com-python/README.md)

Aula na plataforma: (link a definir)
