# 02 · Compte rendu de la réunion de cadrage

> 🎭 **Scénario fictif** : voir le [brief client](2026-10-21-01-brief-client.md).

| | |
|---|---|
| **Date** | 2026-10-21 |
| **Format** | Visioconférence, 45 min |
| **Participants** | Camille Roux (Lumen Forge Games, directrice générale) · Théo Garnier (Lumen Forge Games, producteur) · Data engineer (prestataire) |
| **Objectif** | Transformer la demande initiale en questions précises, mesurables et réalisables |

---

## 1. Questions posées et réponses du client

| # | Question du prestataire | Réponse du client |
|---|---|---|
| 1 | Que signifie « ce qui marche » pour vous ? | Avant tout, **des joueurs satisfaits sur la durée**. Les avis Steam sont notre vitrine : un jeu mal noté ne se vend plus. |
| 2 | Les ventes vous intéressent-elles ? | Oui, mais on sait que les chiffres officiels ne sont pas publics. Des ordres de grandeur suffiront. |
| 3 | Quels jeux comparer ? | Les jeux **publiés sur Steam** par Ubisoft et EA, pas les DLC ni les bandes-son. Seulement ceux qui ont assez d'avis pour être représentatifs. |
| 4 | Pourquoi ces deux éditeurs ? | Ubisoft est français, comme nous. EA est le géant américain. Ce sont deux modèles différents. |
| 5 | Le marché francophone compte-t-il ? | Oui. Nous visons d'abord la France, puis l'international. |
| 6 | Quelles décisions allez-vous prendre avec ces résultats ? | Fixer le prix de lancement, décider quand faire des promotions, et préparer notre suivi des avis après la sortie. |
| 7 | Quel format de livrable ? | Un **rapport clair**, lisible par des non-spécialistes, avec des graphiques. Les données doivent pouvoir être réutilisées plus tard. |
| 8 | Une analyse ponctuelle ou un suivi régulier ? | Ponctuelle pour l'instant. Mais si le pipeline peut être relancé facilement, c'est un plus. |
| 9 | Avez-vous évoqué l'impact boursier des sorties ratées ? | C'est une curiosité, pas une priorité. |

---

## 2. Questions business retenues

| # | Question | Décision du client éclairée |
|---|---|---|
| **Q1** | Lequel des deux éditeurs satisfait le mieux ses joueurs sur Steam, et cette satisfaction est-elle **stable dans le temps** ? | Préparer le suivi de réputation après la sortie |
| **Q2** | Un jeu **plus cher** est-il mieux noté ? Les **promotions** sont-elles un signe de difficulté ? | Prix de lancement et politique de promotions |
| **Q3** | Quels jeux **gardent leurs joueurs** des années après leur sortie ? | Stratégie de contenu après le lancement |
| **Q4** | Les joueurs **francophones** jugent-ils différemment ces éditeurs ? | Priorité au marché français ou à l'international |

## 3. Décisions prises

- ✅ Source de données : **Steam uniquement** (avis, fiches des jeux, joueurs connectés), complétée par les estimations de SteamSpy
- ✅ Livrable principal : un **rapport d'analyse** + un **pipeline relançable** + une base de données réutilisable
- ✅ L'impact boursier est **hors périmètre** et noté comme piste future
- ✅ Aucune donnée personnelle de joueur ne sera conservée

## 4. Points de vigilance signalés au client

- ⚠️ **Steam n'est pas tout le marché.** EA et Ubisoft vendent aussi via leurs propres plateformes (EA app, Ubisoft Connect) et sur consoles. Les conclusions porteront sur **les joueurs Steam**.
- ⚠️ **Les ventes sont des estimations** (SteamSpy), pas des chiffres officiels.
- ⚠️ **Les prix sont un instantané** : Steam ne fournit pas l'historique des prix. La question des promotions sera donc traitée avec prudence.
- ⚠️ Les avis Steam peuvent être influencés par des campagnes de notes négatives massives (*review bombing*).

## 5. Actions

| Action | Responsable | Échéance |
|---|---|---|
| Rédiger et envoyer le cahier des charges | Prestataire | 2026-10-21 |
| Valider le cahier des charges | Camille Roux | À réception |

➡️ Suite : [03 · Cahier des charges](2026-10-21-03-cahier-des-charges.md)
