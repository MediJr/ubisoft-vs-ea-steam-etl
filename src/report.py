"""Production des éléments du rapport à partir de la base DuckDB.

- docs/livraison/figures/<langue>/*.png : les graphiques du rapport, en français (fr) et en anglais (en) ;
- docs/livraison/resultats.md          : les résultats bruts de chaque requête SQL, régénérés à chaque exécution.

Le rapport d'analyse (rédigé) s'appuie sur ces résultats : n'importe qui peut relancer
le pipeline et vérifier que les chiffres cités correspondent bien aux données.

Exécution seule :  python -m src.report
"""

import logging
from pathlib import Path

import duckdb
import matplotlib

matplotlib.use("Agg")  # rendu dans des fichiers, sans ouvrir de fenêtre
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from src import config  # noqa: E402

logger = logging.getLogger(__name__)

SQL_DIR = config.PROJECT_DIR / "sql"
DELIVERY_DIR = config.PROJECT_DIR / "docs" / "livraison"
FIGURES_DIR = DELIVERY_DIR / "figures"
LANGUAGES = ("fr", "en")

# Une couleur fixe par éditeur, dans tous les graphiques (palette validée pour le daltonisme).
COLORS = {"Ubisoft": "#2a78d6", "Electronic Arts": "#eb6834"}
INK, INK_SECONDARY, GRID, SURFACE = "#0b0b0b", "#52514e", "#e4e3df", "#fcfcfb"

# Tous les textes des graphiques, dans chaque langue : le code de tracé reste unique.
LABELS = {
    "fr": {
        "percent": "{:.0f} %", "thousands": " ",
        "q1_title": "Q1 · Satisfaction des joueurs par éditeur",
        "q1_x": "Part d'avis positifs sur Steam (un point = un jeu)",
        "median": "médiane {:.0f} %",
        "trend_title": "Q1 · Évolution de la satisfaction depuis 2020",
        "trend_y": "Avis positifs (moyenne glissante 3 mois)",
        "q2_title": "Q2 · Prix et satisfaction",
        "q2_x": "Prix catalogue actuel, hors promotion (€)", "q2_y": "Avis positifs",
        "q2_client": "prix envisagé par le client (25 €)",
        "q3_title": "Q3 · Les jeux gardent-ils leurs joueurs ?",
        "q3_x": "Ancienneté sur Steam (années)", "q3_y": "Joueurs connectés (échelle log)",
        "q4_title": "Q4 · Les francophones sont-ils plus sévères ?",
        "q4_x": "Avis positifs, toutes langues", "q4_y": "Avis positifs, en français",
        "q4_same": "même avis", "q4_note": "sous la diagonale : francophones plus sévères",
    },
    "en": {
        "percent": "{:.0f}%", "thousands": ",",
        "q1_title": "Q1 · Player satisfaction by publisher",
        "q1_x": "Share of positive Steam reviews (one dot = one game)",
        "median": "median {:.0f}%",
        "trend_title": "Q1 · Satisfaction trend since 2020",
        "trend_y": "Positive reviews (3-month rolling)",
        "q2_title": "Q2 · Price and satisfaction",
        "q2_x": "Current list price, excluding discounts (€)", "q2_y": "Positive reviews",
        "q2_client": "client's planned price (€25)",
        "q3_title": "Q3 · Do games keep their players?",
        "q3_x": "Years on Steam", "q3_y": "Concurrent players (log scale)",
        "q4_title": "Q4 · Are French-speaking players harsher?",
        "q4_x": "Positive reviews, all languages", "q4_y": "Positive reviews, in French",
        "q4_same": "same opinion", "q4_note": "below the diagonal: French speakers are harsher",
    },
}

plt.rcParams.update({
    "figure.facecolor": SURFACE, "axes.facecolor": SURFACE, "savefig.facecolor": SURFACE,
    "axes.edgecolor": GRID, "axes.labelcolor": INK_SECONDARY, "axes.titlecolor": INK,
    "axes.titlesize": 13, "axes.titleweight": "bold", "axes.titlelocation": "left",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "xtick.color": INK_SECONDARY, "ytick.color": INK_SECONDARY,
    "font.size": 10, "legend.frameon": False,
})


def _query(connection: duckdb.DuckDBPyConnection, sql: str) -> pd.DataFrame:
    return connection.execute(sql).df()


def _save(fig: plt.Figure, folder: Path, name: str) -> None:
    fig.tight_layout()
    fig.savefig(folder / name, dpi=150)
    plt.close(fig)


def _percent_axis(axis, text: dict) -> None:
    # Graduations « rondes » uniquement (pas de 2,5) : sinon l'arrondi afficherait deux fois la même valeur.
    axis.set_major_locator(matplotlib.ticker.MaxNLocator(nbins=6, steps=[1, 2, 5, 10]))
    axis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: text["percent"].format(v)))


