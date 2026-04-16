---

# 🟦 1) Dataset d’entrée (référence : entrée de `transform_matches`)  
*(Correspond à la ligne : `def transform_matches(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:`)*

Mini‑exemple :

| home_team | away_team | home_result | away_result | result | date       | round        | city      | stadium        | edition      |
|-----------|-----------|-------------|-------------|--------|------------|--------------|-----------|----------------|--------------|
| France    | Mexico    | 4           | 1           | home   | 1930-07-13 | Group stage  | Montevideo | Pocitos        | 1930-URUGUAY |
| USA       | Belgium   | 3           | 0           | home   | 1930-07-13 | Group stage  | Montevideo | Centenario     | 1930-URUGUAY |
| France    | Belgium   | 3           | 0           | home   | 1930-07-17 | Group stage  | Montevideo | Centenario     | 1930-URUGUAY |

---

# 🟦 2) Génération des dimensions  
*(Référence : fonctions `generate_dimension_table` et appels dans `transform_matches`)*

---

## 🔵 2.1 Dimension TEAM  
*(Référence : `team_df, team_map = generate_dimension_table(df, "home_team")`)*

Valeurs uniques triées :

```
["Belgium", "France", "Mexico", "USA"]
```

Table générée :

| id_home_team | home_team |
|--------------|-----------|
| 1            | Belgium   |
| 2            | France    |
| 3            | Mexico    |
| 4            | USA       |

Mapping :

```python
{"Belgium": 1, "France": 2, "Mexico": 3, "USA": 4}
```

---

## 🔵 2.2 Dimension CITY  
*(Référence : `city_df, city_map = generate_dimension_table(df, "city")`)*

Valeurs uniques :

```
["Montevideo"]
```

Table :

| id_city | city       |
|---------|------------|
| 1       | Montevideo |

Mapping :

```python
{"Montevideo": 1}
```

---

## 🔵 2.3 Dimension STADIUM  
*(Référence : `stadium_df, stadium_map = generate_dimension_table(df, "stadium")`)*

Valeurs uniques triées :

```
["Centenario", "Pocitos"]
```

Table :

| id_stadium | stadium    |
|------------|------------|
| 1          | Centenario |
| 2          | Pocitos    |

Mapping :

```python
{"Centenario": 1, "Pocitos": 2}
```

---

## 🔵 2.4 Dimension EDITION  
*(Référence : `edition_df, edition_map = generate_dimension_table(df, "edition")`)*

Valeurs uniques :

```
["1930-URUGUAY"]
```

Table :

| id_edition | edition        |
|------------|----------------|
| 1          | 1930-URUGUAY   |

Mapping :

```python
{"1930-URUGUAY": 1}
```

---

# 🟦 3) Application des mappings  
*(Référence : appels successifs à `apply_mapping` dans `transform_matches`)*

---

## 🔵 3.1 Mapping des équipes  
*(Référence : `apply_mapping(df, "home_team", team_map, "id_home_team")`)*

| home_team | id_home_team |
|-----------|--------------|
| France    | 2            |
| USA       | 4            |
| France    | 2            |

*(Référence : `apply_mapping(df, "away_team", team_map, "id_away_team")`)*

| away_team | id_away_team |
|-----------|--------------|
| Mexico    | 3            |
| Belgium   | 1            |
| Belgium   | 1            |

---

## 🔵 3.2 Mapping des villes  
*(Référence : `apply_mapping(df, "city", city_map, "id_city")`)*

| city       | id_city |
|------------|---------|
| Montevideo | 1       |
| Montevideo | 1       |
| Montevideo | 1       |

---

## 🔵 3.3 Mapping des stades  
*(Référence : `apply_mapping(df, "stadium", stadium_map, "id_stadium")`)*

| stadium    | id_stadium |
|------------|------------|
| Pocitos    | 2          |
| Centenario | 1          |
| Centenario | 1          |

---

## 🔵 3.4 Mapping des éditions  
*(Référence : `apply_mapping(df, "edition", edition_map, "id_edition")`)*

| edition        | id_edition |
|----------------|------------|
| 1930-URUGUAY   | 1          |
| 1930-URUGUAY   | 1          |
| 1930-URUGUAY   | 1          |

---

# 🟦 4) Construction de la table de faits  
*(Référence : bloc final dans `transform_matches`)*

On sélectionne :

```
date, round, home_result, away_result, result,
id_home_team, id_away_team, id_stadium, id_edition
```

Résultat :

| date       | round        | home_result | away_result | result | id_home_team | id_away_team | id_stadium | id_edition |
|------------|--------------|-------------|-------------|--------|--------------|--------------|------------|------------|
| 1930-07-13 | Group stage  | 4           | 1           | home   | 2            | 3            | 2          | 1          |
| 1930-07-13 | Group stage  | 3           | 0           | home   | 4            | 1            | 1          | 1          |
| 1930-07-17 | Group stage  | 3           | 0           | home   | 2            | 1            | 1          | 1          |

---

# 🟦 5) Schéma visuel (ASCII)  
*(Tu peux le mettre dans `docs/etl_transform_schema.txt`)*

