-- Q2a · Un jeu plus cher est-il mieux noté ?
--
-- ⚠️ Le prix utilisé est le prix catalogue ACTUEL (hors promotion), et non le prix de lancement :
-- les jeux anciens ont souvent baissé de prix. Steam ne fournit pas l'historique des prix.
SELECT
    g.publisher_group                                     AS editeur,
    CASE
        WHEN g.is_free                  THEN '0. Gratuit'
        WHEN g.price_initial_eur < 20   THEN '1. Moins de 20 €'
        WHEN g.price_initial_eur < 40   THEN '2. 20 à 40 €'
        WHEN g.price_initial_eur < 60   THEN '3. 40 à 60 €'
        ELSE                                 '4. 60 € et plus'
    END                                                   AS tranche_prix,
    COUNT(*)                                              AS nb_jeux,
    ROUND(100 * MEDIAN(r.positive_rate), 1)               AS taux_positif_median_pct
FROM games AS g
JOIN review_summary AS r USING (app_id)
WHERE r.language = 'all'
  AND g.price_initial_eur IS NOT NULL
GROUP BY ALL
ORDER BY editeur, tranche_prix;
