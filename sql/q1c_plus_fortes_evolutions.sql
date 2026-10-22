-- Q1c · Les jeux dont la satisfaction a le plus changé depuis leur lancement sur Steam
-- (mêmes fenêtres et mêmes règles de comparabilité que Q1b).
WITH premiers_mois AS (
    SELECT app_id, MIN(month) AS premier_mois
    FROM reviews_monthly
    GROUP BY app_id
),
fenetres AS (
    SELECT
        m.app_id,
        p.premier_mois,
        SUM(m.reviews_up)                  FILTER (WHERE m.month <  p.premier_mois + INTERVAL 3 MONTH) AS up_lancement,
        SUM(m.reviews_up + m.reviews_down) FILTER (WHERE m.month <  p.premier_mois + INTERVAL 3 MONTH) AS total_lancement,
        SUM(m.reviews_up)                  FILTER (WHERE m.month >= date_trunc('month', g.extracted_on) - INTERVAL 12 MONTH) AS up_recent,
        SUM(m.reviews_up + m.reviews_down) FILTER (WHERE m.month >= date_trunc('month', g.extracted_on) - INTERVAL 12 MONTH) AS total_recent
    FROM reviews_monthly AS m
    JOIN premiers_mois AS p USING (app_id)
    JOIN games AS g USING (app_id)
    GROUP BY m.app_id, p.premier_mois
)
SELECT
    g.name                                                                    AS jeu,
    g.publisher_group                                                         AS editeur,
    ROUND(100 * f.up_lancement / f.total_lancement, 1)                        AS taux_lancement_pct,
    ROUND(100 * f.up_recent / f.total_recent, 1)                              AS taux_recent_pct,
    ROUND(100 * (f.up_recent / f.total_recent - f.up_lancement / f.total_lancement), 1) AS evolution_pts
FROM fenetres AS f
JOIN games AS g USING (app_id)
WHERE f.total_lancement >= 50
  AND f.total_recent >= 50
  AND g.years_on_steam >= 2
  AND f.premier_mois <= date_trunc('month', g.steam_release_date) + INTERVAL 3 MONTH
ORDER BY ABS(f.up_recent / f.total_recent - f.up_lancement / f.total_lancement) DESC
LIMIT 10;
