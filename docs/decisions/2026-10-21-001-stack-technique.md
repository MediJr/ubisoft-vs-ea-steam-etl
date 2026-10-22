# ADR 001 : Stack technique du projet 0

- **Date :** 2026-10-21
- **Statut :** Acceptée

## Contexte

- Volume attendu : environ 100 jeux, quelques milliers de lignes au total. C'est très modeste.
- C'est le **niveau 0** du parcours : on veut isoler le concept d'ETL, sans complexité d'infrastructure.
- Le livrable doit être relançable facilement sur n'importe quel poste.

## Décision

| Besoin | Choix | Alternatives écartées |
|---|---|---|
| Base de données | **DuckDB** (fichier local) | PostgreSQL : demande un serveur ou Docker, ce sera la nouveauté du projet 1. SQLite : moins adapté aux requêtes analytiques. |
| Transformation | **pandas** | Polars : plus rapide, mais inutile à ce volume, et pandas est déjà connu de l'auteur |
| Appels HTTP | **requests** | httpx : utile pour l'asynchrone, sans intérêt ici |
| Environnement | **venv + pip + requirements.txt** | uv / Poetry : plus modernes, à introduire plus tard |
| Orchestration | **Aucune** (une commande) | Dagster / Airflow : réservés au projet 3 |

## Stratégie de chargement

**Rechargement complet** (*full refresh*) : à chaque exécution, les tables sont **remplacées** et non complétées.
C'est la façon la plus simple de garantir l'absence de doublons (critère C2). Le chargement **incrémental**
sera abordé au projet 2.

## Conséquences

- ✅ Zéro installation de serveur : `pip install` suffit
- ✅ Le fichier DuckDB est réutilisable directement par le client
- ⚠️ Le rechargement complet ne conserve pas d'historique : chaque exécution est un instantané
