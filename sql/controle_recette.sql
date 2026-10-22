-- Contrôles de recette (cahier des charges, section 10).
-- Chaque ligne doit afficher « OK ».
SELECT 'C2 · aucun doublon dans games' AS controle,
       CASE WHEN COUNT(*) = COUNT(DISTINCT app_id) THEN 'OK' ELSE 'ÉCHEC' END AS resultat,
       COUNT(*)::VARCHAR AS detail
FROM games
UNION ALL
SELECT 'C3 · au moins 15 jeux par éditeur',
       CASE WHEN MIN(n) >= 15 AND COUNT(*) = 2 THEN 'OK' ELSE 'ÉCHEC' END,
       STRING_AGG(publisher_group || ' = ' || n, ' ; ' ORDER BY publisher_group)
FROM (SELECT publisher_group, COUNT(*) AS n FROM games GROUP BY publisher_group)
UNION ALL
SELECT 'C3 · tous les jeux ont au moins 500 avis',
       CASE WHEN MIN(total_reviews) >= 500 THEN 'OK' ELSE 'ÉCHEC' END,
       'minimum = ' || MIN(total_reviews)
FROM review_summary
WHERE language = 'all'
UNION ALL
SELECT 'C5 · aucune colonne personnelle dans la base',
       CASE WHEN COUNT(*) = 0 THEN 'OK' ELSE 'ÉCHEC' END,
       COALESCE(STRING_AGG(table_name || '.' || column_name, ', '), 'aucune')
FROM information_schema.columns
WHERE regexp_matches(lower(column_name), 'steamid|persona|author|user|review_text');
