# Résultats des requêtes SQL

> Fichier **généré automatiquement** par `python -m src.report`. Données extraites le 2026-10-21.
> Ne pas modifier à la main : relancer le pipeline pour le régénérer.

## `controle_recette.sql`

| controle | resultat | detail |
|---|---|---|
| C2 · aucun doublon dans games | OK | 100 |
| C3 · au moins 15 jeux par éditeur | OK | Electronic Arts = 50 ; Ubisoft = 50 |
| C3 · tous les jeux ont au moins 500 avis | OK | minimum = 7215 |
| C5 · aucune colonne personnelle dans la base | OK | aucune |

## `q1a_satisfaction_globale.sql`

| editeur | nb_jeux | nb_avis | taux_positif_moyen_pct | taux_positif_pondere_pct | taux_positif_median_pct | nb_jeux_sous_70_pct |
|---|---|---|---|---|---|---|
| Electronic Arts | 50 | 5309776 | 80.3 | 77.4 | 85.3 | 11 |
| Ubisoft | 50 | 4473617 | 80.2 | 81.3 | 80.6 | 5 |

## `q1b_stabilite_satisfaction.sql`

| editeur | nb_jeux_comparables | taux_lancement_moyen_pct | taux_recent_moyen_pct | evolution_moyenne_pts | nb_jeux_degrades | nb_jeux_redresses |
|---|---|---|---|---|---|---|
| Electronic Arts | 34 | 79.2 | 78.1 | -1.0 | 6 | 4 |
| Ubisoft | 39 | 75.4 | 78.6 | 3.2 | 6 | 12 |

## `q1c_plus_fortes_evolutions.sql`

| jeu | editeur | taux_lancement_pct | taux_recent_pct | evolution_pts |
|---|---|---|---|---|
| Tom Clancy’s Splinter Cell Blacklist | Ubisoft | 97.9 | 65.4 | -32.5 |
| Battlefield™ 2042 | Electronic Arts | 33.0 | 63.7 | 30.7 |
| STAR WARS™: Squadrons | Electronic Arts | 74.4 | 47.5 | -26.9 |
| The Crew™ 2 | Ubisoft | 51.1 | 76.6 | 25.5 |
| Battlefield 3™ | Electronic Arts | 52.2 | 77.5 | 25.3 |
| Apex Legends™ | Electronic Arts | 93.0 | 67.9 | -25.1 |
| Assassin's Creed® Unity | Ubisoft | 49.7 | 74.3 | 24.5 |
| DiRT Rally 2.0 | Electronic Arts | 67.3 | 91.1 | 23.8 |
| Watch_Dogs™ | Ubisoft | 63.4 | 86.5 | 23.1 |
| Far Cry 3 | Ubisoft | 98.7 | 77.3 | -21.3 |

## `q2a_prix_satisfaction.sql`

| editeur | tranche_prix | nb_jeux | taux_positif_median_pct |
|---|---|---|---|
| Electronic Arts | 0. Gratuit | 5 | 69.8 |
| Electronic Arts | 1. Moins de 20 € | 14 | 89.8 |
| Electronic Arts | 2. 20 à 40 € | 16 | 85.5 |
| Electronic Arts | 3. 40 à 60 € | 9 | 83.4 |
| Electronic Arts | 4. 60 € et plus | 5 | 63.3 |
| Ubisoft | 0. Gratuit | 3 | 79.5 |
| Ubisoft | 1. Moins de 20 € | 15 | 87.3 |
| Ubisoft | 2. 20 à 40 € | 15 | 80.1 |
| Ubisoft | 3. 40 à 60 € | 15 | 78.3 |
| Ubisoft | 4. 60 € et plus | 2 | 73.1 |

## `q2b_correlation_prix.sql`

| editeur | nb_jeux_payants | correlation_pearson | correlation_spearman |
|---|---|---|---|
| Electronic Arts | 44 | -0.55 | -0.49 |
| Ubisoft | 47 | -0.46 | -0.49 |

## `q2c_promotions.sql`

| editeur | statut_prix | nb_jeux | remise_moyenne_pct | taux_positif_median_pct |
|---|---|---|---|---|
| Electronic Arts | Plein tarif | 45 |  | 85.4 |
| Ubisoft | Plein tarif | 47 |  | 80.7 |

