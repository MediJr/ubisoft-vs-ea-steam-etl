# Changelog

Toutes les évolutions notables du projet sont consignées ici.
Format inspiré de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/). Le projet suit le [versionnage sémantique](https://semver.org/lang/fr/).

## [1.0.0] - 2026-10-22

Première version livrée au client.

### Ajouté
- Dossier de mission : brief client, compte rendu de cadrage, cahier des charges
- Pipeline ETL complet, exécutable en une commande (`python -m src.pipeline`)
  - **Extract** : 6 sources Steam / SteamSpy, extraction en deux passes, cache de reprise, écriture atomique
  - **Transform** : périmètre, typage, table des exclusions motivées
  - **Load** : schéma DuckDB avec clés primaires, chargement complet dans une transaction
  - Option `--run-date` pour rejouer un lot brut sans appeler les API
- 10 requêtes SQL d'analyse (Q1 à Q4) et une requête de contrôle de recette
- 5 graphiques, générés en français et en anglais, et un fichier de résultats généré automatiquement
- Rapport d'ingénierie des données en LaTeX, en français et en anglais (19 pages chacun, PDF dans `docs/livraison/`)
- README en anglais (page d'accueil) et en français, dictionnaire de données, PV de recette
- Décisions d'architecture : ADR 001 (stack), ADR 002 (extraction), ADR 003 (source de fréquentation)

### Corrigé (pendant le développement)
- Dates de sortie non reconnues : Steam écrit « aout » sans accent
- Mesure de fréquentation : SteamSpy renvoie 0 pour les jeux récents (voir ADR 003)
- Fenêtre de « lancement » (Q1b) : exclusion des jeux dont les premiers avis ne datent pas de la sortie sur Steam
