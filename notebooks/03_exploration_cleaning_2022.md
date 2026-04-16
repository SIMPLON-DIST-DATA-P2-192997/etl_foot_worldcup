### **Imports + configuration**


```python
import pandas as pd
import numpy as np
import json
from pathlib import Path

DATA_RAW = Path("..") / "data_raw"

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
```

### **Chargement du JSON**


```python
with open(DATA_RAW / "worldcup_2022.json", encoding="utf-8") as f:
    data_2022 = json.load(f)
```

### **Inspection de la structure**


```python
print("Clés principales :", data_2022.keys())
print("Nombre de matchs :", len(data_2022["matches"]))
print("Exemple d'un match :")
data_2022["matches"][0]
```

    Clés principales : dict_keys(['name', 'matches'])
    Nombre de matchs : 64
    Exemple d'un match :





    {'round': 'Matchday 1',
     'date': '2022-11-20',
     'time': '19:00',
     'team1': 'Qatar',
     'team2': 'Ecuador',
     'score': {'ft': [0, 2], 'ht': [0, 2]},
     'goals1': [],
     'goals2': [{'name': 'Enner Valencia', 'minute': 16, 'penalty': True},
      {'name': 'Enner Valencia', 'minute': 31}],
     'group': 'Group A',
     'ground': 'Al Bayt Stadium, Al Khor'}



### **Construction du DataFrame brut**


```python
df_2022_raw = pd.DataFrame(data_2022["matches"])
df_2022_raw.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>round</th>
      <th>date</th>
      <th>time</th>
      <th>team1</th>
      <th>team2</th>
      <th>score</th>
      <th>goals1</th>
      <th>goals2</th>
      <th>group</th>
      <th>ground</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Matchday 1</td>
      <td>2022-11-20</td>
      <td>19:00</td>
      <td>Qatar</td>
      <td>Ecuador</td>
      <td>{'ft': [0, 2], 'ht': [0, 2]}</td>
      <td>[]</td>
      <td>[{'name': 'Enner Valencia', 'minute': 16, 'pen...</td>
      <td>Group A</td>
      <td>Al Bayt Stadium, Al Khor</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Matchday 2</td>
      <td>2022-11-21</td>
      <td>19:00</td>
      <td>Senegal</td>
      <td>Netherlands</td>
      <td>{'ft': [0, 2], 'ht': [0, 0]}</td>
      <td>[]</td>
      <td>[{'name': 'Cody Gakpo', 'minute': 84}, {'name'...</td>
      <td>Group A</td>
      <td>Al Thumama Stadium, Doha</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Matchday 6</td>
      <td>2022-11-25</td>
      <td>16:00</td>
      <td>Qatar</td>
      <td>Senegal</td>
      <td>{'ft': [1, 3], 'ht': [0, 1]}</td>
      <td>[{'name': 'Mohammed Muntari', 'minute': 78}]</td>
      <td>[{'name': 'Boulaye Dia', 'minute': 41}, {'name...</td>
      <td>Group A</td>
      <td>Al Thumama Stadium, Doha</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Matchday 6</td>
      <td>2022-11-25</td>
      <td>19:00</td>
      <td>Netherlands</td>
      <td>Ecuador</td>
      <td>{'ft': [1, 1], 'ht': [1, 0]}</td>
      <td>[{'name': 'Cody Gakpo', 'minute': 6}]</td>
      <td>[{'name': 'Enner Valencia', 'minute': 49}]</td>
      <td>Group A</td>
      <td>Khalifa International Stadium, Al Rayyan</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Matchday 10</td>
      <td>2022-11-29</td>
      <td>18:00</td>
      <td>Ecuador</td>
      <td>Senegal</td>
      <td>{'ft': [1, 2], 'ht': [0, 1]}</td>
      <td>[{'name': 'Moisés Caicedo', 'minute': 67}]</td>
      <td>[{'name': 'Ismaila Sarr', 'minute': 44, 'penal...</td>
      <td>Group A</td>
      <td>Khalifa International Stadium, Al Rayyan</td>
    </tr>
  </tbody>
</table>
</div>



### **Extraction des scores**


```python
"""
Extraction des scores à partir de la structure :
"score": {"ft": [home, away], ...}

Certaines entrées contiennent aussi :
- "ht" (half-time)
- "et" (extra time)
- "p"  (penalties)

Nous utilisons uniquement "ft" (full time) pour harmoniser avec 1930–2018.
"""

df_2022_raw["home_result"] = df_2022_raw["score"].apply(lambda s: s.get("ft", [None, None])[0])
df_2022_raw["away_result"] = df_2022_raw["score"].apply(lambda s: s.get("ft", [None, None])[1])
```

### **Extraction du stade et de la ville**


```python
"""
La colonne "ground" contient une chaîne du type :
"Al Bayt Stadium, Al Khor"

Nous séparons :
- stadium = "Al Bayt Stadium"
- city    = "Al Khor"
"""

df_2022_raw["stadium"] = df_2022_raw["ground"].apply(lambda g: g.split(",")[0].strip())
df_2022_raw["city"] = df_2022_raw["ground"].apply(lambda g: g.split(",")[1].strip())
```

### **Construction de la colonne datetime**


```python
df_2022_raw["date"] = pd.to_datetime(df_2022_raw["date"] + " " + df_2022_raw["time"])
```

### **Extraction du vainqueur**


```python
def compute_result_2022(row):
    """
    Détermine le vainqueur d'un match de la Coupe du Monde 2022.

    Paramètres
    ----------
    row : pd.Series
        Ligne du DataFrame contenant :
        - home_result : buts de l'équipe 1
        - away_result : buts de l'équipe 2
        - team1       : nom de l'équipe 1
        - team2       : nom de l'équipe 2

    Retour
    ------
    str
        Nom de l'équipe gagnante.
        Retourne 'draw' en cas d'égalité.
    """
    if row["home_result"] > row["away_result"]:
        return row["team1"]
    elif row["home_result"] < row["away_result"]:
        return row["team2"]
    else:
        return "draw"

