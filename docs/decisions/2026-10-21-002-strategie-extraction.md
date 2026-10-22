# ADR 002 : Stratégie d'extraction

- **Date :** 2026-10-21
- **Statut :** Acceptée

## Contexte

- Il faut collecter 5 à 6 sources par jeu, pour environ 160 jeux candidats (80 par éditeur).
- Steam limite le débit à environ 200 requêtes par tranche de 5 minutes.
- Tout collecter pour tous les candidats représenterait environ 1 000 appels, soit plus de 25 minutes,
  alors qu'une partie des jeux sera de toute façon écartée (moins de 500 avis).

## Décisions

### 1. Extraction en deux passes
- **Passe légère :** la synthèse des avis (1 appel) pour chaque candidat.
- **Passe détaillée :** les 5 autres sources, uniquement pour les jeux d'au moins 500 avis.

Le filtre sur le nombre d'avis s'applique dès l'extraction, ce qui est une petite entorse au principe « E n'interprète pas ».
Ce compromis est assumé : il réduit fortement le nombre d'appels, et le **manifeste** trace à la fois
les candidats et les jeux retenus, donc rien n'est caché.

### 2. Couche brute immuable et datée
- Les réponses sont enregistrées **telles quelles** dans `data/raw/<AAAA-MM-JJ>/<source>/<app_id>.json`.
- Un `manifest.json` décrit chaque exécution : date, candidats, jeux retenus, heure de fin.

### 3. Cache par exécution
- Si un fichier brut existe déjà pour la date du jour, il est relu au lieu de rappeler l'API.
- Une extraction interrompue reprend donc là où elle s'était arrêtée.

### 4. Extraction polie
- Pause de 1,5 s entre deux appels, avec 3 réessais à délai croissant en cas d'erreur 429 ou 5xx.
- Un `User-Agent` explicite identifie le projet.

### 5. Minimisation RGPD dès la source
- Les avis sont demandés avec `num_per_page=0` : on ne reçoit **que des totaux**, sans aucun avis individuel.
- La donnée personnelle n'est donc jamais téléchargée, pas même dans la couche brute.
  C'est plus sûr que de la télécharger puis de la supprimer.

## Conséquences

- ✅ Environ 15 minutes d'extraction au lieu de plus de 25
- ✅ Une reprise après incident sans coût supplémentaire
- ✅ Une conformité RGPD vérifiable : `grep` ne trouve aucun champ `steamid` ni `personaname` dans `data/raw`
- ⚠️ La découverte des jeux repose sur la page de recherche Steam, **non officielle** : son format peut changer
