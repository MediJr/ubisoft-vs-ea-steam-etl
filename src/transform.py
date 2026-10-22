"""Étape T du pipeline : des fichiers bruts aux tables propres.

On y applique les règles du cahier des charges :
- périmètre : jeux sortis, publiés par l'éditeur recherché, au moins MIN_REVIEWS avis ;
- plafond : les MAX_GAMES_PER_PUBLISHER jeux les plus commentés par éditeur ;
- typage : dates, montants en euros, entiers ;
- traçabilité : chaque jeu écarté figure dans la table `exclusions`, avec son motif.
"""

import json
import logging
import re
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd

from src import config

logger = logging.getLogger(__name__)

# Steam renvoie les dates dans la langue demandée (« 12 janv. 2023 »).
# Constat sur les données réelles : Steam écrit « aout » SANS accent. On accepte les deux graphies.
_FRENCH_MONTHS = {
    "janv": 1, "févr": 2, "fevr": 2, "mars": 3, "avr": 4, "mai": 5, "juin": 6,
    "juil": 7, "août": 8, "aout": 8, "sept": 9, "oct": 10, "nov": 11, "déc": 12, "dec": 12,
}
_DATE_PATTERN = re.compile(r"(\d{1,2})\s+([a-zéû]+)\.?\s+(\d{4})", re.IGNORECASE)


def parse_release_date(text: str | None) -> date | None:
    """Convertit « 12 janv. 2023 » en date. Renvoie None si le format est inconnu (ex. « T1 2027 »)."""
    match = _DATE_PATTERN.search(text or "")
    if not match:
        return None
    day, month_name, year = match.groups()
    month = _FRENCH_MONTHS.get(month_name.lower().rstrip("."))
    return date(int(year), month, int(day)) if month else None


def parse_owners(text: str | None) -> tuple[int | None, int | None]:
    """Convertit la fourchette SteamSpy « 1,000,000 .. 2,000,000 » en (1000000, 2000000)."""
    numbers = [int(part.replace(",", "").strip()) for part in (text or "").split("..") if part.strip()]
    return (numbers[0], numbers[1]) if len(numbers) == 2 else (None, None)


def _read_raw(run_dir: Path, source: str, app_id: int) -> dict | None:
    path = run_dir / source / f"{app_id}.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def _matching_publisher(publishers: list[str], searched: str) -> bool:
    """Vrai si l'éditeur recherché figure parmi les éditeurs réels du jeu.

    La recherche Steam est large : un jeu peut remonter alors qu'un autre éditeur le publie.
    """
    return any(searched.lower() in publisher.lower() for publisher in publishers)


def _euros(cents: int | None) -> float | None:
    return round(cents / 100, 2) if cents is not None else None


