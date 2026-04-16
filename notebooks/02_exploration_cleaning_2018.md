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
with open(DATA_RAW / "data_2018.json", encoding="utf-8") as f:
    data_2018 = json.load(f)
```

### **Inspection de la structure**


```python
print("Clés principales :", data_2018.keys())
print("Groupes :", data_2018["groups"].keys())
print("Knockout :", data_2018["knockout"].keys())
print("Exemple équipe :", data_2018["teams"][0])
print("Exemple stade :", data_2018["stadiums"][0])

```

    Clés principales : dict_keys(['stadiums', 'tvchannels', 'teams', 'groups', 'knockout'])
    Groupes : dict_keys(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'])
    Knockout : dict_keys(['round_16', 'round_8', 'round_4', 'round_2_loser', 'round_2'])
    Exemple équipe : {'id': 1, 'name': 'Russia', 'fifaCode': 'RUS', 'iso2': 'ru', 'flag': 'https://upload.wikimedia.org/wikipedia/en/thumb/f/f3/Flag_of_Russia.svg/900px-Flag_of_Russia.png', 'emoji': 'flag-ru', 'emojiString': '🇷🇺'}
    Exemple stade : {'id': 1, 'name': 'Luzhniki Stadium', 'city': 'Moscow', 'lat': 55.715765, 'lng': 37.5515217, 'image': 'https://upload.wikimedia.org/wikipedia/commons/e/e6/Luzhniki_Stadium%2C_Moscow.jpg'}


### **Extraction des matchs de groupes**


```python
"""
Extraction des matchs de la phase de groupes (Group Stage).

Structure du JSON :
data_2018["groups"] est un dictionnaire dont les clés sont 'a', 'b', ..., 'h'.
Chaque entrée contient :
    - group_info["name"] : nom du groupe (ex : "Group A")
    - group_info["matches"] : liste des matchs du groupe

Chaque match contient des IDs (home_team, away_team, stadium, etc.)
que nous résoudrons plus tard via les lookup tables.

Objectif :
Créer une liste 'matches_2018' contenant tous les matchs de groupes,
en ajoutant une clé 'round' pour harmoniser avec les autres datasets.
"""

matches_2018 = []

for group_key, group_info in data_2018["groups"].items():
    for match in group_info["matches"]:
        match["round"] = group_info["name"]  # ex: "Group A"
        matches_2018.append(match)
```

### **Extraction des matchs de phases finales**


```python
"""
Extraction des matchs de la phase finale (Knockout Stage).

Structure du JSON :
data_2018["knockout"] contient plusieurs clés :
    - 'round_16'        → Round of 16
    - 'round_8'         → Quarter-finals
    - 'round_4'         → Semi-finals
    - 'round_2_loser'   → Match pour la 3e place
    - 'round_2'         → Finale

Chaque entrée contient :
    - round_info["name"] : nom officiel du tour (ex : "Round of 16")
    - round_info["matches"] : liste des matchs

Objectif :
Ajouter tous les matchs de phases finales à la liste 'matches_2018',
avec une clé 'round' harmonisée.
"""

for round_key, round_info in data_2018["knockout"].items():
    round_name = round_info["name"] if "name" in round_info else round_key
    for match in round_info["matches"]:
        match["round"] = round_name  # ex: "Round of 16"
        matches_2018.append(match)
```

### **Construction du DataFrame brut**


```python
df_2018_raw = pd.DataFrame(matches_2018)
df_2018_raw.head()
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
      <th>name</th>
      <th>type</th>
      <th>home_team</th>
      <th>away_team</th>
      <th>home_result</th>
      <th>away_result</th>
      <th>date</th>
      <th>stadium</th>
      <th>channels</th>
      <th>finished</th>
      <th>matchday</th>
      <th>round</th>
      <th>home_penalty</th>
      <th>away_penalty</th>
      <th>winner</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>group</td>
      <td>1</td>
      <td>2</td>
      <td>5</td>
      <td>0</td>
      <td>2018-06-14T18:00:00+03:00</td>
      <td>1</td>
      <td>[4, 6, 13, 17, 20, 22]</td>
      <td>True</td>
      <td>1</td>
      <td>Group A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>group</td>
      <td>3</td>
      <td>4</td>
      <td>0</td>
      <td>1</td>
      <td>2018-06-15T17:00:00+05:00</td>
      <td>12</td>
      <td>[3, 6, 14, 17, 20, 22]</td>
      <td>True</td>
      <td>1</td>
      <td>Group A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>17</td>
      <td>group</td>
      <td>1</td>
      <td>3</td>
      <td>3</td>
      <td>1</td>
      <td>2018-06-19T21:00:00+03:00</td>
      <td>3</td>
      <td>[3, 6, 13, 17, 15, 21, 22]</td>
      <td>True</td>
      <td>2</td>
      <td>Group A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>18</td>
      <td>group</td>
      <td>4</td>
      <td>2</td>
      <td>1</td>
      <td>0</td>
      <td>2018-06-20T18:00:00+03:00</td>
      <td>10</td>
      <td>[3, 6, 13, 17, 21, 22]</td>
      <td>True</td>
      <td>2</td>
      <td>Group A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>33</td>
      <td>group</td>
      <td>4</td>
      <td>1</td>
      <td>3</td>
      <td>0</td>
      <td>2018-06-25T18:00:00+04:00</td>
      <td>7</td>
      <td>[4, 6, 13, 18, 15, 20, 22]</td>
      <td>True</td>
      <td>3</td>
      <td>Group A</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
