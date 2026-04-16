import mysql.connector
from mysql.connector import Error
import logging
from typing import Dict
import pandas as pd

logger = logging.getLogger(__name__)


def get_connection(config: Dict[str, str]):
    """
    Établit une connexion MySQL à partir d'un dictionnaire de configuration.

    Paramètres
    ----------
    config : Dict[str, str]
        Dictionnaire contenant les informations de connexion :
        {
            "host": "localhost",
            "user": "alexandre",
            "password": "...",
            "database": "foot"
        }

    Retour
    ------
    mysql.connector.connection.MySQLConnection
        Objet connexion MySQL actif.

    Exceptions
    ----------
    Error
        Si la connexion échoue.
    """
    try:
        conn = mysql.connector.connect(**config)
        logger.info("Connexion MySQL établie avec succès.")
        return conn
    except Error as e:
        logger.error(f"Erreur de connexion MySQL : {e}")
        raise


def insert_dataframe(cursor, table_name: str, df: pd.DataFrame):
    """
    Insère un DataFrame Pandas dans une table MySQL en utilisant des requêtes préparées.

    Paramètres
    ----------
    cursor : mysql.connector.cursor.MySQLCursor
        Curseur MySQL actif.
    table_name : str
        Nom de la table SQL dans laquelle insérer les données.
    df : pd.DataFrame
        DataFrame contenant les données à insérer.

    Retour
    ------
    None

    Notes
    -----
    - Les colonnes du DataFrame doivent correspondre exactement aux colonnes SQL.
    - Les valeurs NULL sont automatiquement gérées par mysql.connector.
    """
    placeholders = ", ".join(["%s"] * len(df.columns))
    columns = ", ".join(df.columns)
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    logger.info(f"Insertion dans la table '{table_name}' ({len(df)} lignes).")

    data = [tuple(row) for row in df.to_numpy()]

    cursor.executemany(sql, data)


def load_all_tables(tables: Dict[str, pd.DataFrame], config: Dict[str, str]):
    """
    Charge l'ensemble des tables transformées dans MySQL dans le bon ordre :
    1. team
    2. city
    3. stadium
    4. edition
    5. match

    Paramètres
    ----------
    tables : Dict[str, pd.DataFrame]
        Dictionnaire contenant les DataFrames générés par transform_matches().
    config : Dict[str, str]
        Paramètres de connexion MySQL.

    Retour
    ------
    None

    Étapes
    ------
    - Connexion MySQL
    - Démarrage d'une transaction
    - Insertion des tables dimensionnelles
    - Insertion de la table de faits
    - Commit si tout est OK
    - Rollback en cas d'erreur

    Exceptions
    ----------
    Error
        Si une erreur SQL survient.
    """
    conn = get_connection(config)
    cursor = conn.cursor()

    try:
        logger.info("Début du chargement MySQL (transaction ouverte).")

        # 1. Tables dimensionnelles
        insert_dataframe(cursor, "team", tables["team"])
        insert_dataframe(cursor, "city", tables["city"])
        insert_dataframe(cursor, "stadium", tables["stadium"])
        insert_dataframe(cursor, "edition", tables["edition"])

        # 2. Table de faits
        insert_dataframe(cursor, "`match`", tables["match"])

        conn.commit()
        logger.info("Chargement MySQL terminé avec succès (commit).")

    except Error as e:
        conn.rollback()
        logger.error(f"Erreur lors du chargement MySQL : {e}")
        raise

    finally:
        cursor.close()
        conn.close()
        logger.info("Connexion MySQL fermée.")
