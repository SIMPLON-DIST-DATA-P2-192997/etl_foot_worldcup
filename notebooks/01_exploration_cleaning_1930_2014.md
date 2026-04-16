### **Imports + configuration du chemin**


```python
import pandas as pd
import numpy as np
import re
from pathlib import Path
from unidecode import unidecode

DATA_RAW = Path("..") / "data_raw"
DATA_CLEAN = Path("..") / "data_clean"

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
```

### **Chargement des CSV (1930–2010 et 2014)**

⚠️ Le fichier 2014 contient des caractères encodés bizarrement → encoding="latin1" est le plus robuste.


```python
# Chargement du fichier 1930–2010
df_1930_2010 = pd.read_csv(
    DATA_RAW / "matches_19302010.csv",
    sep=",",          # à ajuster si besoin après inspection
    encoding="latin1" # ou utf-8 si pas d’erreurs
)

# Chargement du fichier 2014
df_2014 = pd.read_csv(
    DATA_RAW / "WorldCupMatches2014.csv",
    sep=";",
    encoding="latin1"
)

df_1930_2010.head(), df_2014.head()
```




    (        edition        round      score                                team1  \
     0  1930-URUGUAY  GROUP_STAGE  4-1 (3-0)                               France   
     1  1930-URUGUAY  GROUP_STAGE  3-0 (2-0)                                  USA   
     2  1930-URUGUAY  GROUP_STAGE  2-1 (2-0)  Yugoslavia (ÐÑÐ³Ð¾ÑÐ»Ð°Ð²Ð¸ÑÐ°)   
     3  1930-URUGUAY  GROUP_STAGE  3-1 (1-0)                   Romania (RomÃ¢nia)   
     4  1930-URUGUAY  GROUP_STAGE  1-0 (0-0)                            Argentina   
     
                    team2                             url        venue  year  
     0   Mexico (MÃ©xico)   1930_URUGUAY_FS.htm#1-WC-30-I  Montevideo.  1930  
     1  Belgium (BelgiÃ«)  1930_URUGUAY_FS.htm#13-WC-30-I  Montevideo.  1930  
     2    Brazil (Brasil)   1930_URUGUAY_FS.htm#7-WC-30-I  Montevideo.  1930  
     3       Peru (PerÃº)  1930_URUGUAY_FS.htm#10-WC-30-I  Montevideo.  1930  
     4             France   1930_URUGUAY_FS.htm#2-WC-30-I  Montevideo.  1930  ,
        Year              Datetime    Stage             Stadium             City  \
     0  2014  12 Jun 2014 - 17:00   Group A  Arena de Sao Paulo       Sao Paulo    
     1  2014  13 Jun 2014 - 13:00   Group A   Estadio das Dunas           Natal    
     2  2014  13 Jun 2014 - 16:00   Group B    Arena Fonte Nova        Salvador    
     3  2014  13 Jun 2014 - 18:00   Group B      Arena Pantanal          Cuiaba    
     4  2014  14 Jun 2014 - 13:00   Group C    Estadio Mineirao  Belo Horizonte    
     
       Home Team Name  Home Team Goals  Away Team Goals Away Team Name  \
     0         Brazil                3                1        Croatia   
     1         Mexico                1                0       Cameroon   
     2          Spain                1                5    Netherlands   
     3          Chile                3                1      Australia   
     4       Colombia                3                0         Greece   
     
       Win conditions  Attendance  Half-time Home Goals  Half-time Away Goals  \
     0                    62103.0                     1                     1   
     1                    39216.0                     0                     0   
     2                    48173.0                     1                     1   
     3                    40275.0                     2                     1   
     4                    57174.0                     1                     0   
     
                       Referee             Assistant 1  \
     0  NISHIMURA Yuichi (JPN)       SAGARA Toru (JPN)   
     1     ROLDAN Wilmar (COL)  CLAVIJO Humberto (COL)   
     2    Nicola RIZZOLI (ITA)   Renato FAVERANI (ITA)   
     3   Noumandiez DOUE (CIV)    YEO Songuifolo (CIV)   
     4       GEIGER Mark (USA)         HURD Sean (USA)   
     
                          Assistant 2  RoundID    MatchID Home Team Initials  \
     0           NAGI Toshiyuki (JPN)   255931  300186456                BRA   
     1             DIAZ Eduardo (COL)   255931  300186492                MEX   
     2           Andrea STEFANI (ITA)   255931  300186510                ESP   
     3  BIRUMUSHAHU Jean Claude (BDI)   255931  300186473                CHI   
     4             FLETCHER Joe (CAN)   255931  300186471                COL   
     
       Away Team Initials  
     0                CRO  
     1                CMR  
     2                NED  
     3                AUS  
     4                GRE  )



### **Inspection des colonnes**

Objectif : repérer les colonnes utiles pour le schéma final.


```python
print("Colonnes 1930–2010 :")
print(df_1930_2010.columns.tolist())

print("\nColonnes 2014 :")
print(df_2014.columns.tolist())
```

    Colonnes 1930–2010 :
    ['edition', 'round', 'score', 'team1', 'team2', 'url', 'venue', 'year']
    
    Colonnes 2014 :
    ['Year', 'Datetime', 'Stage', 'Stadium', 'City', 'Home Team Name', 'Home Team Goals', 'Away Team Goals', 'Away Team Name', 'Win conditions', 'Attendance', 'Half-time Home Goals', 'Half-time Away Goals', 'Referee', 'Assistant 1', 'Assistant 2', 'RoundID', 'MatchID', 'Home Team Initials', 'Away Team Initials']


### **Dimensions des datasets**


```python
print("Taille 1930–2010 :", df_1930_2010.shape)
print("Taille 2014 :", df_2014.shape)
```

    Taille 1930–2010 : (7299, 8)
    Taille 2014 : (80, 20)


### **Inspection s'il ya des valeurs manquantes (NaN), des doublons, des chaines malformées**

#### **Vérification des valeurs manquantes**