</div>




```python
df_2018_raw.info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 64 entries, 0 to 63
    Data columns (total 15 columns):
     #   Column        Non-Null Count  Dtype  
    ---  ------        --------------  -----  
     0   name          64 non-null     int64  
     1   type          64 non-null     str    
     2   home_team     64 non-null     int64  
     3   away_team     64 non-null     int64  
     4   home_result   64 non-null     int64  
     5   away_result   64 non-null     int64  
     6   date          64 non-null     str    
     7   stadium       64 non-null     int64  
     8   channels      64 non-null     object 
     9   finished      64 non-null     bool   
     10  matchday      64 non-null     int64  
     11  round         64 non-null     str    
     12  home_penalty  4 non-null      float64
     13  away_penalty  4 non-null      float64
     14  winner        16 non-null     float64
    dtypes: bool(1), float64(3), int64(7), object(1), str(3)
    memory usage: 9.6+ KB


### **Lookup tables (tables de recherche : équipes + stades)**


```python
teams_lookup = {team["id"]: team["name"] for team in data_2018["teams"]}

stadiums_lookup = {
    stadium["id"]: {
        "stadium": stadium["name"],
        "city": stadium["city"]
    }
    for stadium in data_2018["stadiums"]
}
```

### **Remplacement des IDs dans df_2018_raw (équipes + stades)**


```python
# Remplacement des équipes
df_2018_raw["home_team"] = df_2018_raw["home_team"].map(teams_lookup)
df_2018_raw["away_team"] = df_2018_raw["away_team"].map(teams_lookup)

# Création des colonnes stade + ville
df_2018_raw["stadium_name"] = df_2018_raw["stadium"].map(lambda x: stadiums_lookup[x]["stadium"])
df_2018_raw["city"] = df_2018_raw["stadium"].map(lambda x: stadiums_lookup[x]["city"])

# Suppression de l’ancienne colonne stadium (ID)
df_2018_raw = df_2018_raw.drop(columns=["stadium"])

# Renommage propre
df_2018_raw = df_2018_raw.rename(columns={"stadium_name": "stadium"})
```

### **Conversion des dates**


```python
df_2018_raw["date"] = pd.to_datetime(df_2018_raw["date"], utc=True)
df_2018_raw["date"] = df_2018_raw["date"].dt.tz_convert(None)
```

### **Extraction du vainqueur**


```python
def compute_result_2018(row):
    """
    Détermine le vainqueur d'un match de la Coupe du Monde 2018.

    Paramètres
    ----------
    row : pd.Series
        Ligne du DataFrame contenant :
        - home_result : buts de l'équipe à domicile
        - away_result : buts de l'équipe à l'extérieur
        - home_team   : nom de l'équipe à domicile
        - away_team   : nom de l'équipe à l'extérieur

    Retour
    ------
    str
        Nom de l'équipe gagnante.
        Retourne 'draw' en cas d'égalité.
    """
    if row["home_result"] > row["away_result"]:
        return row["home_team"]
    elif row["home_result"] < row["away_result"]:
        return row["away_team"]
    else:
        return "draw"

df_2018_raw["result"] = df_2018_raw.apply(compute_result_2018, axis=1)
```

### **Suppression des colonnes non scalaires**


```python
cols_to_drop = ["channels", "home_penalty", "away_penalty", "winner"]