def figure_satisfaction(data: pd.DataFrame, text: dict, folder: Path) -> None:
    """Q1 : la répartition des taux d'avis positifs, jeu par jeu, pour chaque éditeur."""
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for position, (publisher, color) in enumerate(COLORS.items()):
        values = data.loc[data.publisher_group == publisher, "taux"]
        if values.empty:
            continue
        ax.boxplot(values, positions=[position], vert=False, widths=0.5, showfliers=False,
                   medianprops={"color": INK, "linewidth": 2}, boxprops={"color": color},
                   whiskerprops={"color": color}, capprops={"color": color})
        jitter = position + (pd.Series(range(len(values))) % 7 - 3) * 0.04
        ax.scatter(values, jitter, s=22, color=color, alpha=0.7, edgecolor=SURFACE, linewidth=1, zorder=3)
        ax.annotate(text["median"].format(values.median()), (values.median(), position + 0.33),
                    ha="center", fontsize=9, color=INK)
    ax.set_yticks(range(len(COLORS)), list(COLORS))
    ax.grid(axis="y", visible=False)
    _percent_axis(ax.xaxis, text)
    ax.set_xlabel(text["q1_x"])
    ax.set_title(text["q1_title"])
    _save(fig, folder, "q1_satisfaction_par_editeur.png")


def figure_trend(data: pd.DataFrame, text: dict, folder: Path) -> None:
    """Q1 : l'évolution mensuelle de la part d'avis positifs, tous jeux confondus."""
    fig, ax = plt.subplots(figsize=(8, 3.8))
    for publisher, color in COLORS.items():
        series = data[data.publisher_group == publisher].set_index("month")
        if series.empty:
            continue
        # Moyenne glissante sur 3 mois : elle lisse les pics ponctuels sans masquer les tendances.
        rate = 100 * series["up"].rolling(3).sum() / series["total"].rolling(3).sum()
        ax.plot(series.index, rate, color=color, linewidth=2, label=publisher)
    _percent_axis(ax.yaxis, text)
    ax.set_ylabel(text["trend_y"])
    ax.set_title(text["trend_title"])
    ax.legend(loc="lower left")
    _save(fig, folder, "q1_evolution_mensuelle.png")


def figure_price(data: pd.DataFrame, text: dict, folder: Path) -> None:
    """Q2 : le prix catalogue face à la satisfaction."""
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for publisher, color in COLORS.items():
        subset = data[data.publisher_group == publisher]
        ax.scatter(subset.prix, subset.taux, s=40, color=color, alpha=0.8,
                   edgecolor=SURFACE, linewidth=1.5, label=publisher)
    ax.axvline(25, color=INK_SECONDARY, linewidth=1, linestyle="--")
    ax.annotate(text["q2_client"], (25, ax.get_ylim()[0]), xytext=(4, 6),
                textcoords="offset points", fontsize=9, color=INK_SECONDARY)
    _percent_axis(ax.yaxis, text)
    ax.set_xlabel(text["q2_x"])
    ax.set_ylabel(text["q2_y"])
    ax.set_title(text["q2_title"])
    ax.legend(loc="lower right")
    _save(fig, folder, "q2_prix_satisfaction.png")


def figure_longevity(data: pd.DataFrame, text: dict, folder: Path) -> None:
    """Q3 : l'ancienneté sur Steam face à la fréquentation actuelle."""
    fig, ax = plt.subplots(figsize=(8, 4.2))
    for publisher, color in COLORS.items():
        subset = data[data.publisher_group == publisher]
        ax.scatter(subset.annees, subset.joueurs, s=40, color=color, alpha=0.8,
                   edgecolor=SURFACE, linewidth=1.5, label=publisher)
    # Échelle logarithmique : la fréquentation va de quelques joueurs à plus de 100 000.
    ax.set_yscale("log")
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
        lambda v, _: f"{v:,.0f}".replace(",", text["thousands"])))
    ax.set_xlabel(text["q3_x"])
    ax.set_ylabel(text["q3_y"])
    ax.set_title(text["q3_title"])
    ax.legend(loc="upper right")
    _save(fig, folder, "q3_longevite.png")


