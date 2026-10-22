-- Q3b · Les jeux d'au moins 5 ans sur Steam qui attirent encore le plus de joueurs
SELECT
    g.name                                  AS jeu,
    g.publisher_group                       AS editeur,
    g.years_on_steam                        AS annees_sur_steam,
    g.is_free                               AS gratuit,
    p.current_players                       AS joueurs_connectes,
    ROUND(100 * r.positive_rate, 1)         AS taux_positif_pct,
    g.genres                                AS genres
FROM games AS g
JOIN player_snapshot AS p USING (app_id)
JOIN review_summary AS r USING (app_id)
WHERE r.language = 'all'
  AND g.years_on_steam >= 5
ORDER BY p.current_players DESC NULLS LAST
LIMIT 10;