df_2018_raw = df_2018_raw.drop(columns=[c for c in cols_to_drop if c in df_2018_raw.columns])
```

### **Construction du DataFrame final**


```python
df_final_2018 = pd.DataFrame({
    "home_team": df_2018_raw["home_team"],
    "away_team": df_2018_raw["away_team"],
    "home_result": df_2018_raw["home_result"],
    "away_result": df_2018_raw["away_result"],
    "result": df_2018_raw["result"],
    "date": df_2018_raw["date"],
    "round": df_2018_raw["round"],
    "city": df_2018_raw["city"],
    "stadium": df_2018_raw["stadium"],
    "edition": "2018-RUSSIA"
})

df_final_2018.head()
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
      <td>Russia</td>
      <td>Saudi Arabia</td>
      <td>5</td>
      <td>0</td>
      <td>Russia</td>
      <td>2018-06-14 15:00:00</td>
      <td>Group A</td>
      <td>Moscow</td>
      <td>Luzhniki Stadium</td>
      <td>2018-RUSSIA</td>
    </tr>
    <tr>
      <th>1</th>
      <td>Egypt</td>
      <td>Uruguay</td>
      <td>0</td>
      <td>1</td>
      <td>Uruguay</td>
      <td>2018-06-15 12:00:00</td>
      <td>Group A</td>
      <td>Yekaterinburg</td>
      <td>Central Stadium</td>
      <td>2018-RUSSIA</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Russia</td>
      <td>Egypt</td>
      <td>3</td>
      <td>1</td>
      <td>Russia</td>
      <td>2018-06-19 18:00:00</td>
      <td>Group A</td>
      <td>Saint Petersburg</td>
      <td>Krestovsky Stadium</td>
      <td>2018-RUSSIA</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Uruguay</td>
      <td>Saudi Arabia</td>
      <td>1</td>
      <td>0</td>
      <td>Uruguay</td>
      <td>2018-06-20 15:00:00</td>
      <td>Group A</td>
      <td>Rostov-on-Don</td>
      <td>Rostov Arena</td>
      <td>2018-RUSSIA</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Uruguay</td>
      <td>Russia</td>
      <td>3</td>
      <td>0</td>
      <td>Uruguay</td>
      <td>2018-06-25 14:00:00</td>
      <td>Group A</td>
      <td>Samara</td>
      <td>Cosmos Arena</td>
      <td>2018-RUSSIA</td>
    </tr>
  </tbody>
</table>
</div>



### **Vérifications de qualité du dataset**

#### **Inspection s'il y a des NaN**


```python
df_final_2018.isna().sum()
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



#### **Inspection s'il y a des Doublons**


```python
df_final_2018.duplicated().sum()
```




    np.int64(0)



#### **Vérification des types des colonnes**


```python
df_final_2018.dtypes
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



#### **Inspection s'il y a des valeurs incohérentes (ex : scores négatifs)**


```python
df_final_2018[df_final_2018["home_result"] < 0]
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



#### **Inspection s'il y a des chaînes mal formées (espaces, accents, etc.)**


```python
df_final_2018["home_team"].unique()[:20]
df_final_2018["city"].unique()[:20]
```




    <ArrowStringArray>
    [          'Moscow',    'Yekaterinburg', 'Saint Petersburg',
        'Rostov-on-Don',           'Samara',        'Volgograd',
                'Sochi',            'Kazan',          'Saransk',
          'Kaliningrad',  'Nizhny Novgorod']
    Length: 11, dtype: str



#### **Inspection s'il y a des dates invalides**


```python
df_final_2018[df_final_2018["date"].isna()]
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



#### **Colonnes numériques bien typées**


```python
df_final_2018["home_result"].astype(int)
```




    0     5
    1     0
    2     3
    3     1
    4     3
    5     2
    6     3
    7     0
    8     1
    9     0
    10    1
    11    2
    12    2
    13    0
    14    1
    15    1
    16    0
    17    0
    18    1
    19    2
    20    0
    21    2
    22    1
    23    1
    24    1
    25    0
    26    2
    27    1
    28    0
    29    2
    30    0
    31    1
    32    2
    33    1
    34    2
    35    0
    36    3
    37    1
    38    5
    39    6
    40    0
    41    1
    42    1
    43    1
    44    0
    45    2
    46    0
    47    0
    48    2
    49    4
    50    1
    51    1
    52    2
    53    3
    54    1
    55    1
    56    0
    57    1
    58    2
    59    0
    60    1
    61    2
    62    2
    63    4
    Name: home_result, dtype: int64



### **Export**


```python
DATA_CLEAN = Path("..") / "data_clean"

df_final_2018.to_csv(DATA_CLEAN / "matches_2018_clean.csv", index=False)
df_final_2018.to_parquet(DATA_CLEAN / "matches_2018_clean.parquet", index=False)
```