df_2022_raw["result"] = df_2022_raw.apply(compute_result_2022, axis=1)
```

### **Suppression des colonnes non scalaires**


```python
cols_to_drop = ["score", "goals1", "goals2", "ground"]

df_2022_raw = df_2022_raw.drop(columns=[c for c in cols_to_drop if c in df_2022_raw.columns])
```

### **Construction du DataFrame final**


```python
df_final_2022 = pd.DataFrame({
    "home_team": df_2022_raw["team1"],
    "away_team": df_2022_raw["team2"],
    "home_result": df_2022_raw["home_result"],
    "away_result": df_2022_raw["away_result"],
    "result": df_2022_raw["result"],
    "date": df_2022_raw["date"],
    "round": df_2022_raw["round"],
    "city": df_2022_raw["city"],
    "stadium": df_2022_raw["stadium"],
    "edition": "2022-QATAR"
})

df_final_2022.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>home_team</th>
      <th>away_team</th>
      <th>home_result</th>
      <th>away_result</th>
      <th>result</th>
      <th>date</th>
      <th>round</th>
      <th>city</th>
      <th>stadium</th>
      <th>edition</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>Qatar</td>
      <td>Ecuador</td>
      <td>0</td>
      <td>2</td>
      <td>Ecuador</td>
      <td>2022-11-20 19:00:00</td>
      <td>Matchday 1</td>
      <td>Al Khor</td>
      <td>Al Bayt Stadium</td>
      <td>2022-QATAR</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Senegal</td>
      <td>Netherlands</td>
      <td>0</td>
      <td>2</td>
      <td>Netherlands</td>
      <td>2022-11-21 19:00:00</td>
      <td>Matchday 2</td>
      <td>Doha</td>
      <td>Al Thumama Stadium</td>
      <td>2022-QATAR</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Qatar</td>
      <td>Senegal</td>
      <td>1</td>
      <td>3</td>
      <td>Senegal</td>
      <td>2022-11-25 16:00:00</td>
      <td>Matchday 6</td>
      <td>Doha</td>
      <td>Al Thumama Stadium</td>
      <td>2022-QATAR</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Netherlands</td>
      <td>Ecuador</td>
      <td>1</td>
      <td>1</td>
      <td>draw</td>
      <td>2022-11-25 19:00:00</td>
      <td>Matchday 6</td>
      <td>Al Rayyan</td>
      <td>Khalifa International Stadium</td>
      <td>2022-QATAR</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Ecuador</td>
      <td>Senegal</td>
      <td>1</td>
      <td>2</td>
      <td>Senegal</td>
      <td>2022-11-29 18:00:00</td>
      <td>Matchday 10</td>
      <td>Al Rayyan</td>
      <td>Khalifa International Stadium</td>
      <td>2022-QATAR</td>
    </tr>
  </tbody>
</table>
</div>



### **Vérifications de qualité**

#### **Inspection s'il y a des NaN**


```python
df_final_2022.isna().sum()
```




    home_team      0
    away_team      0
    home_result    0
    away_result    0
    result         0
    date           0
    round          0
    city           0
    stadium        0
    edition        0
    dtype: int64



#### **Inspection s'il y a des doublons**


```python
df_final_2022.duplicated().sum()
```




    np.int64(0)



#### **Vérification des types**


```python
df_final_2022.dtypes
```




    home_team                 str
    away_team                 str
    home_result             int64
    away_result             int64
    result                    str
    date           datetime64[us]
    round                     str
    city                      str
    stadium                   str
    edition                   str
    dtype: object



#### **Inspection s'il y a des scores négatifs**


```python
df_final_2022[df_final_2022["home_result"] < 0]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>home_team</th>
      <th>away_team</th>
      <th>home_result</th>
      <th>away_result</th>
      <th>result</th>
      <th>date</th>
      <th>round</th>
      <th>city</th>
      <th>stadium</th>
      <th>edition</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



#### **Inspection s'il y a des chaines mal formées**


```python
df_final_2022["home_team"].unique()[:20]

```




    <ArrowStringArray>
    [       'Qatar',      'Senegal',  'Netherlands',      'Ecuador',
          'England',          'USA',        'Wales',         'Iran',
        'Argentina',       'Mexico',       'Poland', 'Saudi Arabia',
          'Denmark',       'France',      'Tunisia',    'Australia',
          'Germany',        'Spain',        'Japan',   'Costa Rica']
    Length: 20, dtype: str




```python
df_final_2022["city"].unique()[:20]
```




    <ArrowStringArray>
    ['Al Khor', 'Doha', 'Al Rayyan', 'Lusail', 'Al Wakrah']
    Length: 5, dtype: str



#### **Inspection s'il y a des dates invalides**


```python
df_final_2022[df_final_2022["date"].isna()]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>home_team</th>
      <th>away_team</th>
      <th>home_result</th>
      <th>away_result</th>
      <th>result</th>
      <th>date</th>
      <th>round</th>
      <th>city</th>
      <th>stadium</th>
      <th>edition</th>
    </tr>
  </thead>
  <tbody>
  </tbody>
</table>
</div>



### **Export**


```python
DATA_CLEAN = Path("..") / "data_clean"

df_final_2022.to_csv(DATA_CLEAN / "matches_2022_clean.csv", index=False)
df_final_2022.to_parquet(DATA_CLEAN / "matches_2022_clean.parquet", index=False)
```


```python

```
