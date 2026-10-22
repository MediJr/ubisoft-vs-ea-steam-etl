-- Q2b · Force du lien entre le prix et la satisfaction (jeux payants uniquement)
--
-- Corrélation de Pearson : de -1 (plus c'est cher, moins c'est bien noté)
-- à +1 (plus c'est cher, mieux c'est noté). Autour de 0, il n'y a pas de lien linéaire.
-- On calcule aussi la corrélation de rang (Spearman), plus robuste aux valeurs extrêmes :
-- c'est la corrélation de Pearson appliquée aux rangs.
WITH payants AS (
    SELECT
        g.publisher_group,
        g.price_initial_eur::DOUBLE AS prix,
        r.positive_rate::DOUBLE     AS taux,
        RANK() OVER (PARTITION BY g.publisher_group ORDER BY g.price_initial_eur) AS rang_prix,
        RANK() OVER (PARTITION BY g.publisher_group ORDER BY r.positive_rate)     AS rang_taux
    FROM games AS g
    JOIN review_summary AS r USING (app_id)
    WHERE r.language = 'all'
      AND NOT g.is_free
      AND g.price_initial_eur > 0
)
SELECT
    publisher_group                          AS editeur,
    COUNT(*)                                 AS nb_jeux_payants,
    ROUND(CORR(prix, taux), 2)               AS correlation_pearson,
    ROUND(CORR(rang_prix, rang_taux), 2)     AS correlation_spearman
FROM payants
GROUP BY publisher_group
ORDER BY publisher_group;
