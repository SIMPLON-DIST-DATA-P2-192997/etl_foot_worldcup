# Schéma visuel complet du pipeline ETL  

```
                           ┌──────────────────────────────┐
                           │  data_clean/matches_1930_2022 │
                           │          (CSV final)          │
                           └───────────────┬──────────────┘
                                           │
                                           ▼
                         ┌──────────────────────────────────┐
                         │          extract_matches          │
                         │        (module extract.py)        │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │        DataFrame Pandas          │
                         │  (colonnes brutes nettoyées)     │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │        transform_matches          │
                         │       (module transform.py)       │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │                         Génération des dimensions                         │
        │  team_df      ← generate_dimension_table("home_team")                     │
        │  city_df      ← generate_dimension_table("city")                          │
        │  stadium_df   ← generate_dimension_table("stadium")                       │
        │  edition_df   ← generate_dimension_table("edition")                       │
        └──────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │                     Application des mappings (apply_mapping)             │
        │  df["id_home_team"]   ← map(team_map)                                    │
        │  df["id_away_team"]   ← map(team_map)                                    │
        │  df["id_city"]        ← map(city_map)                                    │
        │  df["id_stadium"]     ← map(stadium_map)                                 │
        │  df["id_edition"]     ← map(edition_map)                                 │
        └──────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │        Construction match_df      │
                         │   (table de faits normalisée)     │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │   Dictionnaire final des tables   │
                         │  {team, city, stadium, edition,   │
                         │           match}                  │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │          load_all_tables          │
                         │       (module load_mysql.py)      │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
        ┌──────────────────────────────────────────────────────────────────────────┐
        │                     Insertion MySQL (transactionnelle)                   │
        │  1. INSERT team                                                         │
        │  2. INSERT city                                                         │
        │  3. INSERT stadium                                                      │
        │  4. INSERT edition                                                      │
        │  5. INSERT match                                                        │
        │  COMMIT si OK / ROLLBACK si erreur                                      │
        └──────────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │         Base MySQL "foot"         │
                         │   (tables remplies et cohérentes) │
                         └──────────────────────────────────┘
```

Ce schéma est **parfait pour ton dossier docs/** et pour ton oral.

---