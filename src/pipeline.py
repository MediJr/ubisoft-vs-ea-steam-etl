"""Point d'entrée du pipeline : Extract → Transform → Load → Rapport (graphiques).

Utilisation :
    python -m src.pipeline                        # extraction du jour, puis tout le reste
    python -m src.pipeline --run-date 2026-10-21  # rejoue un lot brut existant, sans appeler les API
"""

import argparse
import logging
import time
from datetime import date

from src import config
from src.extract import extract
from src.load import load
from src.report import build_figures
from src.transform import transform

logger = logging.getLogger("pipeline")


def main() -> None:
    parser = argparse.ArgumentParser(description="Pipeline ETL Steam : Ubisoft vs Electronic Arts")
    parser.add_argument("--run-date", type=date.fromisoformat,
                        help="rejouer un lot brut existant (AAAA-MM-JJ) au lieu d'extraire")
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s")
    started = time.perf_counter()

    if args.run_date:
        run_dir = config.RAW_DIR / args.run_date.isoformat()
        if not (run_dir / "manifest.json").exists():
            parser.error(f"aucun lot brut complet dans {run_dir}")
        logger.info("Rejeu du lot brut %s (aucun appel aux API)", run_dir.name)
    else:
        run_dir = extract()

    tables = transform(run_dir)
    load(tables)
    build_figures()
    logger.info("Pipeline terminé en %.0f s", time.perf_counter() - started)


if __name__ == "__main__":
    main()