## `q3a_longevite.sql`

| editeur | anciennete_steam | nb_jeux | joueurs_connectes_median | nb_jeux_1000_joueurs_ou_plus |
|---|---|---|---|---|
| Electronic Arts | 1. Moins de 2 ans | 7 | 6750 | 6 |
| Electronic Arts | 2. 2 à 5 ans | 7 | 728 | 1 |
| Electronic Arts | 3. 5 à 10 ans | 25 | 917 | 10 |
| Electronic Arts | 4. 10 ans et plus | 11 | 299 | 2 |
| Ubisoft | 1. Moins de 2 ans | 5 | 1617 | 3 |
| Ubisoft | 2. 2 à 5 ans | 10 | 1897 | 7 |
| Ubisoft | 3. 5 à 10 ans | 12 | 2106 | 8 |
| Ubisoft | 4. 10 ans et plus | 22 | 308 | 2 |

## `q3b_jeux_durables.sql`

| jeu | editeur | annees_sur_steam | gratuit | joueurs_connectes | taux_positif_pct | genres |
|---|---|---|---|---|---|---|
| Apex Legends™ | Electronic Arts | 6.0 | True | 79893 | 67.8 | Action, Aventure, Free-to-play |
| Tom Clancy's Rainbow Six Siege | Ubisoft | 10.9 | True | 60193 | 82.1 | Action, Free-to-play |
| The Sims™ 4 | Electronic Arts | 6.3 | True | 25009 | 86.3 | Aventure, Occasionnel, Simulation, Free-to-play |
| Brawlhalla | Ubisoft | 9.0 | True | 11592 | 79.5 | Action, Indépendant, Free-to-play |
| Battlefield™ 1 | Electronic Arts | 6.4 | False | 4491 | 86.5 | Action, Massivement multijoueur |
| Assassin's Creed® Odyssey | Ubisoft | 8.0 | False | 4138 | 88.7 | Action, Aventure, RPG |
| STAR WARS™: The Old Republic™ | Electronic Arts | 6.3 | True | 3785 | 89.6 | Massivement multijoueur, RPG, Free-to-play |
| It Takes Two | Electronic Arts | 5.6 | False | 3635 | 95.4 | Action, Aventure |
| FOR HONOR™ | Ubisoft | 9.7 | False | 3615 | 68.7 | Action |
| Far Cry® 5 | Ubisoft | 8.6 | False | 2762 | 81.1 | Action, Aventure |

## `q4a_francophones.sql`

| editeur | nb_jeux | part_avis_fr_pct | taux_positif_tous_pct | taux_positif_fr_pct | ecart_fr_pts | nb_jeux_fr_plus_severes | nb_jeux_fr_plus_genereux |
|---|---|---|---|---|---|---|---|
| Electronic Arts | 50 | 1.9 | 77.4 | 79.9 | 2.5 | 4 | 5 |
| Ubisoft | 50 | 2.1 | 81.3 | 83.5 | 2.1 | 2 | 9 |

## `q4b_plus_forts_ecarts_fr.sql`

| jeu | editeur | avis_fr | taux_positif_tous_pct | taux_positif_fr_pct | ecart_fr_pts |
|---|---|---|---|---|---|
| Dragon Age: Origins - Ultimate Edition | Electronic Arts | 320 | 85.6 | 66.9 | -18.7 |
| Apex Legends™ | Electronic Arts | 22319 | 67.8 | 81.4 | 13.6 |
| EA SPORTS™ WRC | Electronic Arts | 726 | 61.4 | 72.9 | 11.5 |
| Dead Space™ 3 | Electronic Arts | 190 | 72.4 | 62.6 | -9.8 |
| Medal of Honor™ | Electronic Arts | 235 | 77.0 | 67.2 | -9.7 |
| Far Cry® 2 | Ubisoft | 399 | 75.5 | 65.9 | -9.6 |
| Anno 117: Pax Romana | Ubisoft | 618 | 69.5 | 77.2 | 7.7 |
| The Crew™ 2 | Ubisoft | 2260 | 77.6 | 84.7 | 7.2 |
| Tom Clancy’s The Division™ | Ubisoft | 1383 | 71.0 | 77.0 | 6.1 |
| Assassin's Creed® Unity | Ubisoft | 1891 | 77.7 | 71.7 | -6.0 |