```python
print("NaN 1930–2010 :")
display(df_1930_2010.isna().sum())

print("\nNaN 2014 :")
display(df_2014.isna().sum())
```

    NaN 1930–2010 :



    edition    0
    round      0
    score      0
    team1      0
    team2      0
    url        0
    venue      0
    year       0
    dtype: int64


    
    NaN 2014 :



    Year                    0
    Datetime                0
    Stage                   0
    Stadium                 0
    City                    0
    Home Team Name          0
    Home Team Goals         0
    Away Team Goals         0
    Away Team Name          0
    Win conditions          0
    Attendance              2
    Half-time Home Goals    0
    Half-time Away Goals    0
    Referee                 0
    Assistant 1             0
    Assistant 2             0
    RoundID                 0
    MatchID                 0
    Home Team Initials      0
    Away Team Initials      0
    dtype: int64


#### **Vérification des doublons**


```python
print("Doublons 1930–2010 :", df_1930_2010.duplicated().sum())
print("Doublons 2014 :", df_2014.duplicated().sum())
```

    Doublons 1930–2010 : 0
    Doublons 2014 : 16


#### **Aperçu des valeurs clés (équipes, villes, rounds)**


```python
print("Équipes 2014 :", df_2014["Home Team Name"].unique()[:20])
print("Villes 2014 :", df_2014["City"].unique()[:20])
print("Stages 2014 :", df_2014["Stage"].unique())
```

    Équipes 2014 : <ArrowStringArray>
    [         'Brazil',          'Mexico',           'Spain',           'Chile',
            'Colombia',         'Uruguay',         'England', 'Cï¿½te d'Ivoire',
         'Switzerland',          'France',       'Argentina',         'Germany',
             'IR Iran',           'Ghana',         'Belgium',          'Russia',
           'Australia',        'Cameroon',           'Japan',           'Italy']
    Length: 20, dtype: str
    Villes 2014 : <ArrowStringArray>
    [     'Sao Paulo ',          'Natal ',       'Salvador ',         'Cuiaba ',
     'Belo Horizonte ',      'Fortaleza ',         'Manaus ',         'Recife ',
           'Brasilia ',   'Porto Alegre ', 'Rio De Janeiro ',       'Curitiba ']
    Length: 12, dtype: str
    Stages 2014 : <ArrowStringArray>
    [                 'Group A',                  'Group B',
                      'Group C',                  'Group D',
                      'Group E',                  'Group F',
                      'Group G',                  'Group H',
                  'Round of 16',           'Quarter-finals',
                  'Semi-finals', 'Play-off for third place',
                        'Final']
    Length: 13, dtype: str



```python
TARGET_COLUMNS = [
    "home_team",
    "away_team",
    "home_result",
    "away_result",
    "result",
    "date",
    "round",
    "city",
    "edition"
]

TARGET_COLUMNS
```




    ['home_team',
     'away_team',
     'home_result',
     'away_result',
     'result',
     'date',
     'round',
     'city',
     'edition']



### **Nettoyage minimal des espaces et encodages visibles**


```python
# Nettoyage minimal des chaînes de caractères
# -------------------------------------------

# Suppression des espaces en fin de chaîne pour 2014
df_2014["City"] = df_2014["City"].str.strip()
df_2014["Home Team Name"] = df_2014["Home Team Name"].str.strip()
df_2014["Away Team Name"] = df_2014["Away Team Name"].str.strip()

# Suppression des parenthèses et du texte entre parenthèses pour 1930–2010
df_1930_2010["team1"] = df_1930_2010["team1"].str.replace(r"\(.*?\)", "", regex=True).str.strip()
df_1930_2010["team2"] = df_1930_2010["team2"].str.replace(r"\(.*?\)", "", regex=True).str.strip()

# Nettoyage du champ 'venue'
df_1930_2010["venue"] = df_1930_2010["venue"].str.replace(".", "", regex=False).str.strip()

print("Nettoyage minimal effectué.")
print("Exemple team1 (1930–2010) :", df_1930_2010['team1'].head().tolist())
print("Exemple City (2014) :", df_2014['City'].unique()[:5])
```

    Nettoyage minimal effectué.
    Exemple team1 (1930–2010) : ['France', 'USA', 'Yugoslavia', 'Romania', 'Argentina']
    Exemple City (2014) : <ArrowStringArray>
    ['Sao Paulo', 'Natal', 'Salvador', 'Cuiaba', 'Belo Horizonte']
    Length: 5, dtype: str


### **Détection des problèmes d’encodage**


