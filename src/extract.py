"""Étape E du pipeline : extraction des données brutes depuis Steam et SteamSpy.

Principe : on enregistre les réponses des API **telles quelles** dans data/raw/<date>/.
Aucun nettoyage ici. Si la transformation contient un bug, on la corrige et on la
relance sans réinterroger les API : la couche brute est notre filet de sécurité.

L'extraction se fait en deux passes, pour limiter le nombre d'appels :
1. Passe légère : pour chaque jeu candidat, on lit seulement la synthèse des avis.
2. Passe détaillée : uniquement pour les jeux d'au moins MIN_REVIEWS avis.

Exécution seule (utile pour tester) :  python -m src.extract
"""

import json
import logging
import re
import time
from datetime import date, datetime, timezone
from pathlib import Path

import requests

from src import config

logger = logging.getLogger(__name__)

SEARCH_URL = "https://store.steampowered.com/search/results/"
APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"
REVIEWS_URL = "https://store.steampowered.com/appreviews/{app_id}"
REVIEW_HISTOGRAM_URL = "https://store.steampowered.com/appreviewhistogram/{app_id}"
CURRENT_PLAYERS_URL = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1/"
STEAMSPY_URL = "https://steamspy.com/api.php"

# Une session réutilise la même connexion réseau pour tous les appels : c'est plus rapide.
_session = requests.Session()
_session.headers.update({"User-Agent": config.USER_AGENT})


# --- Outils réseau ---------------------------------------------------------

def _http_get(url: str, params: dict) -> requests.Response:
    """GET poli : une pause avant chaque appel, et quelques réessais en cas d'erreur temporaire.

    Version volontairement simple. La gestion des erreurs sera approfondie au projet 1.
    """
    for attempt in range(1, config.MAX_RETRIES + 1):
        time.sleep(config.REQUEST_PAUSE_SECONDS)
        try:
            response = _session.get(url, params=params, timeout=config.REQUEST_TIMEOUT_SECONDS)
            # 429 = « trop de requêtes », 5xx = erreur du serveur : on peut réessayer.
            if response.status_code == 429 or response.status_code >= 500:
                raise requests.HTTPError(f"HTTP {response.status_code}")
            response.raise_for_status()
            return response
        except requests.RequestException as error:
            if attempt == config.MAX_RETRIES:
                raise
            wait = 10 * attempt  # on attend de plus en plus longtemps : 10 s, 20 s…
            logger.warning("Échec (%s) sur %s, nouvel essai dans %s s", error, url, wait)
            time.sleep(wait)
    raise RuntimeError("inaccessible")  # pour les vérificateurs de type : la boucle renvoie ou lève


def _fetch_json(run_dir: Path, source: str, key: str, url: str, params: dict) -> dict:
    """Renvoie la réponse JSON d'une API en la mettant en cache dans data/raw/.

    Si le fichier brut existe déjà pour cette exécution, on le relit au lieu de rappeler l'API.
    On peut ainsi relancer l'extraction après une interruption sans tout recommencer.
    """
    path = run_dir / source / f"{key}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))

    payload = _http_get(url, params).json()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Écriture atomique : on écrit dans un fichier temporaire, puis on le renomme.
    # Si le programme est interrompu en pleine écriture, le cache ne contient jamais
    # de fichier à moitié écrit (le renommage est instantané).
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(path)
    return payload


# --- Découverte des jeux ---------------------------------------------------

# Dans le HTML de la recherche Steam, chaque jeu porte un attribut data-ds-appid="123456".
_APP_ID_PATTERN = re.compile(r'data-ds-appid="(\d+)"')


