-- Q4b · Les jeux sur lesquels les francophones se démarquent le plus (au moins 100 avis en français)
SELECT
    g.name                                                         AS jeu,
    g.publisher_group                                              AS editeur,
    fr.total_reviews                                               AS avis_fr,
    ROUND(100 * tous.positive_rate, 1)                             AS taux_positif_tous_pct,
    ROUND(100 * fr.positive_rate, 1)                               AS taux_positif_fr_pct,
    ROUND(100 * (fr.positive_rate - tous.positive_rate), 1)        AS ecart_fr_pts
FROM games AS g
JOIN review_summary AS tous ON tous.app_id = g.app_id AND tous.language = 'all'
JOIN review_summary AS fr   ON fr.app_id   = g.app_id AND fr.language   = 'french'
WHERE fr.total_reviews >= 100
ORDER BY ABS(fr.positive_rate - tous.positive_rate) DESC
LIMIT 10;
