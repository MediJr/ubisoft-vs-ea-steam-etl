-- Q1a · Quel éditeur satisfait le mieux ses joueurs sur Steam ?
--
-- Trois mesures complémentaires, car elles ne racontent pas la même histoire :
--   - moyenne par jeu  : chaque jeu pèse autant (la qualité « typique » d'un jeu de l'éditeur) ;
--   - taux pondéré     : chaque avis pèse autant (dominé par les jeux très populaires) ;
--   - médiane          : insensible aux quelques jeux extrêmes.
SELECT
    g.publisher_group                                                AS editeur,
    COUNT(*)                                                         AS nb_jeux,
    SUM(r.total_reviews)::BIGINT                                     AS nb_avis,
    ROUND(100 * AVG(r.positive_rate), 1)                             AS taux_positif_moyen_pct,
    ROUND(100 * SUM(r.total_positive) / SUM(r.total_reviews), 1)     AS taux_positif_pondere_pct,
    ROUND(100 * MEDIAN(r.positive_rate), 1)                          AS taux_positif_median_pct,
    COUNT(*) FILTER (WHERE r.positive_rate < 0.70)                   AS nb_jeux_sous_70_pct
FROM games AS g
JOIN review_summary AS r USING (app_id)
WHERE r.language = 'all'
GROUP BY g.publisher_group
ORDER BY g.publisher_group;
