-- Q3a · Les jeux gardent-ils leurs joueurs avec les années ?
--
-- Mesure de fréquentation : joueurs connectés au moment de l'extraction (API officielle Steam).
-- Le pic de SteamSpy a été écarté : il vaut 0 pour plusieurs jeux récents très joués
-- (ex. Battlefield 6), signe que SteamSpy ne les suit pas encore (voir le journal du 2026-10-21).
-- ⚠️ L'ancienneté est celle SUR STEAM : EA est revenu sur Steam en 2020 et Ubisoft fin 2022,
-- avec des jeux parfois sortis des années plus tôt.
SELECT
    g.publisher_group                                        AS editeur,
    CASE
        WHEN g.years_on_steam < 2   THEN '1. Moins de 2 ans'
        WHEN g.years_on_steam < 5   THEN '2. 2 à 5 ans'
        WHEN g.years_on_steam < 10  THEN '3. 5 à 10 ans'
        ELSE                             '4. 10 ans et plus'
    END                                                      AS anciennete_steam,
    COUNT(*)                                                 AS nb_jeux,
    MEDIAN(p.current_players)::INTEGER                       AS joueurs_connectes_median,
    COUNT(*) FILTER (WHERE p.current_players >= 1000)        AS nb_jeux_1000_joueurs_ou_plus
FROM games AS g
JOIN player_snapshot AS p USING (app_id)
WHERE g.years_on_steam IS NOT NULL
GROUP BY ALL
ORDER BY editeur, anciennete_steam;
