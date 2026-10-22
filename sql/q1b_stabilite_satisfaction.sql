-- Q1b · La satisfaction est-elle stable dans le temps ?
--
-- Pour chaque jeu, on compare deux fenêtres :
--   - le lancement      : les 3 premiers mois d'avis sur Steam ;
--   - la période récente : les 12 derniers mois avant l'extraction.
-- Règles de comparabilité : au moins 50 avis dans chaque fenêtre, et au moins 2 ans sur Steam
-- pour que les deux fenêtres ne se chevauchent pas.
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
),
evolution AS (
    SELECT
        f.app_id,
        f.up_lancement / f.total_lancement AS taux_lancement,
        f.up_recent / f.total_recent       AS taux_recent
    FROM fenetres AS f
    JOIN games AS g USING (app_id)
    WHERE f.total_lancement >= 50
      AND f.total_recent >= 50
      AND g.years_on_steam >= 2
      -- Les premiers avis doivent dater de la sortie sur Steam (à 3 mois près) : sinon,
      -- la « fenêtre de lancement » ne mesure pas le lancement (jeu sorti avant le système d’avis de Steam).
      AND f.premier_mois <= date_trunc('month', g.steam_release_date) + INTERVAL 3 MONTH
)
SELECT
    g.publisher_group                                                      AS editeur,
    COUNT(*)                                                               AS nb_jeux_comparables,
    ROUND(100 * AVG(e.taux_lancement), 1)                                  AS taux_lancement_moyen_pct,
    ROUND(100 * AVG(e.taux_recent), 1)                                     AS taux_recent_moyen_pct,
    ROUND(100 * AVG(e.taux_recent - e.taux_lancement), 1)                  AS evolution_moyenne_pts,
    COUNT(*) FILTER (WHERE e.taux_recent - e.taux_lancement <= -0.10)      AS nb_jeux_degrades,
    COUNT(*) FILTER (WHERE e.taux_recent - e.taux_lancement >= 0.10)       AS nb_jeux_redresses
FROM evolution AS e
JOIN games AS g USING (app_id)
GROUP BY g.publisher_group
ORDER BY g.publisher_group;
