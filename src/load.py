"""Étape L du pipeline : chargement des tables dans DuckDB.

Stratégie de rechargement complet (ADR 001) : on recrée le schéma, puis on insère toutes les tables,
le tout dans UNE transaction. Si une étape échoue, rien n'est validé et la base garde
son état précédent. On n'obtient jamais une base à moitié chargée.
"""

import logging

import duckdb
import pandas as pd

from src import config

logger = logging.getLogger(__name__)

SCHEMA_PATH = config.PROJECT_DIR / "sql" / "00_schema.sql"

# Ordre d'insertion : `games` d'abord, car les autres tables y font référence (clés étrangères).
LOAD_ORDER = ["games", "review_summary", "reviews_monthly", "player_snapshot", "exclusions"]


def load(tables: dict[str, pd.DataFrame]) -> None:
    config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with duckdb.connect(str(config.DATABASE_PATH)) as connection:
        connection.execute("BEGIN TRANSACTION")
        try:
            connection.execute(SCHEMA_PATH.read_text(encoding="utf-8"))
            for name in LOAD_ORDER:
                connection.register("incoming", tables[name])
                # BY NAME : les colonnes sont associées par leur nom, pas par leur position.
                connection.execute(f"INSERT INTO {name} BY NAME SELECT * FROM incoming")
                connection.unregister("incoming")
            connection.execute("COMMIT")
        except Exception:
            connection.execute("ROLLBACK")
            raise
    logger.info("Base chargée : %s", config.DATABASE_PATH)
