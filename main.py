import logging
from etl.extract import extract_matches
from etl.transform import transform_matches
from etl.load_mysql import load_all_tables
import yaml
from pathlib import Path


def setup_logging():
    """
    Configure le système de logs pour l'ensemble du pipeline ETL.
    Les logs sont enregistrés dans logs/etl.log et affichés en console.

    Retour
    ------
    None
    """
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s — %(levelname)s — %(message)s",
        handlers=[
            logging.FileHandler(log_dir / "etl.log", mode="w", encoding="utf-8"),
            logging.StreamHandler()
        ]
    )


def load_config(path: str) -> dict:
    """
    Charge le fichier de configuration YAML contenant les paramètres
    de connexion MySQL.

    Paramètres
    ----------
    path : str
        Chemin vers le fichier YAML (ex : config/db_config.yaml).

    Retour
    ------
    dict
        Dictionnaire contenant les paramètres de connexion.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)


def main():
    """
    Orchestration complète du pipeline ETL :
    1. Extraction du dataset nettoyé
    2. Transformation en tables dimensionnelles + table de faits
    3. Chargement dans MySQL

    Retour
    ------
    None
    """
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("===== DÉBUT DU PIPELINE ETL =====")

    # 1. Extraction
    df = extract_matches("data_clean/matches_1930_2022_clean.csv")

    # 2. Transformation
    tables = transform_matches(df)

    # 3. Chargement MySQL
    config = load_config("config/db_config.yaml")
    load_all_tables(tables, config)

    logger.info("===== FIN DU PIPELINE ETL =====")


if __name__ == "__main__":
    main()
