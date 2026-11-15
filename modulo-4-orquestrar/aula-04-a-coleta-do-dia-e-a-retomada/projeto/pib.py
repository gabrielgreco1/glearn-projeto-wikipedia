"""Converte o PIB para reais. O que não dá para decidir pelo texto vai para uma tabela de rejeitados, com o motivo."""

import csv
from decimal import Decimal
from pathlib import Path

from baixar import registro
from numeros import limpar, numero

UNIDADES = {"trilhões": Decimal(10) ** 12, "trilhão": Decimal(10) ** 12, "bilhões": Decimal(10) ** 9}
PER_CAPITA_MINIMO, PER_CAPITA_MAXIMO = Decimal(5_000), Decimal(200_000)  # reais por pessoa por ano
TOLERANCIA = Decimal("0.25")  # quanto o PIB pode se afastar de per capita × população
COLUNAS = ["sigla", "regiao", "municipios", "area_km2", "populacao", "pib_per_capita", "idh", "ano_pib", "pib_reais", "arquivo"]
COLUNAS_REJEITADOS = ["sigla", "coluna", "texto", "motivo"]


def leituras(texto):
    """As leituras possíveis do texto, em reais. '21.374 bilhões' tem duas: 21 374 bilhões, com ponto de milhar,
    e 21,374 bilhões, com o ponto no lugar da vírgula. O texto sozinho não diz qual é a certa."""
    limpo = limpar(texto)
    multiplicador = Decimal(1)
    for palavra, valor in UNIDADES.items():
        if limpo.endswith(palavra):
            limpo, multiplicador = limpo.removesuffix(palavra).strip(), valor
            break
    candidatos = [numero(limpo)]
    if multiplicador > 1 and limpo.count(".") == 1 and "," not in limpo:
        candidatos.append(numero(limpo.replace(".", ",")))  # o ponto escrito como separador de decimais
    return [valor * multiplicador for valor in candidatos if valor is not None]


def conferir_pib(pib, per_capita, populacao):
    """Devolve None se o PIB bate com per capita × população, ou o motivo para rejeitar."""
    estimado = per_capita * populacao
    razao = pib / estimado
    if abs(razao - 1) <= TOLERANCIA:
        return None
    return f"não bate com PIB per capita × população: {razao:.3g} vezes o esperado"


def avaliar(estado, populacao):
    """Devolve a linha aceita (ou None) e a lista de rejeições daquele estado."""
    rejeitados = []
    per_capita = Decimal(estado["pib_per_capita"])
    if not PER_CAPITA_MINIMO <= per_capita <= PER_CAPITA_MAXIMO:
        rejeitados.append({"sigla": estado["sigla"], "coluna": "pib_per_capita", "texto": estado["pib_per_capita"],
                           "motivo": f"fora da faixa de {PER_CAPITA_MINIMO} a {PER_CAPITA_MAXIMO} reais"})
        rejeitados.append({"sigla": estado["sigla"], "coluna": "pib", "texto": estado["pib"],
                           "motivo": "sem PIB per capita aceito, não há como conferir"})
        return None, rejeitados
    opcoes = leituras(estado["pib"])
    pib, motivo = None, "o texto não tem número"
    for valor in opcoes:  # fica a primeira leitura que bate com a conferência
        motivo = conferir_pib(valor, per_capita, populacao)
        if motivo is None:
            pib = valor
            break
    if pib is None:
        rejeitados.append({"sigla": estado["sigla"], "coluna": "pib", "texto": estado["pib"], "motivo": motivo})
        return None, rejeitados
    linha = {coluna: estado.get(coluna) for coluna in COLUNAS}
    return {**linha, "populacao": populacao, "pib_reais": pib.quantize(Decimal(1))}, rejeitados


def ler_csv(caminho):
    with Path(caminho).open(newline="", encoding="utf-8") as arquivo:
        return list(csv.DictReader(arquivo))


def gravar_csv(caminho, colunas, linhas):
    with Path(caminho).open("w", newline="", encoding="utf-8") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(linhas)


def main():
    populacao = {linha["sigla"]: int(linha["populacao"]) for linha in ler_csv("dados/estados.csv")}
    aceitos, rejeitados = [], []
    for estado in ler_csv("dados/numeros.csv"):
        linha, motivos = avaliar(estado, populacao[estado["sigla"]])
        rejeitados += motivos
        aceitos.append(linha or {**{c: estado.get(c) for c in COLUNAS}, "populacao": populacao[estado["sigla"]], "pib_reais": None})
    gravar_csv("dados/pib.csv", COLUNAS, aceitos)
    gravar_csv("dados/rejeitados.csv", COLUNAS_REJEITADOS, rejeitados)
    com_pib = [linha for linha in aceitos if linha["pib_reais"] is not None]
    soma = sum(Decimal(linha["pib_reais"]) for linha in com_pib)
    registro.info("PIB aceito em %s de %s estados; %s rejeições em dados/rejeitados.csv", len(com_pib), len(aceitos), len(rejeitados))
    registro.info("soma do PIB aceito: R$ %s trilhões", f"{soma / Decimal(10) ** 12:.2f}")


if __name__ == "__main__":
    main()