def discover_app_ids(run_dir: Path, publisher: str) -> list[int]:
    """Liste les identifiants Steam (app_id) des jeux d'un éditeur, par ordre de pertinence Steam."""
    app_ids: list[int] = []
    page_size = 50
    start = 0
    while len(app_ids) < config.MAX_CANDIDATES_PER_PUBLISHER:
        payload = _fetch_json(
            run_dir,
            source="search",
            key=f"{publisher.lower().replace(' ', '_')}_{start:04d}",
            url=SEARCH_URL,
            params={
                "publisher": publisher,
                "category1": 998,  # 998 = « jeux » uniquement (pas de DLC ni de bande-son)
                "infinite": 1,     # renvoie du JSON contenant le HTML de la liste
                "start": start,
                "count": page_size,
                "cc": config.STEAM_COUNTRY,
            },
        )
        page_ids = [int(app_id) for app_id in _APP_ID_PATTERN.findall(payload.get("results_html", ""))]
        if not page_ids:
            break  # plus de résultats
        app_ids.extend(app_id for app_id in page_ids if app_id not in app_ids)
        start += page_size
        if start >= payload.get("total_count", 0):
            break
    return app_ids[: config.MAX_CANDIDATES_PER_PUBLISHER]


# --- Collecte par jeu ------------------------------------------------------

def _review_summary(run_dir: Path, app_id: int, language: str) -> dict:
    """Synthèse des avis d'un jeu.

    num_per_page=0 : on ne demande AUCUN avis individuel, seulement les totaux.
    Aucun pseudo ni identifiant de joueur n'est donc téléchargé (minimisation RGPD).
    """
    return _fetch_json(
        run_dir,
        source=f"reviews_{language}",
        key=str(app_id),
        url=REVIEWS_URL.format(app_id=app_id),
        params={"json": 1, "num_per_page": 0, "language": language, "purchase_type": "all"},
    )


def _collect_details(run_dir: Path, app_id: int) -> None:
    """Passe détaillée : toutes les autres sources pour un jeu retenu."""
    _fetch_json(run_dir, "app_details", str(app_id), APP_DETAILS_URL,
                {"appids": app_id, "cc": config.STEAM_COUNTRY, "l": config.STEAM_LANGUAGE})
    _review_summary(run_dir, app_id, language="french")
    _fetch_json(run_dir, "review_histogram", str(app_id),
                REVIEW_HISTOGRAM_URL.format(app_id=app_id), {"l": "english"})
    _fetch_json(run_dir, "current_players", str(app_id), CURRENT_PLAYERS_URL, {"appid": app_id})
    _fetch_json(run_dir, "steamspy", str(app_id), STEAMSPY_URL,
                {"request": "appdetails", "appid": app_id})


# --- Point d'entrée --------------------------------------------------------

def extract(run_date: date | None = None) -> Path:
    """Extrait toutes les données brutes et renvoie le dossier de l'exécution."""
    run_date = run_date or date.today()
    run_dir = config.RAW_DIR / run_date.isoformat()
    run_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Extraction vers %s", run_dir)

    manifest: dict = {"run_date": run_date.isoformat(), "publishers": {}}

    for publisher in config.PUBLISHERS:
        candidates = discover_app_ids(run_dir, publisher)
        logger.info("%s : %d jeux candidats", publisher, len(candidates))

        # Passe 1 : synthèse des avis, toutes langues confondues.
        selected = []
        for app_id in candidates:
            summary = _review_summary(run_dir, app_id, language="all").get("query_summary", {})
            if summary.get("total_reviews", 0) >= config.MIN_REVIEWS:
                selected.append(app_id)
        logger.info("%s : %d jeux avec au moins %d avis", publisher, len(selected), config.MIN_REVIEWS)

        # Passe 2 : détails, uniquement pour les jeux retenus.
        for position, app_id in enumerate(selected, start=1):
            _collect_details(run_dir, app_id)
            if position % 10 == 0:
                logger.info("%s : détails collectés pour %d / %d jeux", publisher, position, len(selected))

        manifest["publishers"][publisher] = {"candidates": candidates, "selected": selected}

    # Le manifeste décrit l'exécution : quand, quoi, combien. C'est la « carte d'identité » du lot brut.
    manifest["completed_at"] = datetime.now(timezone.utc).isoformat()
    (run_dir / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    logger.info("Extraction terminée")
    return run_dir


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    extract()
