-- Schéma de la base analytique (DuckDB).
-- Les clés primaires garantissent l'absence de doublons : une insertion en double échoue
-- au lieu de fausser silencieusement les résultats (critère d'acceptation C2).

DROP TABLE IF EXISTS player_snapshot;
DROP TABLE IF EXISTS reviews_monthly;
DROP TABLE IF EXISTS review_summary;
DROP TABLE IF EXISTS exclusions;
DROP TABLE IF EXISTS games;

-- Un jeu retenu dans le périmètre.
CREATE TABLE games (
    app_id                INTEGER PRIMARY KEY,
    name                  VARCHAR NOT NULL,
    publisher_group       VARCHAR NOT NULL,   -- « Ubisoft » ou « Electronic Arts »
    publishers            VARCHAR,            -- éditeurs déclarés sur Steam
    developers            VARCHAR,
    is_free               BOOLEAN NOT NULL,
    price_initial_eur     DECIMAL(6, 2),      -- prix hors promotion, en euros
    price_final_eur       DECIMAL(6, 2),      -- prix payé le jour de l'extraction
    discount_percent      INTEGER,
    steam_release_date    DATE,               -- date de sortie SUR STEAM (pas forcément la sortie mondiale)
    years_on_steam        DECIMAL(4, 1),
    genres                VARCHAR,
    metacritic_score      INTEGER,
    owners_estimate_low   BIGINT,             -- estimation SteamSpy (fourchette basse)
    owners_estimate_high  BIGINT,
    extracted_on          DATE NOT NULL
);

-- Synthèse des avis, toutes langues (« all ») et en français (« french »).
CREATE TABLE review_summary (
    app_id             INTEGER NOT NULL REFERENCES games (app_id),
    language           VARCHAR NOT NULL,
    total_reviews      INTEGER NOT NULL,
    total_positive     INTEGER NOT NULL,
    total_negative     INTEGER NOT NULL,
    positive_rate      DECIMAL(5, 4),         -- NULL s'il n'y a aucun avis
    review_score_desc  VARCHAR,
    PRIMARY KEY (app_id, language)
);

-- Nombre d'avis positifs et négatifs publiés chaque mois.
CREATE TABLE reviews_monthly (
    app_id        INTEGER NOT NULL REFERENCES games (app_id),
    month         DATE NOT NULL,              -- premier jour du mois
    reviews_up    INTEGER NOT NULL,
    reviews_down  INTEGER NOT NULL,
    PRIMARY KEY (app_id, month)
);

-- Fréquentation le jour de l'extraction.
CREATE TABLE player_snapshot (
    app_id                  INTEGER NOT NULL REFERENCES games (app_id),
    snapshot_date           DATE NOT NULL,
    current_players         INTEGER,          -- joueurs connectés au moment de l'appel
    peak_players_yesterday  INTEGER,          -- pic de joueurs simultanés la veille (SteamSpy)
    PRIMARY KEY (app_id, snapshot_date)
);

-- Jeux candidats écartés, avec le motif : la transparence sur le périmètre.
CREATE TABLE exclusions (
    app_id              INTEGER NOT NULL,
    publisher_searched  VARCHAR NOT NULL,
    reason              VARCHAR NOT NULL,
    PRIMARY KEY (app_id, publisher_searched)
);