def figure_french(data: pd.DataFrame, text: dict, folder: Path) -> None:
    """Q4 : la satisfaction des francophones face à celle de l'ensemble des joueurs."""
    fig, ax = plt.subplots(figsize=(6, 5.5))
    low = min(data.tous.min(), data.fr.min()) - 3
    ax.plot([low, 100], [low, 100], color=INK_SECONDARY, linewidth=1, linestyle="--")
    ax.annotate(text["q4_same"], (low + 2, low + 4), fontsize=9, color=INK_SECONDARY, rotation=40)
    for publisher, color in COLORS.items():
        subset = data[data.publisher_group == publisher]
        ax.scatter(subset.tous, subset.fr, s=40, color=color, alpha=0.8,
                   edgecolor=SURFACE, linewidth=1.5, label=publisher)
    ax.set_xlim(low, 100)
    ax.set_ylim(low, 100)
    _percent_axis(ax.xaxis, text)
    _percent_axis(ax.yaxis, text)
    ax.set_xlabel(text["q4_x"])
    ax.set_ylabel(text["q4_y"])
    ax.set_title(text["q4_title"])
    ax.text(0.98, 0.04, text["q4_note"], transform=ax.transAxes, ha="right", fontsize=9, color=INK_SECONDARY)
    ax.legend(loc="upper left")
    _save(fig, folder, "q4_francophones.png")


def _figure_data(connection) -> dict[str, pd.DataFrame]:
    """Données des graphiques, lues une seule fois pour toutes les langues."""
    return {
        "satisfaction": _query(connection, """
            SELECT g.publisher_group, 100 * r.positive_rate::DOUBLE AS taux
            FROM games g JOIN review_summary r USING (app_id) WHERE r.language = 'all'
        """),
        "trend": _query(connection, """
            SELECT g.publisher_group, m.month,
                   SUM(m.reviews_up)::DOUBLE AS up, SUM(m.reviews_up + m.reviews_down)::DOUBLE AS total
            FROM reviews_monthly m JOIN games g USING (app_id)
            WHERE m.month >= DATE '2020-01-01' AND m.month < date_trunc('month', g.extracted_on)
            GROUP BY ALL ORDER BY m.month
        """),
        "price": _query(connection, """
            SELECT g.publisher_group, g.price_initial_eur::DOUBLE AS prix, 100 * r.positive_rate::DOUBLE AS taux
            FROM games g JOIN review_summary r USING (app_id)
            WHERE r.language = 'all' AND g.price_initial_eur IS NOT NULL
        """),
        "longevity": _query(connection, """
            SELECT g.publisher_group, g.years_on_steam::DOUBLE AS annees, p.current_players AS joueurs
            FROM games g JOIN player_snapshot p USING (app_id)
            WHERE g.years_on_steam IS NOT NULL AND p.current_players > 0
        """),
        "french": _query(connection, """
            SELECT g.publisher_group, 100 * tous.positive_rate::DOUBLE AS tous, 100 * fr.positive_rate::DOUBLE AS fr
            FROM games g
            JOIN review_summary tous ON tous.app_id = g.app_id AND tous.language = 'all'
            JOIN review_summary fr   ON fr.app_id   = g.app_id AND fr.language   = 'french'
            WHERE fr.total_reviews >= 100
        """),
    }


def _markdown_table(frame: pd.DataFrame) -> str:
    """Convertit un tableau pandas en tableau Markdown (sans dépendance supplémentaire)."""
    def cell(value) -> str:
        return "" if pd.isna(value) else str(value)
    header = "| " + " | ".join(frame.columns) + " |"
    separator = "|" + "---|" * len(frame.columns)
    rows = ["| " + " | ".join(cell(v) for v in row) + " |" for row in frame.itertuples(index=False)]
    return "\n".join([header, separator, *rows])


def write_results(connection) -> None:
    """Exécute chaque requête de sql/ et consigne les résultats dans resultats.md."""
    run_date = connection.execute("SELECT MAX(extracted_on) FROM games").fetchone()[0]
    sections = [
        "# Résultats des requêtes SQL",
        "",
        f"> Fichier **généré automatiquement** par `python -m src.report`. Données extraites le {run_date}.",
        "> Ne pas modifier à la main : relancer le pipeline pour le régénérer.",
    ]
    for path in sorted(SQL_DIR.glob("*.sql")):
        if path.name == "00_schema.sql":
            continue
        sections += ["", f"## `{path.name}`", "", _markdown_table(_query(connection, path.read_text(encoding="utf-8")))]
    (DELIVERY_DIR / "resultats.md").write_text("\n".join(sections) + "\n", encoding="utf-8")


def build_figures() -> None:
    with duckdb.connect(str(config.DATABASE_PATH), read_only=True) as connection:
        data = _figure_data(connection)
        for language in LANGUAGES:
            folder = FIGURES_DIR / language
            folder.mkdir(parents=True, exist_ok=True)
            text = LABELS[language]
            figure_satisfaction(data["satisfaction"], text, folder)
            figure_trend(data["trend"], text, folder)
            figure_price(data["price"], text, folder)
            figure_longevity(data["longevity"], text, folder)
            figure_french(data["french"], text, folder)
        write_results(connection)
    logger.info("Graphiques (%s) et résultats écrits dans %s", ", ".join(LANGUAGES), DELIVERY_DIR)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
    build_figures()
