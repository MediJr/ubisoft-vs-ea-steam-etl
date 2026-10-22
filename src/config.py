"""Paramètres du pipeline.

Tout ce qui définit le périmètre (cahier des charges, section 4) ou le comportement du pipeline
est centralisé ici. Ainsi, aucun « nombre magique » n'est dispersé dans le code, et une
évolution du périmètre se fait à un seul endroit.
"""

from pathlib import Path

# --- Chemins ---------------------------------------------------------------
# On part de l'emplacement de ce fichier, et non du dossier courant : le pipeline
# fonctionne ainsi quel que soit l'endroit d'où on le lance.
PROJECT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_DIR / "data"
RAW_DIR = DATA_DIR / "raw"              # réponses brutes des API, jamais modifiées
DATABASE_PATH = DATA_DIR / "steam.duckdb"

# --- Périmètre (cahier des charges, section 4) -----------------------------
PUBLISHERS = ["Ubisoft", "Electronic Arts"]
MAX_GAMES_PER_PUBLISHER = 50
MIN_REVIEWS = 500

# Nombre de jeux candidats examinés par éditeur. Il est plus grand que
# MAX_GAMES_PER_PUBLISHER, car une partie des candidats sera écartée
# (moins de 500 avis, autre éditeur réel, etc.).
MAX_CANDIDATES_PER_PUBLISHER = 80

# Le client est français : prix en euros (pays « fr ») et fiches en français.
STEAM_COUNTRY = "fr"
STEAM_LANGUAGE = "french"

# --- Comportement réseau ---------------------------------------------------
# Steam tolère environ 200 requêtes par tranche de 5 minutes. Une pause de 1,5 s
# entre deux appels nous maintient sous cette limite.
REQUEST_PAUSE_SECONDS = 1.5
REQUEST_TIMEOUT_SECONDS = 20
MAX_RETRIES = 3

# Se présenter honnêtement auprès des API est une règle de politesse du web :
# en cas de problème, l'administrateur sait qui contacter.
USER_AGENT = "portfolio-etl-steam/0.1 (projet pedagogique, usage non commercial)"
