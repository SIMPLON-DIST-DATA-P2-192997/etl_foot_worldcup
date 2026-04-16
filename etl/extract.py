import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

EXPECTED_COLUMNS = [
    "home_team",
    "away_team",
    "home_result",
    "away_result",
    "result",
    "date",
    "round",
    "city",
    "stadium",
    "edition"
]

def extract_matches(csv_path: str) -> pd.DataFrame:
    """
    Charge le fichier CSV final contenant l’ensemble des matchs (1930–2022),
    vérifie la présence des colonnes attendues et convertit la colonne date.

    Paramètres
    ----------
    csv_path : str
        Chemin vers le fichier CSV nettoyé situé dans data_clean/.

    Retour
    ------
    pd.DataFrame
        DataFrame Pandas contenant les données extraites et validées.

    Exceptions
    ----------
    FileNotFoundError
        Si le fichier CSV n'existe pas.
    ValueError
        Si une ou plusieurs colonnes attendues sont absentes.
    """
    csv_path = Path(csv_path)

    if not csv_path.exists():
        logger.error(f"Fichier introuvable : {csv_path}")
        raise FileNotFoundError(f"Fichier manquant : {csv_path}")

    logger.info(f"Chargement du dataset depuis {csv_path}")

    df = pd.read_csv(csv_path)

    # Vérification des colonnes attendues
    missing_cols = set(EXPECTED_COLUMNS) - set(df.columns)
    if missing_cols:
        logger.error(f"Colonnes manquantes dans le dataset : {missing_cols}")
        raise ValueError(f"Colonnes manquantes : {missing_cols}")

    # Conversion robuste : on tente datetime, sinon fallback YYYY-01-01
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

    # Remplacement des dates invalides par YYYY-01-01
    mask_invalid = df["date"].isna()
    if mask_invalid.any():
        df.loc[mask_invalid, "date"] = pd.to_datetime(
            df.loc[mask_invalid, "edition"].str[:4] + "-01-01"
        )

    logger.info(f"Dataset chargé avec succès : {len(df)} lignes.")

    return df
