---

# 🟦 1) `conn = mysql.connector.connect(**config)`  
### 👉 Pourquoi le `**` ?

Le `**` en Python signifie :  
> **déballer un dictionnaire en arguments nommés**.

Autrement dit, si tu as :

```python
config = {
    "host": "localhost",
    "user": "alexandre",
    "password": "mon_mdp",
    "database": "foot"
}
```

Alors :

```python
mysql.connector.connect(**config)
```

est équivalent à écrire :

```python
mysql.connector.connect(
    host="localhost",
    user="alexandre",
    password="mon_mdp",
    database="foot"
)
```

### ✔ Pourquoi c’est utile ?

- ton code est plus propre  
- tu peux charger la config depuis un fichier YAML  
- tu peux changer les paramètres sans modifier le code  
- tu peux réutiliser la fonction dans d’autres projets  

### ✔ En résumé

`**config` = *“prends chaque clé du dictionnaire et utilise-la comme argument nommé”*.

---

# 🟦 2) Le bloc d’insertion SQL  

```python
placeholders = ", ".join(["%s"] * len(df.columns))
columns = ", ".join(df.columns)
sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

data = [tuple(row) for row in df.to_numpy()]

cursor.executemany(sql, data)
```

Explication **ligne par ligne**, avec un exemple concret.

---

# 🟦 2.1 `placeholders = ", ".join(["%s"] * len(df.columns))`

Supposons que la table TEAM ait 2 colonnes :

```
id_team, team_name
```

Alors :

```python
["%s"] * len(df.columns)
```

devient :

```python
["%s", "%s"]
```

Puis :

```python
", ".join(["%s", "%s"])
```

donne :

```
"%s, %s"
```

👉 Ce sont les **valeurs paramétrées** pour la requête SQL.

---

# 🟦 2.2 `columns = ", ".join(df.columns)`

Avec les colonnes :

```
["id_team", "team_name"]
```

on obtient :

```
"id_team, team_name"
```

---

# 🟦 2.3 Construction de la requête SQL

```python
sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
```

Avec `table_name = "team"` :

On obtient :

```
INSERT INTO team (id_team, team_name) VALUES (%s, %s)
```

👉 C’est une requête **préparée**, sécurisée, compatible MySQL.

---

# 🟦 2.4 Conversion du DataFrame en tuples Python

```python
data = [tuple(row) for row in df.to_numpy()]
```

Supposons que le DataFrame TEAM soit :

| id_team | team_name |
|---------|-----------|
| 1       | France    |
| 2       | Mexico    |
| 3       | Belgium   |

Alors :

```python
df.to_numpy()
```

donne :

```
[
  [1, "France"],
  [2, "Mexico"],
  [3, "Belgium"]
]
```

Puis :

```python
tuple(row)
```

donne :

```
(1, "France")
(2, "Mexico")
(3, "Belgium")
```

Donc `data` devient :

```python
[
  (1, "France"),
  (2, "Mexico"),
  (3, "Belgium")
]
```

👉 C’est exactement ce que `executemany()` attend.

---

# 🟦 2.5 Exécution de l’insertion

```python
cursor.executemany(sql, data)
```

MySQL exécute :

```
INSERT INTO team (id_team, team_name) VALUES (1, "France")
INSERT INTO team (id_team, team_name) VALUES (2, "Mexico")
INSERT INTO team (id_team, team_name) VALUES (3, "Belgium")
```

en **un seul appel**, ce qui est :

- plus rapide  
- plus propre  
- plus robuste  
- transactionnel  

---

# 🟩 Résumé clair pour ton dossier `docs/`

### ✔ `**config`  
→ déballage d’un dictionnaire en arguments nommés  
→ permet d’appeler `mysql.connector.connect()` proprement

### ✔ placeholders  
→ génère `%s, %s, %s, ...` selon le nombre de colonnes

### ✔ columns  
→ génère `id_team, team_name, ...`

### ✔ sql  
→ construit une requête SQL paramétrée

### ✔ data  
→ transforme le DataFrame en liste de tuples

### ✔ executemany  
→ exécute toutes les insertions en une seule fois

---

Parfait Alexandre — je te prépare **les deux éléments demandés** :

1) **Le schéma visuel du pipeline LOAD** (clair, propre, intégrable dans `docs/load_mysql_explained.md`)  
2) **Le fichier `main.py` complet**, structuré, professionnel, avec docstrings en français et parfaitement aligné avec ton ETL.

Je garde ton style : clair, modulaire, pédagogique, prêt pour un jury.

---

# 🟦 3) Schéma visuel du pipeline LOAD (ASCII, prêt à coller dans docs)

Voici un schéma **simple, lisible, et professionnel**, montrant exactement ce que fait `load_mysql.py` :

```
                          ┌──────────────────────────────┐
                          │   tables (dict de DataFrames) │
                          │  team / city / stadium / ...  │
                          └───────────────┬──────────────┘
                                          │
                                          ▼
                             ┌────────────────────────┐
                             │   load_all_tables()    │
                             │  (module load_mysql)   │
                             └─────────────┬──────────┘
                                           │
                                           ▼
                         ┌──────────────────────────────────┐
                         │   get_connection(config)         │
                         │   → Connexion MySQL              │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │   Début de transaction           │
                         │   conn.start_transaction()       │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
        ┌──────────────────────────────────────────────────────────────────────┐
        │                     INSERTION DES DIMENSIONS                          │
        │                                                                        │
        │  insert_dataframe(cursor, "team",    tables["team"])                  │
        │  insert_dataframe(cursor, "city",    tables["city"])                  │
        │  insert_dataframe(cursor, "stadium", tables["stadium"])               │
        │  insert_dataframe(cursor, "edition", tables["edition"])               │
        └──────────────────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │   INSERTION DE LA TABLE DE FAITS │
                         │   insert_dataframe(cursor, "match") │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │   COMMIT si tout est OK          │
                         │   ROLLBACK si erreur             │
                         └──────────────────┬───────────────┘
                                            │
                                            ▼
                         ┌──────────────────────────────────┐
                         │   Fermeture curseur + connexion  │
                         └──────────────────────────────────┘
```

Ce schéma montre :

- l’ordre d’insertion  
- la logique transactionnelle  
- la séparation dimensions / faits  
- la structure du module  

---