-- Q4a · Les joueurs francophones jugent-ils différemment ces éditeurs ?
--
-- « Francophones » = auteurs d'avis rédigés en français (Steam ne fournit pas le pays).
-- Comparaison sur les jeux ayant au moins 100 avis en français, pour des taux fiables.
WITH comparaison AS (
    SELECT
        g.publisher_group,
        g.app_id,
        tous.total_reviews     AS avis_tous,
        tous.total_positive    AS positifs_tous,
        fr.total_reviews       AS avis_fr,
        fr.total_positive      AS positifs_fr
    FROM games AS g
    JOIN review_summary AS tous ON tous.app_id = g.app_id AND tous.language = 'all'
    JOIN review_summary AS fr   ON fr.app_id   = g.app_id AND fr.language   = 'french'
    WHERE fr.total_reviews >= 100
)
SELECT
    publisher_group                                                          AS editeur,
    COUNT(*)                                                                 AS nb_jeux,
    ROUND(100 * SUM(avis_fr) / SUM(avis_tous), 1)                            AS part_avis_fr_pct,
    ROUND(100 * SUM(positifs_tous) / SUM(avis_tous), 1)                      AS taux_positif_tous_pct,
    ROUND(100 * SUM(positifs_fr) / SUM(avis_fr), 1)                          AS taux_positif_fr_pct,
    ROUND(100 * (SUM(positifs_fr) / SUM(avis_fr) - SUM(positifs_tous) / SUM(avis_tous)), 1) AS ecart_fr_pts,
    COUNT(*) FILTER (WHERE positifs_fr / avis_fr < positifs_tous / avis_tous - 0.05) AS nb_jeux_fr_plus_severes,
    COUNT(*) FILTER (WHERE positifs_fr / avis_fr > positifs_tous / avis_tous + 0.05) AS nb_jeux_fr_plus_genereux
FROM comparaison
GROUP BY publisher_group
ORDER BY publisher_group;
