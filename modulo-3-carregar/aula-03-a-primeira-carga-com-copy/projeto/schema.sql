-- As tabelas do projeto no Postgres. O banco.py roda este arquivo antes de cada carga:
-- IF NOT EXISTS cria só o que falta, então rodar de novo não muda nada.

CREATE TABLE IF NOT EXISTS estados (
    sigla           char(2) PRIMARY KEY CHECK (sigla ~ '^[A-Z]{2}$'),
    estado          text NOT NULL,
    regiao          text NOT NULL CHECK (regiao IN ('Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul')),
    municipios      integer CHECK (municipios > 0),
    area_km2        double precision NOT NULL CHECK (area_km2 > 0),
    populacao       bigint NOT NULL CHECK (populacao > 0),
    idh             double precision NOT NULL CHECK (idh BETWEEN 0 AND 1),
    pib_per_capita  double precision,
    ano_pib         smallint NOT NULL,
    pib_reais       double precision CHECK (pib_reais > 0),
    latitude        double precision,
    longitude       double precision,
    arquivo         text NOT NULL,
    revisao         bigint NOT NULL,
    revisao_em      timestamptz NOT NULL,
    sha256_ficha    char(64) NOT NULL,
    transformado_em timestamptz NOT NULL
);
