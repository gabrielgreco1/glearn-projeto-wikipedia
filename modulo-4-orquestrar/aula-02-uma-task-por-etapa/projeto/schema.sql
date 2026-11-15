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

-- Colunas que vieram depois da primeira carga. ADD COLUMN IF NOT EXISTS muda a tabela que já existe, sem apagar nada.
ALTER TABLE estados ADD COLUMN IF NOT EXISTS hash_conteudo char(64);
ALTER TABLE estados ADD COLUMN IF NOT EXISTS carregado_em timestamptz NOT NULL DEFAULT now();

-- Uma linha por carga: quantas linhas vieram, o que aconteceu com cada uma e a soma que confere o resultado.
-- O CHECK é a conta que tem de fechar: o banco recusa um relatório que não fecha.
CREATE TABLE IF NOT EXISTS cargas (
    id          bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    feita_em    timestamptz NOT NULL DEFAULT now(),
    tentados    integer NOT NULL,
    inseridos   integer NOT NULL,
    atualizados integer NOT NULL,
    iguais      integer NOT NULL,
    populacao   bigint NOT NULL,
    revisao_ate timestamptz NOT NULL,
    CHECK (tentados = inseridos + atualizados + iguais)
);

-- A gold: a resposta por região, trocada inteira a cada carga.
CREATE TABLE IF NOT EXISTS regioes (
    regiao          text PRIMARY KEY,
    estados         integer NOT NULL,
    populacao       bigint NOT NULL,
    estados_com_pib integer NOT NULL,
    pib_bilhoes     double precision,
    pib_por_pessoa  double precision
);
