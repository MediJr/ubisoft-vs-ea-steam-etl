-- Q2c · Les jeux en promotion sont-ils moins bien notés ?
--
-- ⚠️ Instantané : un jeu est « en promotion » s'il l'est LE JOUR de l'extraction.
-- Les promotions saisonnières (soldes d'été, d'hiver…) peuvent fausser la comparaison.
SELECT
    g.publisher_group                                             AS editeur,
    CASE WHEN g.discount_percent > 0 THEN 'En promotion' ELSE 'Plein tarif' END AS statut_prix,
    COUNT(*)                                                      AS nb_jeux,
    ROUND(AVG(g.discount_percent) FILTER (WHERE g.discount_percent > 0), 0) AS remise_moyenne_pct,
    ROUND(100 * MEDIAN(r.positive_rate), 1)                       AS taux_positif_median_pct
FROM games AS g
JOIN review_summary AS r USING (app_id)
WHERE r.language = 'all'
  AND NOT g.is_free
GROUP BY ALL
ORDER BY editeur, statut_prix;
