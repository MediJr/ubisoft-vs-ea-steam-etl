# ADR 003 : Source de la mesure de fréquentation (Q3)

- **Date :** 2026-10-21
- **Statut :** Acceptée

## Contexte

Le cahier des charges prévoyait deux mesures de fréquentation :
- le **pic de joueurs de la veille**, selon SteamSpy ;
- les **joueurs connectés** au moment de l'extraction, selon l'API officielle de Steam.

Sur les données réelles, **SteamSpy renvoie 0 pour 9 jeux**, tous récents et pourtant très joués.
Par exemple, *Battlefield 6* : 0 selon SteamSpy, contre 45 100 joueurs connectés selon Steam.

## Décision

La question Q3 repose sur les **joueurs connectés (API officielle Steam)**. Le pic SteamSpy reste
stocké dans `player_snapshot.peak_players_yesterday`, à titre d'information, mais il n'est utilisé dans aucune analyse.

## Justification

- Le zéro de SteamSpy est une **valeur manquante déguisée** : elle aurait faussé la médiane des jeux récents.
- La corrélation entre les deux sources est forte (0,85) lorsque SteamSpy dispose de la donnée.
  Le changement ne modifie donc pas la nature de la mesure.
- Une source officielle est préférable à une source tierce.

## Conséquences

- ✅ Les jeux récents sont correctement mesurés
- ⚠️ La mesure est un instantané (mercredi, vers 19 h, heure de Paris), et non un pic quotidien