def build_games(run_dir: Path, manifest: dict) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Construit la table des jeux retenus et la table des exclusions."""
    run_date = date.fromisoformat(manifest["run_date"])
    games, exclusions = [], []

    for publisher, lists in manifest["publishers"].items():
        for app_id in lists["selected"]:
            details = (_read_raw(run_dir, "app_details", app_id) or {}).get(str(app_id), {})
            data = details.get("data", {}) if details.get("success") else {}
            reason = None
            if not data:
                reason = "fiche Steam indisponible"
            elif data.get("type") != "game":
                reason = f"type « {data.get('type')} » (pas un jeu)"
            elif data.get("release_date", {}).get("coming_soon"):
                reason = "pas encore sorti"
            elif not _matching_publisher(data.get("publishers", []), publisher):
                reason = f"publié par {', '.join(data.get('publishers', [])) or 'inconnu'}"
            if reason:
                exclusions.append({"app_id": app_id, "publisher_searched": publisher, "reason": reason})
                continue

            price = data.get("price_overview") or {}
            spy = _read_raw(run_dir, "steamspy", app_id) or {}
            owners_low, owners_high = parse_owners(spy.get("owners"))
            release = parse_release_date(data.get("release_date", {}).get("date"))
            summary = (_read_raw(run_dir, "reviews_all", app_id) or {}).get("query_summary", {})
            games.append({
                "app_id": app_id,
                "name": data.get("name"),
                "publisher_group": publisher,
                "publishers": ", ".join(data.get("publishers", [])),
                "developers": ", ".join(data.get("developers", [])),
                "is_free": bool(data.get("is_free")),
                # Un jeu gratuit n'a pas de bloc price_overview : son prix vaut 0 €.
                "price_initial_eur": _euros(price.get("initial")) if price else (0.0 if data.get("is_free") else None),
                "price_final_eur": _euros(price.get("final")) if price else (0.0 if data.get("is_free") else None),
                "discount_percent": price.get("discount_percent", 0),
                "steam_release_date": release,
                "years_on_steam": round((run_date - release).days / 365.25, 1) if release else None,
                "genres": ", ".join(g["description"] for g in data.get("genres", [])),
                "metacritic_score": (data.get("metacritic") or {}).get("score"),
                "owners_estimate_low": owners_low,
                "owners_estimate_high": owners_high,
                "total_reviews": summary.get("total_reviews", 0),
                "extracted_on": run_date,
            })

    games_df = pd.DataFrame(games)
    exclusions_df = pd.DataFrame(exclusions, columns=["app_id", "publisher_searched", "reason"])

    # Doublon possible si un jeu est co-publié par les deux éditeurs : on garde la première occurrence.
    duplicated = games_df.duplicated("app_id")
    if duplicated.any():
        logger.warning("%d jeu(x) en double ignoré(s)", duplicated.sum())
        games_df = games_df[~duplicated]

    # Plafond du cahier des charges : les jeux les plus commentés de chaque éditeur.
    ranked = games_df.sort_values("total_reviews", ascending=False)
    kept = ranked.groupby("publisher_group", group_keys=False).head(config.MAX_GAMES_PER_PUBLISHER)
    over_cap = ranked.drop(kept.index)
    exclusions_df = pd.concat([exclusions_df, pd.DataFrame({
        "app_id": over_cap["app_id"],
        "publisher_searched": over_cap["publisher_group"],
        "reason": f"hors plafond ({config.MAX_GAMES_PER_PUBLISHER} jeux les plus commentés par éditeur)",
    })], ignore_index=True)

    games_df = kept.drop(columns="total_reviews").reset_index(drop=True)
    return games_df, exclusions_df


def build_review_summary(run_dir: Path, app_ids: list[int]) -> pd.DataFrame:
    rows = []
    for app_id in app_ids:
        for language in ("all", "french"):
            summary = (_read_raw(run_dir, f"reviews_{language}", app_id) or {}).get("query_summary")
            if not summary:
                continue
            total = summary.get("total_reviews", 0)
            rows.append({
                "app_id": app_id,
                "language": language,
                "total_reviews": total,
                "total_positive": summary.get("total_positive", 0),
                "total_negative": summary.get("total_negative", 0),
                # NULL plutôt que 0 quand il n'y a aucun avis : 0 % voudrait dire « tous négatifs ».
                "positive_rate": round(summary["total_positive"] / total, 4) if total else None,
                "review_score_desc": summary.get("review_score_desc"),
            })
    return pd.DataFrame(rows)


def build_reviews_monthly(run_dir: Path, app_ids: list[int]) -> pd.DataFrame:
    rows = []
    for app_id in app_ids:
        results = (_read_raw(run_dir, "review_histogram", app_id) or {}).get("results", {})
        for point in results.get("rollups", []):
            rows.append({
                "app_id": app_id,
                # Steam fournit un horodatage Unix (secondes depuis 1970, en UTC).
                "month": datetime.fromtimestamp(point["date"], tz=timezone.utc).date().replace(day=1),
                "granularity": results.get("rollup_type", "month"),
                "reviews_up": point.get("recommendations_up", 0),
                "reviews_down": point.get("recommendations_down", 0),
            })
    monthly = pd.DataFrame(rows)
    # Si Steam renvoie un découpage par semaine, plusieurs points tombent dans le même mois : on les additionne.
    return (
        monthly.groupby(["app_id", "month"], as_index=False)
        .agg(reviews_up=("reviews_up", "sum"), reviews_down=("reviews_down", "sum"))
    )


def build_player_snapshot(run_dir: Path, app_ids: list[int], run_date: date) -> pd.DataFrame:
    rows = []
    for app_id in app_ids:
        current = (_read_raw(run_dir, "current_players", app_id) or {}).get("response", {})
        spy = _read_raw(run_dir, "steamspy", app_id) or {}
        rows.append({
            "app_id": app_id,
            "snapshot_date": run_date,
            "current_players": current.get("player_count") if current.get("result") == 1 else None,
            "peak_players_yesterday": spy.get("ccu"),
        })
    return pd.DataFrame(rows)


def transform(run_dir: Path) -> dict[str, pd.DataFrame]:
    """Transforme un lot brut en tables prêtes à charger."""
    manifest = json.loads((run_dir / "manifest.json").read_text(encoding="utf-8"))
    run_date = date.fromisoformat(manifest["run_date"])

    games, exclusions = build_games(run_dir, manifest)
    app_ids = games["app_id"].tolist()
    tables = {
        "games": games,
        "review_summary": build_review_summary(run_dir, app_ids),
        "reviews_monthly": build_reviews_monthly(run_dir, app_ids),
        "player_snapshot": build_player_snapshot(run_dir, app_ids, run_date),
        "exclusions": exclusions,
    }
    for name, table in tables.items():
        logger.info("Table %-16s : %6d lignes", name, len(table))
    return tables
