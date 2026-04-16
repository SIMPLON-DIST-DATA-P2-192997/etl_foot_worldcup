import pandas as pd
from etl.extract import extract_matches
from etl.transform import transform_matches


def test_extract_matches():
    """
    Vérifie que l'extraction charge bien un DataFrame
    et que les colonnes attendues sont présentes.
    """
    df = extract_matches("data_clean/matches_1930_2022_clean.csv")

    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0

    expected_cols = {
        "home_team", "away_team", "home_result", "away_result",
        "result", "date", "round", "city", "stadium", "edition"
    }

    assert expected_cols.issubset(df.columns)


def test_transform_matches_structure():
    """
    Vérifie que transform_matches renvoie bien un dictionnaire
    contenant les 5 tables attendues.
    """
    df = extract_matches("data_clean/matches_1930_2022_clean.csv")
    tables = transform_matches(df)

    expected_tables = {"team", "city", "stadium", "edition", "match"}

    assert set(tables.keys()) == expected_tables


def test_dimensions_have_ids():
    """
    Vérifie que chaque table dimensionnelle contient bien une colonne ID.
    """
    df = extract_matches("data_clean/matches_1930_2022_clean.csv")
    tables = transform_matches(df)

    assert "id_home_team" in tables["team"].columns or "id_team" in tables["team"].columns
    assert "id_city" in tables["city"].columns
    assert "id_stadium" in tables["stadium"].columns
    assert "id_edition" in tables["edition"].columns


def test_match_table_columns():
    """
    Vérifie que la table de faits contient les colonnes normalisées attendues.
    """
    df = extract_matches("data_clean/matches_1930_2022_clean.csv")
    tables = transform_matches(df)

    match_df = tables["match"]

    expected_cols = {
        "date", "round", "home_result", "away_result", "result",
        "id_home_team", "id_away_team", "id_stadium", "id_edition"
    }

    assert expected_cols.issubset(match_df.columns)