```python
def detect_encoding_issues(series):
    """
    Détecte les chaînes contenant des artefacts d'encodage courants
    (caractères 'Ã', 'Ð', '¿', '�') dans une série Pandas.

    Paramètres
    ----------
    series : pd.Series
        Série de chaînes à analyser.

    Retour
    ------
    np.ndarray
        Tableau des valeurs problématiques détectées.
    """
    return series[series.str.contains("Ã|Ð|¿|�", na=False)].unique()

print("Problèmes d'encodage détectés dans team1 (1930–2010) :")
print(detect_encoding_issues(df_1930_2010["team1"]))

print("\nProblèmes d'encodage détectés dans team2 (1930–2010) :")
print(detect_encoding_issues(df_1930_2010["team2"]))

print("\nProblèmes d'encodage détectés dans les équipes 2014 :")
print(detect_encoding_issues(df_2014["Home Team Name"]))

```

    Problèmes d'encodage détectés dans team1 (1930–2010) :
    <ArrowStringArray>
    ['CuraÃ§ao', 'SÃ£o TomÃ© e PrÃ­ncipe']
    Length: 2, dtype: str
    
    Problèmes d'encodage détectés dans team2 (1930–2010) :
    <ArrowStringArray>
    ['CuraÃ§ao', 'SÃ£o TomÃ© e PrÃ­ncipe']
    Length: 2, dtype: str
    
    Problèmes d'encodage détectés dans les équipes 2014 :
    <ArrowStringArray>
    ['Cï¿½te d'Ivoire']
    Length: 1, dtype: str


### **Aperçu des rounds (pour harmonisation)**

*utile pour préparer un mapping*


```python
print("Rounds 1930–2010 :", df_1930_2010["round"].unique()[:20])
print("\nRounds 2014 :", df_2014["Stage"].unique())
```

    Rounds 1930–2010 : <ArrowStringArray>
    [            'GROUP_STAGE',               '1/2_FINAL',
                      '_FINAL',      'PRELIMINARY-Europe',
     'PRELIMINARY-N/C.America',        'PRELIMINARY-N.E.',
                       'FIRST',               '1/4_FINAL',
                  'PLACES_3&4',   'PRELIMINARY-Eur./N.E.',
       'PRELIMINARY-S.America',             'FINAL_ROUND',
        'PRELIMINARY-Eu./Afr.',        'PRELIMINARY-Asia',
        'PRELIMINARY-Afr./As.',    'PRELIMINARY-Euro/As.',
     'PRELIMINARY-E./Afr./As.',  'PRELIMINARY-Af./As./O.',
          'PRELIMINARY-Africa',      'PRELIMINARY-As./O.']
    Length: 20, dtype: str
    
    Rounds 2014 : <ArrowStringArray>
    [                 'Group A',                  'Group B',
                      'Group C',                  'Group D',
                      'Group E',                  'Group F',
                      'Group G',                  'Group H',
                  'Round of 16',           'Quarter-finals',
                  'Semi-finals', 'Play-off for third place',
                        'Final']
    Length: 13, dtype: str


### **Extraction des scores (1930–2010)**


```python
def extract_scores(score_str):
    """
    Extrait les scores finaux d'une chaîne de type '4-1 (3-0)'.

    Paramètres
    ----------
    score_str : str
        Chaîne contenant le score final et éventuellement le score à la mi-temps.

    Retour
    ------
    tuple(int, int)
        (buts équipe 1, buts équipe 2)
    """
    match = re.match(r"(\d+)-(\d+)", score_str)
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

# Explication :
# df["score"].apply(extract_scores) renvoie une série de tuples : [(4,1), (3,0), ...]
# zip(*serie) "transpose" cette liste de tuples en deux listes :
#   - la liste des scores home
#   - la liste des scores away

df_1930_2010["home_result"], df_1930_2010["away_result"] = zip(
    *df_1930_2010["score"].apply(extract_scores)
)

print("Extraction des scores effectuée.")
df_1930_2010[["score", "home_result", "away_result"]].head()

```

    Extraction des scores effectuée.





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
      <th>score</th>
      <th>home_result</th>
      <th>away_result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>4-1 (3-0)</td>
      <td>4.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3-0 (2-0)</td>
      <td>3.0</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2-1 (2-0)</td>
      <td>2.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3-1 (1-0)</td>
      <td>3.0</td>
      <td>1.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1-0 (0-0)</td>
      <td>1.0</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
</div>



### **Extraction du vainqueur**


```python
def compute_result(row):
    """
    Détermine le vainqueur d'un match à partir des scores.

    Paramètres
    ----------
    row : pd.Series
        Ligne contenant 'home_result' et 'away_result'.

    Retour
    ------
    str
        Nom de l'équipe gagnante ou 'draw' en cas d'égalité.
    """
    if row["home_result"] > row["away_result"]:
        return row["team1"]
    elif row["home_result"] < row["away_result"]:
        return row["team2"]
    else:
        return "draw"

# Explication :
# axis=1 signifie que la fonction compute_result est appliquée LIGNE PAR LIGNE.
# axis=0 = colonne par colonne
# axis=1 = ligne par ligne (ce qu'il nous faut ici)

df_1930_2010["result"] = df_1930_2010.apply(compute_result, axis=1)

print("Calcul du vainqueur effectué.")
df_1930_2010[["team1", "team2", "home_result", "away_result", "result"]].head()

```

    Calcul du vainqueur effectué.





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
      <th>team1</th>
      <th>team2</th>
      <th>home_result</th>
      <th>away_result</th>
      <th>result</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>France</td>
      <td>Mexico</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>France</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USA</td>
      <td>Belgium</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>USA</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Yugoslavia</td>
      <td>Brazil</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>Yugoslavia</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Romania</td>
      <td>Peru</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>Romania</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Argentina</td>
      <td>France</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>Argentina</td>
    </tr>
  </tbody>
</table>
</div>



### **Préparation du DataFrame final 1930–2014**


```python
df_1930_2014 = pd.DataFrame({
    "home_team": df_1930_2010["team1"],
    "away_team": df_1930_2010["team2"],
    "home_result": df_1930_2010["home_result"],
    "away_result": df_1930_2010["away_result"],
    "result": df_1930_2010["result"],
    "date": df_1930_2010["year"],  # à convertir ensuite
    "round": df_1930_2010["round"],
    "city": df_1930_2010["venue"],
    "stadium": None,
    "edition": df_1930_2010["edition"]
})

df_1930_2014.head()
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
      <td>France</td>
      <td>Mexico</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>France</td>
      <td>1930</td>
      <td>GROUP_STAGE</td>
      <td>Montevideo</td>
      <td>None</td>
      <td>1930-URUGUAY</td>
    </tr>
    <tr>
      <th>1</th>
      <td>USA</td>
      <td>Belgium</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>USA</td>
      <td>1930</td>
      <td>GROUP_STAGE</td>
      <td>Montevideo</td>
      <td>None</td>
      <td>1930-URUGUAY</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Yugoslavia</td>
      <td>Brazil</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>Yugoslavia</td>
      <td>1930</td>
      <td>GROUP_STAGE</td>
      <td>Montevideo</td>
      <td>None</td>
      <td>1930-URUGUAY</td>
    </tr>
    <tr>
      <th>3</th>
      <td>Romania</td>
      <td>Peru</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>Romania</td>
      <td>1930</td>
      <td>GROUP_STAGE</td>
      <td>Montevideo</td>
      <td>None</td>
      <td>1930-URUGUAY</td>
    </tr>
    <tr>
      <th>4</th>
      <td>Argentina</td>
      <td>France</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>Argentina</td>
      <td>1930</td>
      <td>GROUP_STAGE</td>
      <td>Montevideo</td>
      <td>None</td>
      <td>1930-URUGUAY</td>
    </tr>
  </tbody>
</table>
</div>



### **Détecter toutes les valeurs uniques problématiques**


```python
# Détection des équipes problématiques dans 1930–2010
teams_1930_2010 = pd.concat([df_1930_2010["team1"], df_1930_2010["team2"]]).unique()
teams_1930_2010[:50]
```




    <ArrowStringArray>
    [          'France',              'USA',       'Yugoslavia',
              'Romania',        'Argentina',            'Chile',
              'Uruguay',           'Brazil',         'Paraguay',
               'Sweden',        'Lithuania',           'Poland',
          'Switzerland',            'Haiti', 'Irish Free State',
               'Mexico',            'Spain',       'Luxembourg',
                'Egypt',         'Portugal',            'Italy',
             'Bulgaria',        'Palestine',      'Netherlands',
              'Austria',          'Hungary',          'Belgium',
              'Germany',   'Czechoslovakia',          'Finland',
               'Latvia',           'Norway',           'Greece',
                 'Cuba',          'Ireland',           'Israel',
     'Northern Ireland',            'Wales',         'Scotland',
              'England',           'Turkey',          'Bolivia',
                  'FRG',         'Saarland',            'Japan',
          'South Korea',        'Guatemala',       'Costa Rica',
                'Sudan',             'Peru']
    Length: 50, dtype: str




```python
# Détection des équipes problématiques en 2014
teams_2014 = pd.concat([df_2014["Home Team Name"], df_2014["Away Team Name"]]).unique()
teams_2014
```




    <ArrowStringArray>
    [                    'Brazil',                     'Mexico',
                          'Spain',                      'Chile',
                       'Colombia',                    'Uruguay',
                        'England',            'Cï¿½te d'Ivoire',
                    'Switzerland',                     'France',
                      'Argentina',                    'Germany',
                        'IR Iran',                      'Ghana',
                        'Belgium',                     'Russia',
                      'Australia',                   'Cameroon',
                          'Japan',                      'Italy',
                       'Honduras',                    'Nigeria',
                 'Korea Republic',                        'USA',
                    'Netherlands',                    'Croatia',
                     'Costa Rica',                     'Greece',
     'rn">Bosnia and Herzegovina',                    'Ecuador',
                       'Portugal',                    'Algeria']
    Length: 32, dtype: str



### **Création d'une fonction de nettoyage générique**


```python
def clean_team_name(name):
    """
    Nettoie un nom d'équipe provenant des datasets historiques FIFA.
    
    Étapes :
    1. Gère les valeurs manquantes.
    2. Supprime les artefacts HTML (ex: 'rn">Bosnia and Herzegovina').
    3. Supprime les artefacts d'encodage (ex: 'Cï¿½te d'Ivoire').
    4. Normalise Unicode → ASCII via unidecode.
    5. Supprime les espaces superflus.
    6. Applique un mapping manuel pour harmoniser les variantes.
    
    Paramètres
    ----------
    name : str
        Nom brut de l'équipe.

    Retour
    ------
    str
        Nom nettoyé et harmonisé.
    """
    
    if pd.isna(name):
        return name

    # Convertir en string au cas où
    name = str(name)

    # 1. Nettoyage des artefacts HTML
    html_artifacts = ['rn">', 'rn&quot;&gt;', 'rn&quot;', 'rn&gt;', 'rn>']
    for art in html_artifacts:
        name = name.replace(art, "")

    # 2. Nettoyage des artefacts d'encodage spécifiques observés
    encoding_fixes = {
        "Cï¿½te d'Ivoire": "Cote d'Ivoire",
        "Ci? 1/2te d'Ivoire": "Cote d'Ivoire",
        "CÃ´te d'Ivoire": "Cote d'Ivoire",
        "CÃ´te dIvoire": "Cote d'Ivoire",
    }
    if name in encoding_fixes:
        name = encoding_fixes[name]

    # 3. Normalisation Unicode → ASCII
    name = unidecode(name)

    # 4. Suppression des espaces superflus
    name = name.strip()

    # 5. Mapping manuel complet
    TEAM_MAPPING = {
        # Variantes modernes
        "IR Iran": "Iran",
        "Korea Republic": "South Korea",
        "USA": "United States",
        "Sao Tome e Principe": "Sao Tome and Principe",
        "Cote d'Ivoire": "Ivory Coast",

        # Artefacts HTML
        'Bosnia and Herzegovina': "Bosnia and Herzegovina",

        # Variantes historiques (à discuter en équipe)
        "Soviet Union": "Russia",
        "Yugoslavia": "Serbia",
        "Czechoslovakia": "Czech Republic",
        "FRG": "Germany",
        "Saarland": "Germany",
        "Irish Free State": "Ireland",

        # Cas particuliers
        "Curacao": "Curacao",  # unidecode enlève l'accent → choix d'équipe
    }

    return TEAM_MAPPING.get(name, name)
```

### **Appliquer le nettoyage aux deux datasets**


```python
df_1930_2010["team1"] = df_1930_2010["team1"].apply(clean_team_name)
df_1930_2010["team2"] = df_1930_2010["team2"].apply(clean_team_name)

df_2014["Home Team Name"] = df_2014["Home Team Name"].apply(clean_team_name)
df_2014["Away Team Name"] = df_2014["Away Team Name"].apply(clean_team_name)
```

### **Vérifier le résultat**


```python
print("Équipes 1930–2010 après nettoyage :", 
      pd.concat([df_1930_2010["team1"], df_1930_2010["team2"]]).unique()[:50])

print("\nÉquipes 2014 après nettoyage :", 
      pd.concat([df_2014["Home Team Name"], df_2014["Away Team Name"]]).unique())
```

    Équipes 1930–2010 après nettoyage : <ArrowStringArray>
    [          'France',    'United States',           'Serbia',
              'Romania',        'Argentina',            'Chile',
              'Uruguay',           'Brazil',         'Paraguay',
               'Sweden',        'Lithuania',           'Poland',
          'Switzerland',            'Haiti',          'Ireland',
               'Mexico',            'Spain',       'Luxembourg',
                'Egypt',         'Portugal',            'Italy',
             'Bulgaria',        'Palestine',      'Netherlands',
              'Austria',          'Hungary',          'Belgium',
              'Germany',   'Czech Republic',          'Finland',
               'Latvia',           'Norway',           'Greece',
                 'Cuba',           'Israel', 'Northern Ireland',
                'Wales',         'Scotland',          'England',
               'Turkey',          'Bolivia',            'Japan',
          'South Korea',        'Guatemala',       'Costa Rica',
                'Sudan',             'Peru',        'Indonesia',
              'Denmark',              'GDR']
    Length: 50, dtype: str
    
    Équipes 2014 après nettoyage : <ArrowStringArray>
    [                'Brazil',                 'Mexico',                  'Spain',
                      'Chile',               'Colombia',                'Uruguay',
                    'England',            'Ivory Coast',            'Switzerland',
                     'France',              'Argentina',                'Germany',
                       'Iran',                  'Ghana',                'Belgium',
                     'Russia',              'Australia',               'Cameroon',
                      'Japan',                  'Italy',               'Honduras',
                    'Nigeria',            'South Korea',          'United States',
                'Netherlands',                'Croatia',             'Costa Rica',
                     'Greece', 'Bosnia and Herzegovina',                'Ecuador',
                   'Portugal',                'Algeria']
    Length: 32, dtype: str



```python
# Villes 1930–2010
cities_1930_2010 = df_1930_2010["venue"].unique()
print("Villes 1930–2010 :", cities_1930_2010[:50])

# Villes 2014
cities_2014 = df_2014["City"].unique()
print("\nVilles 2014 :", cities_2014)
```

    Villes 1930–2010 : <ArrowStringArray>
    [    'Montevideo',      'Stockholm',         'Kaunas',        'Beograd',
           'Warszawa',           'Bern', 'Port-au-Prince',         'Dublin',
         'MÃ©xico DF',         'Madrid',     'Luxembourg',          'Cairo',
             'Lisboa',         'Milano',         'Sofija',      'Jerusalem',
          'Amsterdam',           'Wien',       'Budapest',     'BucureÅti',
          'Antwerpen',           'Roma',         'Torino',        'Firenze',
            'Trieste',        'Bologna',         'Genova',         'Napoli',
           'Helsinki',          'RÄ«ga',          'Turku',    'KÃ¶nigsberg',
               'Oslo',        'Hamburg',      'Rotterdam',       'Tel Aviv',
            'AthÃ­na',          'Praha',          'Paris',      'Marseille',
              'Reims',       'Toulouse',     'Strasbourg',       'Le_Havre',
           'Bordeaux',          'Lille',        'Antibes',        'ZÃ¼rich',
            'Belfast',         'MalmÃ¶']
    Length: 50, dtype: str
    
    Villes 2014 : <ArrowStringArray>
    [     'Sao Paulo',          'Natal',       'Salvador',         'Cuiaba',
     'Belo Horizonte',      'Fortaleza',         'Manaus',         'Recife',
           'Brasilia',   'Porto Alegre', 'Rio De Janeiro',       'Curitiba']
    Length: 12, dtype: str


### **Création d'une fonction de nettoyage des villes**


```python
def clean_city(name):
    """
    Nettoie un nom de ville provenant des datasets FIFA (1930–2014).

    Étapes :
    1. Gère les valeurs manquantes.
    2. Corrige les artefacts d'encodage observés dans les données.
    3. Normalise Unicode → ASCII via unidecode.
    4. Supprime les espaces superflus.
    5. Applique un mapping manuel minimal basé sur vos données réelles.
    """

    if pd.isna(name):
        return name

    name = str(name).strip()

    # 1. Corrections d'encodage spécifiques observées
    encoding_fixes = {
        "MÃ©xico DF": "Mexico City",
        "BucureÅti": "Bucharest",
        "KÃ¶nigsberg": "Konigsberg",
        "AthÃ­na": "Athens",
        "ZÃ¼rich": "Zurich",
        "MalmÃ¶": "Malmo",
        "RÄ«ga": "Riga",
    }
    if name in encoding_fixes:
        name = encoding_fixes[name]

    # 2. Normalisation Unicode
    name = unidecode(name)

    # 3. Mapping manuel minimal
    CITY_MAPPING = {
        # Harmonisation 1930–2010
        "Beograd": "Belgrade",
        "Warszawa": "Warsaw",
        "Milano": "Milan",
        "Firenze": "Florence",
        "Torino": "Turin",
        "Genova": "Genoa",
        "Napoli": "Naples",
        "Praha": "Prague",
        "Wien": "Vienna",
        "Le_Havre": "Le Havre",

        # Harmonisation 2014
        "Rio De Janeiro": "Rio de Janeiro",

        # Corrections d’encodage déjà normalisées via unidecode
        "Geneve": "Geneva",
        "Genève": "Geneva",
    }

    return CITY_MAPPING.get(name, name)
```

### **Appliquer le nettoyage**


```python
df_1930_2010["venue"] = df_1930_2010["venue"].apply(clean_city)
df_2014["City"] = df_2014["City"].apply(clean_city)
```

### **Vérifier le résultat**


```python
print("Villes 1930–2010 après nettoyage :", df_1930_2010["venue"].unique()[:50])
print("\nVilles 2014 après nettoyage :", df_2014["City"].unique())
```

    Villes 1930–2010 après nettoyage : <ArrowStringArray>
    [    'Montevideo',      'Stockholm',         'Kaunas',       'Belgrade',
             'Warsaw',           'Bern', 'Port-au-Prince',         'Dublin',
        'Mexico City',         'Madrid',     'Luxembourg',          'Cairo',
             'Lisboa',          'Milan',         'Sofija',      'Jerusalem',
          'Amsterdam',         'Vienna',       'Budapest',      'Bucharest',
          'Antwerpen',           'Roma',          'Turin',       'Florence',
            'Trieste',        'Bologna',          'Genoa',         'Naples',
           'Helsinki',           'Riga',          'Turku',     'Konigsberg',
               'Oslo',        'Hamburg',      'Rotterdam',       'Tel Aviv',
             'Athens',         'Prague',          'Paris',      'Marseille',
              'Reims',       'Toulouse',     'Strasbourg',       'Le Havre',
           'Bordeaux',          'Lille',        'Antibes',         'Zurich',
            'Belfast',          'Malmo']
    Length: 50, dtype: str
    
    Villes 2014 après nettoyage : <ArrowStringArray>
    [     'Sao Paulo',          'Natal',       'Salvador',         'Cuiaba',
     'Belo Horizonte',      'Fortaleza',         'Manaus',         'Recife',
           'Brasilia',   'Porto Alegre', 'Rio de Janeiro',       'Curitiba']
    Length: 12, dtype: str


### **Création d'une fonction d'harmonisation des rounds**


```python
def clean_round(value):
    """
    Harmonise les rounds provenant des datasets FIFA (1930–2014).

    Étapes :
    1. Normalise la casse et supprime les espaces superflus.
    2. Détecte les rounds de type 'Group A', 'Group B', etc.
    3. Mappe les rounds historiques (1930–2010) vers un vocabulaire commun.
    4. Mappe les rounds 2014 vers les mêmes valeurs normalisées.
    """

    if pd.isna(value):
        return value

    value = str(value).strip()

    # 1. Groupes 2014 : Group A → group_stage
    if value.startswith("Group "):
        return "group_stage"

    # 2. Mapping manuel basé sur vos données réelles
    ROUND_MAPPING = {
        # 1930–2010
        "GROUP_STAGE": "group_stage",
        "FIRST": "group_stage",
        "FINAL_ROUND": "group_stage",

        "1/8_FINAL": "round_of_16",
        "1/4_FINAL": "quarter_final",
        "1/2_FINAL": "semi_final",
        "_FINAL": "final",
        "PLACES_3&4": "third_place",

        # Préliminaires
        "PRELIMINARY-Europe": "qualification",
        "PRELIMINARY-N/C.America": "qualification",
        "PRELIMINARY-N.E.": "qualification",
        "PRELIMINARY-Eur./N.E.": "qualification",
        "PRELIMINARY-S.America": "qualification",
        "PRELIMINARY-Eu./Afr.": "qualification",
        "PRELIMINARY-Asia": "qualification",
        "PRELIMINARY-Afr./As.": "qualification",
        "PRELIMINARY-Euro/As.": "qualification",
        "PRELIMINARY-E./Afr./As.": "qualification",
        "PRELIMINARY-Af./As./O.": "qualification",
        "PRELIMINARY-Africa": "qualification",
        "PRELIMINARY-As./O.": "qualification",
        "PRELIMINARY-O./As.": "qualification",
        "PRELIMINARY-Oceania": "qualification",

        # 2014
        "Round of 16": "round_of_16",
        "Quarter-finals": "quarter_final",
        "Semi-finals": "semi_final",
        "Play-off for third place": "third_place",
        "Final": "final",

        # Valeurs résiduelles détectées
        "SEMIFINAL_STAGE": "semi_final",
        "QUARTERFINAL_STAGE": "quarter_final",
    }

    return ROUND_MAPPING.get(value, value)
```

### **Application du nettoyage**


```python
df_1930_2010["round"] = df_1930_2010["round"].apply(clean_round)
df_2014["Stage"] = df_2014["Stage"].apply(clean_round)
```

### **Vérifier le résultat**


```python
print("Rounds 1930–2010 après nettoyage :", df_1930_2010["round"].unique())
print("\nRounds 2014 après nettoyage :", df_2014["Stage"].unique())
```

    Rounds 1930–2010 après nettoyage : <ArrowStringArray>
    [  'group_stage',    'semi_final',         'final', 'qualification',
     'quarter_final',   'third_place',   'round_of_16']
    Length: 7, dtype: str
    
    Rounds 2014 après nettoyage : <ArrowStringArray>
    [  'group_stage',   'round_of_16', 'quarter_final',    'semi_final',
       'third_place',         'final']
    Length: 6, dtype: str


### **Conversion 1930–2010**


```python
if "date" in df_1930_2010.columns:
    df_1930_2010 = df_1930_2010.rename(columns={"date": "year"})

df_1930_2010["date"] = pd.NaT

print("Exemple dates 1930–2010 :")
df_1930_2010["date"].head()
```

    Exemple dates 1930–2010 :





    0   NaT
    1   NaT
    2   NaT
    3   NaT
    4   NaT
    Name: date, dtype: datetime64[ns]



### **Conversion 2014**


```python
# Nettoyage préalable
df_2014["Datetime"] = df_2014["Datetime"].str.strip()
df_2014["Datetime"] = df_2014["Datetime"].str.replace("\u00A0", " ", regex=False)

# Parsing robuste
df_2014["date"] = pd.to_datetime(df_2014["Datetime"], dayfirst=True)

print(df_2014["date"].head())
```

    0   2014-06-12 17:00:00
    1   2014-06-13 13:00:00
    2   2014-06-13 16:00:00
    3   2014-06-13 18:00:00
    4   2014-06-14 13:00:00
    Name: date, dtype: datetime64[us]



```python
df_1930_2010["edition"].unique()

```




    <ArrowStringArray>
    [     '1930-URUGUAY',        '1934-ITALY',       '1938-FRANCE',
           '1950-BRAZIL',  '1954-SWITZERLAND',       '1958-SWEDEN',
            '1962-CHILE',      '1966-ENGLAND',       '1970-MEXICO',
              '1974-FRG',    '1978-ARGENTINA',        '1982-SPAIN',
           '1986-MEXICO',        '1990-ITALY',          '1994-USA',
           '1998-FRANCE',  '2002-KOREA/JAPAN',      '2006-GERMANY',
     '2010-SOUTH AFRICA',       '2014-BRAZIL']
    Length: 20, dtype: str



### **Vérifier et supprimer les doublons dans df_2014**


```python
df_2014 = df_2014.drop_duplicates()
len(df_2014)
```




    64



### **Vérifier les encodages dans les deux datasets**


```python
def detect_encoding_issues(df):
    """
    Détecte les artefacts d'encodage dans les colonnes de type string d'un DataFrame.

    Cette fonction recherche des caractères typiquement associés à des problèmes 
    d'encodage (UTF-8 mal décodé, ISO-8859-1 interprété comme UTF-8, etc.), tels que :
    'Ã', 'Â', '�', 'ð', 'Ð', '¿', '¡', '¢', '¤', '¦', '§', '¨', '©', 'ª', '«', '¬', '®', '¯'.

    Paramètres
    ----------
    df : pandas.DataFrame
        Le DataFrame à analyser.

    Retour
    ------
    dict
        Un dictionnaire dont les clés sont les noms des colonnes contenant des anomalies
        d'encodage, et les valeurs sont les valeurs uniques problématiques détectées.
        Retourne un dictionnaire vide si aucune anomalie n'est trouvée.

    Exemple
    -------
    >>> detect_encoding_issues(df)
    {'city': array(['MÃ©xico DF', 'ZÃ¼rich'], dtype=object)}
    """
    issues = {}
    for col in df.columns:
        if df[col].dtype == "object":
            bad = df[col].str.contains("Ã|Â|�|ð|Ð|¿|¡|¢|¤|¦|§|¨|©|ª|«|¬|®|¯", na=False)
            if bad.any():
                issues[col] = df.loc[bad, col].unique()
    return issues

```


```python
detect_encoding_issues(df_1930_2010)
```




    {}




```python
detect_encoding_issues(df_2014)
```




    {}




```python
df_1930_2010.columns
```




    Index(['edition', 'round', 'score', 'team1', 'team2', 'url', 'venue', 'year',
           'home_result', 'away_result', 'result', 'date'],
          dtype='str')




```python
df_2014.columns
```




    Index(['Year', 'Datetime', 'Stage', 'Stadium', 'City', 'Home Team Name',
           'Home Team Goals', 'Away Team Goals', 'Away Team Name',
           'Win conditions', 'Attendance', 'Half-time Home Goals',
           'Half-time Away Goals', 'Referee', 'Assistant 1', 'Assistant 2',
           'RoundID', 'MatchID', 'Home Team Initials', 'Away Team Initials',
           'date'],
          dtype='str')



### **Construction du DataFrame final 1930–2014 (qualifications + phases finales jusqu’à 2010)**


```python
df_1930_2010 = df_1930_2010.rename(columns={
    "team1": "home_team",
    "team2": "away_team"
})

df_final_1930_2014_qualif = df_1930_2010.copy()

# Rien à supprimer pour l’instant, car tu veux garder toutes les colonnes
# (y compris url, score, venue, etc.)

df_final_1930_2014_qualif.head()
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
      <th>edition</th>
      <th>round</th>
      <th>score</th>
      <th>home_team</th>
      <th>away_team</th>
      <th>url</th>
      <th>venue</th>
      <th>year</th>
      <th>home_result</th>
      <th>away_result</th>
      <th>result</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1930-URUGUAY</td>
      <td>group_stage</td>
      <td>4-1 (3-0)</td>
      <td>France</td>
      <td>Mexico</td>
      <td>1930_URUGUAY_FS.htm#1-WC-30-I</td>
      <td>Montevideo</td>
      <td>1930</td>
      <td>4.0</td>
      <td>1.0</td>
      <td>France</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1930-URUGUAY</td>
      <td>group_stage</td>
      <td>3-0 (2-0)</td>
      <td>United States</td>
      <td>Belgium</td>
      <td>1930_URUGUAY_FS.htm#13-WC-30-I</td>
      <td>Montevideo</td>
      <td>1930</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>USA</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1930-URUGUAY</td>
      <td>group_stage</td>
      <td>2-1 (2-0)</td>
      <td>Serbia</td>
      <td>Brazil</td>
      <td>1930_URUGUAY_FS.htm#7-WC-30-I</td>
      <td>Montevideo</td>
      <td>1930</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>Yugoslavia</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1930-URUGUAY</td>
      <td>group_stage</td>
      <td>3-1 (1-0)</td>
      <td>Romania</td>
      <td>Peru</td>
      <td>1930_URUGUAY_FS.htm#10-WC-30-I</td>
      <td>Montevideo</td>
      <td>1930</td>
      <td>3.0</td>
      <td>1.0</td>
      <td>Romania</td>
      <td>NaT</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1930-URUGUAY</td>
      <td>group_stage</td>
      <td>1-0 (0-0)</td>
      <td>Argentina</td>
      <td>France</td>
      <td>1930_URUGUAY_FS.htm#2-WC-30-I</td>
      <td>Montevideo</td>
      <td>1930</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>Argentina</td>
      <td>NaT</td>
    </tr>
  </tbody>
</table>
</div>



### **Construction du DataFrame final 2014 (phase finale)**


```python
df_final_2014_finals = df_2014.copy()

# On garde toutes les colonnes, y compris Datetime (source) et date (datetime64)
df_final_2014_finals.head()
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
      <th>Year</th>
      <th>Datetime</th>
      <th>Stage</th>
      <th>Stadium</th>
      <th>City</th>
      <th>Home Team Name</th>
      <th>Home Team Goals</th>
      <th>Away Team Goals</th>
      <th>Away Team Name</th>
      <th>Win conditions</th>
      <th>Attendance</th>
      <th>Half-time Home Goals</th>
      <th>Half-time Away Goals</th>
      <th>Referee</th>
      <th>Assistant 1</th>
      <th>Assistant 2</th>
      <th>RoundID</th>
      <th>MatchID</th>
      <th>Home Team Initials</th>
      <th>Away Team Initials</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2014</td>
      <td>12 Jun 2014 - 17:00</td>
      <td>group_stage</td>
      <td>Arena de Sao Paulo</td>
      <td>Sao Paulo</td>
      <td>Brazil</td>
      <td>3</td>
      <td>1</td>
      <td>Croatia</td>
      <td></td>
      <td>62103.0</td>
      <td>1</td>
      <td>1</td>
      <td>NISHIMURA Yuichi (JPN)</td>
      <td>SAGARA Toru (JPN)</td>
      <td>NAGI Toshiyuki (JPN)</td>
      <td>255931</td>
      <td>300186456</td>
      <td>BRA</td>
      <td>CRO</td>
      <td>2014-06-12 17:00:00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2014</td>
      <td>13 Jun 2014 - 13:00</td>
      <td>group_stage</td>
      <td>Estadio das Dunas</td>
      <td>Natal</td>
      <td>Mexico</td>
      <td>1</td>
      <td>0</td>
      <td>Cameroon</td>
      <td></td>
      <td>39216.0</td>
      <td>0</td>
      <td>0</td>
      <td>ROLDAN Wilmar (COL)</td>
      <td>CLAVIJO Humberto (COL)</td>
      <td>DIAZ Eduardo (COL)</td>
      <td>255931</td>
      <td>300186492</td>
      <td>MEX</td>
      <td>CMR</td>
      <td>2014-06-13 13:00:00</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2014</td>
      <td>13 Jun 2014 - 16:00</td>
      <td>group_stage</td>
      <td>Arena Fonte Nova</td>
      <td>Salvador</td>
      <td>Spain</td>
      <td>1</td>
      <td>5</td>
      <td>Netherlands</td>
      <td></td>
      <td>48173.0</td>
      <td>1</td>
      <td>1</td>
      <td>Nicola RIZZOLI (ITA)</td>
      <td>Renato FAVERANI (ITA)</td>
      <td>Andrea STEFANI (ITA)</td>
      <td>255931</td>
      <td>300186510</td>
      <td>ESP</td>
      <td>NED</td>
      <td>2014-06-13 16:00:00</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2014</td>
      <td>13 Jun 2014 - 18:00</td>
      <td>group_stage</td>
      <td>Arena Pantanal</td>
      <td>Cuiaba</td>
      <td>Chile</td>
      <td>3</td>
      <td>1</td>
      <td>Australia</td>
      <td></td>
      <td>40275.0</td>
      <td>2</td>
      <td>1</td>
      <td>Noumandiez DOUE (CIV)</td>
      <td>YEO Songuifolo (CIV)</td>
      <td>BIRUMUSHAHU Jean Claude (BDI)</td>
      <td>255931</td>
      <td>300186473</td>
      <td>CHI</td>
      <td>AUS</td>
      <td>2014-06-13 18:00:00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2014</td>
      <td>14 Jun 2014 - 13:00</td>
      <td>group_stage</td>
      <td>Estadio Mineirao</td>
      <td>Belo Horizonte</td>
      <td>Colombia</td>
      <td>3</td>
      <td>0</td>
      <td>Greece</td>
      <td></td>
      <td>57174.0</td>
      <td>1</td>
      <td>0</td>
      <td>GEIGER Mark (USA)</td>
      <td>HURD Sean (USA)</td>
      <td>FLETCHER Joe (CAN)</td>
      <td>255931</td>
      <td>300186471</td>
      <td>COL</td>
      <td>GRE</td>
      <td>2014-06-14 13:00:00</td>
    </tr>
  </tbody>
</table>
</div>



### **Vérification rapide des deux DataFrames**


```python
df_final_1930_2014_qualif.info()
df_final_2014_finals.info()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 7299 entries, 0 to 7298
    Data columns (total 12 columns):
     #   Column       Non-Null Count  Dtype         
    ---  ------       --------------  -----         
     0   edition      7299 non-null   str           
     1   round        7299 non-null   str           
     2   score        7299 non-null   str           
     3   home_team    7299 non-null   str           
     4   away_team    7299 non-null   str           
     5   url          7299 non-null   str           
     6   venue        7299 non-null   str           
     7   year         7299 non-null   int64         
     8   home_result  7235 non-null   float64       
     9   away_result  7235 non-null   float64       
     10  result       7299 non-null   str           
     11  date         0 non-null      datetime64[ns]
    dtypes: datetime64[ns](1), float64(2), int64(1), str(8)
    memory usage: 1.2 MB
    <class 'pandas.DataFrame'>
    RangeIndex: 64 entries, 0 to 63
    Data columns (total 21 columns):
     #   Column                Non-Null Count  Dtype         
    ---  ------                --------------  -----         
     0   Year                  64 non-null     int64         
     1   Datetime              64 non-null     str           
     2   Stage                 64 non-null     str           
     3   Stadium               64 non-null     str           
     4   City                  64 non-null     str           
     5   Home Team Name        64 non-null     str           
     6   Home Team Goals       64 non-null     int64         
     7   Away Team Goals       64 non-null     int64         
     8   Away Team Name        64 non-null     str           
     9   Win conditions        64 non-null     str           
     10  Attendance            63 non-null     float64       
     11  Half-time Home Goals  64 non-null     int64         
     12  Half-time Away Goals  64 non-null     int64         
     13  Referee               64 non-null     str           
     14  Assistant 1           64 non-null     str           
     15  Assistant 2           64 non-null     str           
     16  RoundID               64 non-null     int64         
     17  MatchID               64 non-null     int64         
     18  Home Team Initials    64 non-null     str           
     19  Away Team Initials    64 non-null     str           
     20  date                  64 non-null     datetime64[us]
    dtypes: datetime64[us](1), float64(1), int64(7), str(12)
    memory usage: 19.7 KB


### **Création du dossier data_clean/ si besoin**


```python
DATA_CLEAN = Path("..") / "data_clean"
DATA_CLEAN.mkdir(exist_ok=True)
```

### **Export du dataset 1930–2014 (qualifications + finales jusqu’à 2010)**


```python
df_final_1930_2014_qualif.to_csv(
    DATA_CLEAN / "matches_1930_2014_qualif_clean.csv",
    index=False,
    encoding="utf-8"
)
```


```python
df_final_1930_2014_qualif.to_parquet(
    DATA_CLEAN / "matches_1930_2014_qualif_clean.parquet",
    index=False
)
```

### **Export du dataset 2014 (phase finale complète)**


```python
df_final_2014_finals.to_csv(
    DATA_CLEAN / "matches_2014_finals_clean.csv",
    index=False,
    encoding="utf-8"
)
```


```python
df_final_2014_finals.to_parquet(
    DATA_CLEAN / "matches_2014_finals_clean.parquet",
    index=False
)
```


```python

```
