import pandas as pd
import logging
from typing import Dict, Tuple

logger = logging.getLogger(__name__)


def generate_dimension_table(df: pd.DataFrame, column_name: str) -> Tuple[pd.DataFrame, Dict[str, int]]:
    """
    Génère une table de dimension à partir d'une colonne catégorielle du dataset principal.
    Cette fonction extrait les valeurs uniques, crée un identifiant entier pour chaque valeur,
    et renvoie à la fois la table dimensionnelle et un dictionnaire de correspondance.

    Paramètres
    ----------
    df : pd.DataFrame
        Le DataFrame contenant l'ensemble des matchs (1930–2022).
    column_name : str
        Le nom de la colonne à transformer en table de dimension
        (exemples : 'home_team', 'city', 'stadium', 'edition').

    Retour
    ------
    Tuple[pd.DataFrame, Dict[str, int]]
        - La table dimensionnelle contenant deux colonnes :
            * id_<dimension> : identifiant entier auto‑généré
            * <dimension>    : valeur textuelle d'origine
        - Un dictionnaire permettant de mapper chaque valeur textuelle vers son identifiant entier.

    Notes
    -----
    - Les valeurs NULL sont conservées dans la table dimensionnelle et reçoivent un identifiant.
    - L'ordre des identifiants est déterministe (tri alphabétique), ce qui facilite la reproductibilité.
    """
    logger.info(f"Génération de la dimension '{column_name}'")

    unique_values = sorted(df[column_name].drop_duplicates().fillna("UNKNOWN"))

    dim_df = pd.DataFrame({
        f"id_{column_name}": range(1, len(unique_values) + 1),
        column_name: unique_values
    })

    mapping = dict(zip(unique_values, dim_df[f"id_{column_name}"]))

    logger.info(f"Dimension '{column_name}' générée avec {len(dim_df)} lignes.")

    return dim_df, mapping


def apply_mapping(df: pd.DataFrame, column_name: str, mapping: Dict[str, int], new_col: str):
    """
    Applique un dictionnaire de correspondance (valeur textuelle → identifiant entier)
    à une colonne du DataFrame principal.

    Paramètres
    ----------
    df : pd.DataFrame
        Le DataFrame principal contenant les matchs.
    column_name : str
        Le nom de la colonne textuelle à convertir.
    mapping : Dict[str, int]
        Le dictionnaire associant chaque valeur textuelle à un identifiant entier.
    new_col : str
        Le nom de la nouvelle colonne contenant les identifiants.

    Retour
    ------
    None
        La fonction modifie le DataFrame en place.

    Exceptions
    ----------
    KeyError
        Si une valeur textuelle n'est pas présente dans le dictionnaire de mapping.
    """
    logger.info(f"Application du mapping pour la colonne '{column_name}' → '{new_col}'")

    df[column_name] = df[column_name].fillna("UNKNOWN")

    try:
        df[new_col] = df[column_name].map(mapping)
    except Exception as e:
        logger.error(f"Erreur lors du mapping de la colonne '{column_name}' : {e}")
        raise

    logger.info(f"Mapping appliqué avec succès pour '{column_name}'.")

def transform_matches(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Transforme le DataFrame brut des matchs en tables dimensionnelles et en table de faits
    conformes au modèle relationnel (MLD) et prêtes à être chargées dans MySQL.
    """

    logger.info("Début de la transformation du dataset.")

    # ============================================================
    # 0. FILTRAGE DES LIGNES NON VALIDES
    # ============================================================

    invalid_patterns = [
        r"^[A-H][1-4]$",     # A1, B2, C3...
        r"^[A-H]$",          # A, B, C...
        r"^\d+$",            # 1, 2, 3...
        r"^WINNER",          # WINNER X, WINNER Y...
        r"^LOSER",           # LOSER X, LOSER Y...
    ]
    pattern = "|".join(invalid_patterns)

    df = df[
        ~df["home_team"].astype(str).str.match(pattern) &
        ~df["away_team"].astype(str).str.match(pattern)
    ].copy()

    # Suppression des qualifications
    df = df[~df["round"].str.contains("qualification", case=False, na=False)].copy()

    # Suppression des matchs sans score
    df = df.dropna(subset=["home_result", "away_result"]).copy()

    # ============================================================
    # 1. DIMENSIONS
    # ============================================================

    # TEAM
    all_teams = pd.concat([df["home_team"], df["away_team"]]).drop_duplicates().sort_values()
    team_df = pd.DataFrame({
        "id_team": range(1, len(all_teams) + 1),
        "team_name": all_teams
    })
    team_map = dict(zip(team_df["team_name"], team_df["id_team"]))

    # CITY
    city_df, city_map = generate_dimension_table(df, "city")

    # STADIUM
    stadium_df, stadium_map = generate_dimension_table(df, "stadium")

    # EDITION
    edition_df, edition_map = generate_dimension_table(df, "edition")

    # ============================================================
    # 2. MAPPINGS
    # ============================================================

    apply_mapping(df, "home_team", team_map, "id_home_team")
    apply_mapping(df, "away_team", team_map, "id_away_team")
    apply_mapping(df, "city", city_map, "id_city")
    apply_mapping(df, "stadium", stadium_map, "id_stadium")
    apply_mapping(df, "edition", edition_map, "id_edition")

    # ============================================================
    # 3. AJOUT DE id_city DANS LA DIMENSION STADIUM
    # ============================================================

    # On récupère pour chaque stade la ville correspondante
    stadium_city_map = df.drop_duplicates(subset=["stadium"])[["stadium", "id_city"]]
    stadium_city_map = dict(zip(stadium_city_map["stadium"], stadium_city_map["id_city"]))

    stadium_df["id_city"] = stadium_df["stadium"].map(stadium_city_map)

    # ============================================================
    # 4. TABLE DE FAITS MATCH
    # ============================================================

    match_df = df[[
        "date",
        "round",
        "home_result",
        "away_result",
        "result",
        "id_home_team",
        "id_away_team",
        "id_stadium",
        "id_edition"
    ]].copy()

    # ============================================================
    # 5. DEBUG OPTIONNEL
    # ============================================================

    missing_scores = df[df["home_result"].isna() | df["away_result"].isna()]
    print("Lignes avec score manquant :", len(missing_scores))

    missing_away = df[df["id_away_team"].isna()]
    if len(missing_away) > 0:
        print("⚠️ Équipes away_team non mappées :", len(missing_away))
        print(missing_away[["away_team", "home_team", "edition", "round"]].head(20))
        raise ValueError("Certaines équipes away_team n'ont pas été mappées.")

    missing_home = df[df["id_home_team"].isna()]
    if len(missing_home) > 0:
        print("⚠️ Équipes home_team non mappées :", len(missing_home))
        print(missing_home[["home_team", "away_team", "edition", "round"]].head(20))
        raise ValueError("Certaines équipes home_team n'ont pas été mappées.")

    logger.info("Transformation terminée. Tables prêtes pour le chargement MySQL.")

    # ============================================================
    # 6. RETOUR DES TABLES
    # ============================================================

    return {
        "team": team_df,
        "city": city_df.rename(columns={"city": "city_name"}),
        "stadium": stadium_df.rename(columns={
            "stadium": "stadium_name",
            "id_city": "id_city"
        }),
        "edition": edition_df.rename(columns={"edition": "edition_name"}),
        "match": match_df
    }