```
                ┌──────────────────────────────┐
                │  matches_1930_2022_clean.csv │
                └───────────────┬──────────────┘
                                │
                                ▼
                    ┌────────────────────┐
                    │  transform_matches │
                    └──────────┬─────────┘
                               │
     ┌─────────────────────────┼─────────────────────────┐
     ▼                         ▼                         ▼
┌──────────┐            ┌──────────┐              ┌──────────┐
│ generate │            │ generate │              │ generate │
│  team    │            │  city    │              │ stadium  │
└────┬─────┘            └────┬─────┘              └────┬─────┘
     │                       │                           │
     ▼                       ▼                           ▼
┌──────────┐            ┌──────────┐              ┌──────────┐
│ team_df  │            │ city_df  │              │stadium_df│
└────┬─────┘            └────┬─────┘              └────┬─────┘
     │                       │                           │
     └──────────────┬────────┴──────────────┬────────────┘
                    ▼                       ▼
               ┌──────────┐           ┌──────────┐
               │ generate │           │ generate │
               │ edition  │           │ mappings │
               └────┬─────┘           └────┬─────┘
                    │                       │
                    ▼                       ▼
               ┌──────────┐           ┌──────────┐
               │edition_df│           │ apply_*  │
               └────┬─────┘           └────┬─────┘
                    │                       │
                    └──────────────┬────────┘
                                   ▼
                         ┌────────────────┐
                         │   match_df     │
                         └────────────────┘
```

---

# 🟩 Résultat final : ce que renvoie `transform.py`

Un dictionnaire :

```python
{
  "team": df_team,
  "city": df_city,
  "stadium": df_stadium,
  "edition": df_edition,
  "match": df_match
}
```

---

# 🟦 1) Rappel du cœur du mécanisme

Les trois lignes essentielles :

```python
unique_values = sorted(df[column_name].drop_duplicates().fillna("UNKNOWN"))

dim_df = pd.DataFrame({
    f"id_{column_name}": range(1, len(unique_values) + 1),
    column_name: unique_values
})

mapping = dict(zip(unique_values, dim_df[f"id_{column_name}"]))
```

Elles font trois choses :

---

## ✔ Étape 1 — Extraire les valeurs uniques triées  
Exemple pour `home_team` :

```
["Belgium", "France", "Mexico", "USA"]
```

---

## ✔ Étape 2 — Créer une table dimensionnelle avec des IDs

| id_home_team | home_team |
|--------------|-----------|
| 1            | Belgium   |
| 2            | France    |
| 3            | Mexico    |
| 4            | USA       |

---

## ✔ Étape 3 — Construire un dictionnaire de mapping

```python
{
  "Belgium": 1,
  "France": 2,
  "Mexico": 3,
  "USA": 4
}
```

---

# 🟦 2) La ligne clé : `df[new_col] = df[column_name].map(mapping)`

---

## 🔵 Exemple concret

Supposons que le DataFrame principal contienne :

| home_team |
|-----------|
| France    |
| Mexico    |
| USA       |

Et que le mapping soit :

```python
{"Belgium": 1, "France": 2, "Mexico": 3, "USA": 4}
```

Alors :

```python
df["id_home_team"] = df["home_team"].map(mapping)
```

produit :

| home_team | id_home_team |
|-----------|--------------|
| France    | 2            |
| Mexico    | 3            |
| USA       | 4            |

👉 **La nouvelle colonne correspond exactement à la colonne `id_home_team` de la dimension TEAM.**

---

# 🟦 3) Pourquoi ça fonctionne si bien ?

Parce que :

- `mapping` associe chaque valeur textuelle à son identifiant entier  
- `.map(mapping)` remplace chaque valeur par son ID  
- `df[new_col]` crée une nouvelle colonne dans le DataFrame principal  
- `new_col` est toujours de la forme `id_<dimension>`

Donc :

### ✔ `home_team` → `id_home_team`  
### ✔ `away_team` → `id_away_team`  
### ✔ `city` → `id_city`  
### ✔ `stadium` → `id_stadium`  
### ✔ `edition` → `id_edition`

---

# 🟦 4) Visualisation complète (mini‑exemple)

### Avant mapping :

| home_team | away_team | city       | stadium    | edition        |
|-----------|-----------|------------|------------|----------------|
| France    | Mexico    | Montevideo | Pocitos    | 1930-URUGUAY   |

### Après mapping :

| home_team | away_team | id_home_team | id_away_team | id_city | id_stadium | id_edition |
|-----------|-----------|--------------|--------------|---------|------------|------------|
| France    | Mexico    | 2            | 3            | 1       | 2          | 1          |

---

# 🟩 5) Conclusion claire

👉 **Oui : la nouvelle colonne créée par `.map(mapping)` correspond exactement à la colonne d’identifiants de la table dimensionnelle.**

👉 C’est ce qui permet ensuite d’insérer proprement dans MySQL :

- d’abord les dimensions  
- puis la table `match` avec les FK correctes  

👉 C’est aussi ce qui garantit la cohérence entre le MLD, le schéma SQL et l'ETL.

---