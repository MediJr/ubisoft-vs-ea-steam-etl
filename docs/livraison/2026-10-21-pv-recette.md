# Procès-verbal de recette

> 🎭 **Scénario fictif** : voir le [README](../../README.md).

| | |
|---|---|
| **Référence** | LFG-2026-001 · Livrable L6 |
| **Version recettée** | 1.0.0 |
| **Date de recette** | 2026-10-21 |
| **Client** | Lumen Forge Games, représenté par Camille Roux |
| **Prestataire** | Data engineer indépendant |

---

## 1. Conditions de la recette

- **Environnement neuf :** copie des seuls fichiers publiables du dépôt (38 fichiers, sans données ni environnement virtuel),
  nouvel environnement Python 3.14, installation par `pip install -r requirements.txt`.
- **Exécution :** `python -m src.pipeline`, la commande unique du README.
- **Contrôles automatiques :** [`sql/controle_recette.sql`](../../sql/controle_recette.sql).

## 2. Résultats par critère (cahier des charges, section 10)

| # | Critère | Méthode | Résultat | Statut |
|---|---|---|---|---|
| **C1** | Le pipeline s'exécute de bout en bout en une seule commande | Exécution sur l'environnement neuf, en suivant le README | Installation en 54 s. Pipeline complet en **30 min 25 s**, code de retour 0. Base, graphiques et résultats produits. | ✅ Conforme |
| **C2** | Relancer le pipeline ne crée pas de doublons | Comptage des lignes de chaque table avant et après une nouvelle exécution | Avant : 100 / 200 / 9 929 / 100 / 53. Après : **identique**. Clés primaires sur toutes les tables. | ✅ Conforme |
| **C3** | Au moins 15 jeux par éditeur respectent le périmètre | Requête de contrôle | **50 jeux** pour chaque éditeur, tous avec au moins 500 avis (minimum : 7 215) | ✅ Conforme |
| **C4** | Chaque question a sa requête SQL et sa réponse argumentée | Relecture du rapport | Q1 : 3 requêtes, Q2 : 3, Q3 : 2, Q4 : 2. Chaque question a une section dans le [rapport](Rapport_Ubisoft_vs_EA_FR.pdf) | ✅ Conforme |
| **C5** | Aucune donnée personnelle stockée | Inspection du schéma et recherche dans les 930 fichiers bruts | **Aucun** champ `steamid`, `personaname`, `author` ni texte d'avis, ni dans la base, ni dans les fichiers bruts | ✅ Conforme |
| **C6** | Les limites sont explicitées | Relecture du rapport | Section 12 du rapport PDF : 6 limites et 4 éléments de dette technique | ✅ Conforme |

## 3. Réserves

| # | Réserve | Gravité | Traitement proposé |
|---|---|---|---|
| R1 | **Reproductibilité du panel :** la découverte des jeux repose sur l'ordre de pertinence de la recherche Steam, qui varie légèrement d'une exécution à l'autre. Entre l'exécution de production et celle de recette, 99 jeux sur 100 sont identiques (*Dead Space (2008)* remplacé par *Alerte Rouge 2*). Les indicateurs clés restent identiques au dixième près (taux pondérés : EA 77,4 %, Ubisoft 81,3 %). | Mineure | Dans une version ultérieure, rendre la découverte déterministe en parcourant tout le catalogue de l'éditeur, puis en triant par nombre d'avis. |
| R2 | **Question des promotions (Q2) non tranchée :** aucun jeu n'était en promotion le jour de l'extraction. | Mineure, liée aux données | Suivi quotidien des prix (piste d'évolution n°1 du rapport). |

## 4. Décision

- [x] **Recette prononcée avec réserves mineures.** Les réserves ne remettent pas en cause les conclusions du rapport.
- [ ] Recette refusée

| | Client | Prestataire |
|---|---|---|
| **Nom** | Camille Roux | Data engineer |
| **Date** | 2026-10-21 | 2026-10-21 |
| **Mention** | Bon pour réception, avec réserves R1 et R2 | Livraison conforme au cahier des charges LFG-2026-001 |
