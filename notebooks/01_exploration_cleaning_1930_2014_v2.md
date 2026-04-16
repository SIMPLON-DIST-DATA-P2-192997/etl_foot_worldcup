### **1. Imports et configuration des chemins**


```python
import pandas as pd
import numpy as np
import re
from pathlib import Path
from unidecode import unidecode

# Dossiers de travail
DATA_RAW = Path("..") / "data_raw"
DATA_CLEAN = Path("..") / "data_clean"
DATA_CLEAN.mkdir(exist_ok=True)

# Options d'affichage
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
```

### **2. Chargement des CSV bruts**


```python
# 1930–2010 (+ qualifs 2014)
df_1930_2010 = pd.read_csv(
    DATA_RAW / "matches_19302010.csv",
    sep=",",
    encoding="latin1"
)

# 2014 (phase finale)
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



### **3. Inspection initiale des données**

#### **3.1 Colonnes et dimensions**


```python
print("Colonnes 1930–2010 :")
print(df_1930_2010.columns.tolist())
print("Taille 1930–2010 :", df_1930_2010.shape)

print("\nColonnes 2014 :")
print(df_2014.columns.tolist())
print("Taille 2014 :", df_2014.shape)
```

    Colonnes 1930–2010 :
    ['edition', 'round', 'score', 'team1', 'team2', 'url', 'venue', 'year']
    Taille 1930–2010 : (7299, 8)
    
    Colonnes 2014 :
    ['Year', 'Datetime', 'Stage', 'Stadium', 'City', 'Home Team Name', 'Home Team Goals', 'Away Team Goals', 'Away Team Name', 'Win conditions', 'Attendance', 'Half-time Home Goals', 'Half-time Away Goals', 'Referee', 'Assistant 1', 'Assistant 2', 'RoundID', 'MatchID', 'Home Team Initials', 'Away Team Initials']
    Taille 2014 : (80, 20)



#### **3.2 Valeurs manquantes**


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



#### **3.3 Doublons**


```python

print("Doublons 1930–2010 :", df_1930_2010.duplicated().sum())
print("Doublons 2014 :", df_2014.duplicated().sum())
```

    Doublons 1930–2010 : 0
    Doublons 2014 : 16



#### **3.4 Types des colonnes**


```python
print("Types 1930–2010 :")
display(df_1930_2010.dtypes)

print("\nTypes 2014 :")
display(df_2014.dtypes)
```

    Types 1930–2010 :



    edition      str
    round        str
    score        str
    team1        str
    team2        str
    url          str
    venue        str
    year       int64
    dtype: object


    
    Types 2014 :



    Year                      int64
    Datetime                    str
    Stage                       str
    Stadium                     str
    City                        str
    Home Team Name              str
    Home Team Goals           int64
    Away Team Goals           int64
    Away Team Name              str
    Win conditions              str
    Attendance              float64
    Half-time Home Goals      int64
    Half-time Away Goals      int64
    Referee                     str
    Assistant 1                 str
    Assistant 2                 str
    RoundID                   int64
    MatchID                   int64
    Home Team Initials          str
    Away Team Initials          str
    dtype: object


#### **3.5 Aperçu des valeurs clés (équipes, villes, rounds)**


```python
print("Équipes 1930–2010 (team1) :", df_1930_2010["team1"].unique()[:20])
print("\nVilles 1930–2010 (venue) :", df_1930_2010["venue"].unique()[:20])
print("\nRounds 1930–2010 :", df_1930_2010["round"].unique()[:20])
```

    Équipes 1930–2010 (team1) : <ArrowStringArray>
    [                               'France',
                                       'USA',
       'Yugoslavia (ÐÑÐ³Ð¾ÑÐ»Ð°Ð²Ð¸ÑÐ°)',
                        'Romania (RomÃ¢nia)',
                                 'Argentina',
                                     'Chile',
                                   'Uruguay',
                           'Brazil (Brasil)',
                                  'Paraguay',
                          'Sweden (Sverige)',
                       'Lithuania (Lietuva)',
                           'Poland (Polska)',
            'Switzerland (Schweiz / Suisse)',
                            'Haiti (HaÃ¯ti)',
     'Irish Free State (SaorstÃ¡t Ãireann)',
                          'Mexico (MÃ©xico)',
                           'Spain (EspaÃ±a)',
                  'Luxembourg (LÃ«tzebuerg)',
                            'Egypt (ÙØµØ±)',
                                  'Portugal']
    Length: 20, dtype: str
    
    Villes 1930–2010 (venue) : <ArrowStringArray>
    [    'Montevideo.',      'Stockholm.',         'Kaunas.',        'Beograd.',
           'Warszawa.',           'Bern.', 'Port-au-Prince.',         'Dublin.',
        'MÃ©xico D.F.',         'Madrid.',     'Luxembourg.',          'Cairo.',
             'Lisboa.',         'Milano.',         'Sofija.',      'Jerusalem.',
          'Amsterdam.',           'Wien.',       'Budapest.',     'BucureÅti.']
    Length: 20, dtype: str
    
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



```python
print("Équipes 2014 (Home Team Name) :", df_2014["Home Team Name"].unique()[:20])
print("\nVilles 2014 (City) :", df_2014["City"].unique()[:20])
print("\nStages 2014 (Stage) :", df_2014["Stage"].unique())
```

    Équipes 2014 (Home Team Name) : <ArrowStringArray>
    [         'Brazil',          'Mexico',           'Spain',           'Chile',
            'Colombia',         'Uruguay',         'England', 'Cï¿½te d'Ivoire',
         'Switzerland',          'France',       'Argentina',         'Germany',
             'IR Iran',           'Ghana',         'Belgium',          'Russia',
           'Australia',        'Cameroon',           'Japan',           'Italy']
    Length: 20, dtype: str
    
    Villes 2014 (City) : <ArrowStringArray>
    [     'Sao Paulo ',          'Natal ',       'Salvador ',         'Cuiaba ',
     'Belo Horizonte ',      'Fortaleza ',         'Manaus ',         'Recife ',
           'Brasilia ',   'Porto Alegre ', 'Rio De Janeiro ',       'Curitiba ']
    Length: 12, dtype: str
    
    Stages 2014 (Stage) : <ArrowStringArray>
    [                 'Group A',                  'Group B',
                      'Group C',                  'Group D',
                      'Group E',                  'Group F',
                      'Group G',                  'Group H',
                  'Round of 16',           'Quarter-finals',
                  'Semi-finals', 'Play-off for third place',
                        'Final']
    Length: 13, dtype: str


### **4. Détection et nettoyage des problèmes d’encodage**

#### **4.1 Fonction générique de détection d’encodage**


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
print("Problèmes d'encodage 1930–2010 :")
display(detect_encoding_issues(df_1930_2010))

print("\nProblèmes d'encodage 2014 :")
display(detect_encoding_issues(df_2014))
```

    Problèmes d'encodage 1930–2010 :



    {}


    
    Problèmes d'encodage 2014 :



    {}



### **5. Nettoyage minimal des chaînes (espaces, parenthèses, etc.)**



```python
# 2014 : suppression des espaces superflus
df_2014["City"] = df_2014["City"].str.strip()
df_2014["Home Team Name"] = df_2014["Home Team Name"].str.strip()
df_2014["Away Team Name"] = df_2014["Away Team Name"].str.strip()

# 1930–2010 : suppression des parenthèses dans les noms d'équipes
df_1930_2010["team1"] = df_1930_2010["team1"].str.replace(r"\(.*?\)", "", regex=True).str.strip()
df_1930_2010["team2"] = df_1930_2010["team2"].str.replace(r"\(.*?\)", "", regex=True).str.strip()

# 1930–2010 : nettoyage du champ 'venue' (suppression du point final)
df_1930_2010["venue"] = df_1930_2010["venue"].str.replace(".", "", regex=False).str.strip()

print("Nettoyage minimal effectué.")
```

    Nettoyage minimal effectué.


### **6. Nettoyage et harmonisation des noms d’équipes**

#### **6.1 Fonction `clean_team_name`**


```python
def clean_team_name(name):
    """
    Nettoie et harmonise un nom d'équipe provenant des datasets historiques FIFA.

    Étapes :
    1. Gère les valeurs manquantes.
    2. Supprime les artefacts HTML (ex: 'rn">Bosnia and Herzegovina').
    3. Corrige certains artefacts d'encodage (ex: 'Cï¿½te d'Ivoire').
    4. Normalise Unicode → ASCII via unidecode.
    5. Supprime les espaces superflus.
    6. Applique un mapping manuel pour harmoniser les variantes (historiques et modernes).

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

    name = str(name)

    # Artefacts HTML
    html_artifacts = ['rn">', 'rn&quot;&gt;', 'rn&quot;', 'rn&gt;', 'rn>']
    for art in html_artifacts:
        name = name.replace(art, "")

    # Corrections d'encodage spécifiques
    encoding_fixes = {
        "Cï¿½te d'Ivoire": "Cote d'Ivoire",
        "Ci? 1/2te d'Ivoire": "Cote d'Ivoire",
        "CÃ´te d'Ivoire": "Cote d'Ivoire",
        "CÃ´te dIvoire": "Cote d'Ivoire",
    }
    if name in encoding_fixes:
        name = encoding_fixes[name]

    # Normalisation Unicode → ASCII
    name = unidecode(name)

    # Trim
    name = name.strip()

    # Mapping manuel
    TEAM_MAPPING = {
        # Variantes modernes
        "IR Iran": "Iran",
        "Korea Republic": "South Korea",
        "USA": "United States",
        "Sao Tome e Principe": "Sao Tome and Principe",
        "Cote d'Ivoire": "Ivory Coast",

        # Artefacts HTML
        "Bosnia and Herzegovina": "Bosnia and Herzegovina",

        # Variantes historiques
        "Soviet Union": "Russia",
        "Yugoslavia": "Serbia",
        "Czechoslovakia": "Czech Republic",
        "FRG": "Germany",
        "Saarland": "Germany",
        "Irish Free State": "Ireland",

        # Cas particuliers
        "Curacao": "Curacao",
    }

    return TEAM_MAPPING.get(name, name)
```

#### **6.2 Application aux deux datasets**


```python
df_1930_2010["team1"] = df_1930_2010["team1"].apply(clean_team_name)
df_1930_2010["team2"] = df_1930_2010["team2"].apply(clean_team_name)

df_2014["Home Team Name"] = df_2014["Home Team Name"].apply(clean_team_name)
df_2014["Away Team Name"] = df_2014["Away Team Name"].apply(clean_team_name)

print("Équipes 1930–2010 après nettoyage :")
display(pd.concat([df_1930_2010["team1"], df_1930_2010["team2"]]).unique()[:50])

print("\nÉquipes 2014 après nettoyage :")
display(pd.concat([df_2014["Home Team Name"], df_2014["Away Team Name"]]).unique())
```

    Équipes 1930–2010 après nettoyage :



    <ArrowStringArray>
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


    
    Équipes 2014 après nettoyage :



    <ArrowStringArray>
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


### **7. Nettoyage et harmonisation des villes**

#### **7.1 Fonction `clean_city`**


```python

def clean_city(name):
    """
    Nettoie et harmonise un nom de ville provenant des datasets FIFA (1930–2014).

    Étapes :
    1. Gère les valeurs manquantes.
    2. Corrige des artefacts d'encodage observés.
    3. Normalise Unicode → ASCII via unidecode.
    4. Supprime les espaces superflus.
    5. Applique un mapping manuel minimal pour harmoniser les noms.
    """
    if pd.isna(name):
        return name

    name = str(name).strip()

    # Corrections d'encodage spécifiques
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

    # Normalisation Unicode
    name = unidecode(name)

    # Mapping manuel
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

        # Corrections supplémentaires
        "Geneve": "Geneva",
        "Genève": "Geneva",
    }

    name = name.strip()
    return CITY_MAPPING.get(name, name)
```

#### **7.2 Application aux deux datasets**


```python

df_1930_2010["venue"] = df_1930_2010["venue"].apply(clean_city)
df_2014["City"] = df_2014["City"].apply(clean_city)

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


### **8. Extraction des scores et du vainqueur (1930–2010)**

#### **8.1 Extraction des scores**


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
    match = re.match(r"(\d+)-(\d+)", str(score_str))
    if match:
        return int(match.group(1)), int(match.group(2))
    return None, None

df_1930_2010["home_result"], df_1930_2010["away_result"] = zip(
    *df_1930_2010["score"].apply(extract_scores)
)

df_1930_2010[["score", "home_result", "away_result"]].head()
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



#### **8.2 Extraction du vainqueur**


```python
# (Remarque : cette cellule intervient **avant** le renommage de `team1` / `team2`.)
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

df_1930_2010["result"] = df_1930_2010.apply(compute_result, axis=1)

df_1930_2010[["team1", "team2", "home_result", "away_result", "result"]].head()

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
      <td>United States</td>
      <td>Belgium</td>
      <td>3.0</td>
      <td>0.0</td>
      <td>United States</td>
    </tr>
    <tr>
      <th>2</th>
      <td>Serbia</td>
      <td>Brazil</td>
      <td>2.0</td>
      <td>1.0</td>
      <td>Serbia</td>
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



### **9. Harmonisation des rounds**


```python
#### **9.1 Fonction `clean_round`**
```


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

    # Groupes 2014 : Group A → group_stage
    if value.startswith("Group "):
        return "group_stage"

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

        # Valeurs résiduelles
        "SEMIFINAL_STAGE": "semi_final",
        "QUARTERFINAL_STAGE": "quarter_final",
    }

    return ROUND_MAPPING.get(value, value)
```

#### **9.2 Application aux deux datasets**


```python
df_1930_2010["round"] = df_1930_2010["round"].apply(clean_round)
df_2014["Stage"] = df_2014["Stage"].apply(clean_round)

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


### **10. Harmonisation des dates et des colonnes**

#### **10.1 Gestion de `year` et `date` pour 1930–2010**


```python
# On s'assure que 'year' est bien un entier
df_1930_2010["year"] = df_1930_2010["year"].astype(int)

# Si une colonne 'date' existait déjà, on la renomme en 'year' (sécurité)
if "date" in df_1930_2010.columns and "year" not in df_1930_2010.columns:
    df_1930_2010 = df_1930_2010.rename(columns={"date": "year"})

# Construction d'une date valide de type YYYY-01-01
df_1930_2010["date"] = pd.to_datetime(df_1930_2010["year"].astype(str) + "-01-01")

df_1930_2010[["year", "date"]].head()

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
      <th>year</th>
      <th>date</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1930</td>
      <td>1930-01-01</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1930</td>
      <td>1930-01-01</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1930</td>
      <td>1930-01-01</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1930</td>
      <td>1930-01-01</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1930</td>
      <td>1930-01-01</td>
    </tr>
  </tbody>
</table>
</div>



#### **10.2 Parsing de la date pour 2014**


```python
# Nettoyage préalable de la colonne Datetime
df_2014["Datetime"] = df_2014["Datetime"].str.strip()
df_2014["Datetime"] = df_2014["Datetime"].str.replace("\u00A0", " ", regex=False)

# Parsing robuste en datetime
df_2014["date"] = pd.to_datetime(df_2014["Datetime"], dayfirst=True)

df_2014["date"].head()
df_2014[df_2014["date"].isna()].head(100)
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
  </tbody>
</table>
</div>



#### **10.3 Harmonisation des noms de colonnes (lower_snake_case)**


```python
# 2014 : renommage des colonnes en snake_case cohérent
df_2014 = df_2014.rename(columns={
    "Year": "year",
    "Home Team Name": "home_team",
    "Away Team Name": "away_team",
    "Home Team Goals": "home_result",
    "Away Team Goals": "away_result",
    "City": "city",
    "Stadium": "stadium",
    "Stage": "round",
    "Win conditions": "win_conditions",
    "Attendance": "attendance",
    "Half-time Home Goals": "half_time_home_goals",
    "Half-time Away Goals": "half_time_away_goals",
    "Referee": "referee",
    "Assistant 1": "assistant_1",
    "Assistant 2": "assistant_2",
    "RoundID": "round_id",
    "MatchID": "match_id",
    "Home Team Initials": "home_team_initials",
    "Away Team Initials": "away_team_initials",
    "Datetime": "datetime_raw"
})

df_2014.columns

```




    Index(['year', 'datetime_raw', 'round', 'stadium', 'city', 'home_team',
           'home_result', 'away_result', 'away_team', 'win_conditions',
           'attendance', 'half_time_home_goals', 'half_time_away_goals', 'referee',
           'assistant_1', 'assistant_2', 'round_id', 'match_id',
           'home_team_initials', 'away_team_initials', 'date'],
          dtype='str')




```python
# 1930–2010 : renommage de venue → city, team1/team2 → home_team/away_team
df_1930_2010 = df_1930_2010.rename(columns={
    "team1": "home_team",
    "team2": "away_team",
    "venue": "city"
})

df_1930_2010.columns
```




    Index(['edition', 'round', 'score', 'home_team', 'away_team', 'url', 'city',
           'year', 'home_result', 'away_result', 'result', 'date'],
          dtype='str')



### **11. Nettoyage des doublons après harmonisation**


```python
df_2014 = df_2014.drop_duplicates()
print("Taille 2014 après suppression des doublons :", len(df_2014))

df_1930_2010 = df_1930_2010.drop_duplicates()
print("Taille 1930–2010 après suppression des doublons :", len(df_1930_2010))
```

    Taille 2014 après suppression des doublons : 64
    Taille 1930–2010 après suppression des doublons : 7299


### **12. Construction des DataFrames finaux**

#### **12.1 Dataset 1930–2014 (qualifications + finales jusqu’à 2010)**


```python
df_final_1930_2014_qualif = df_1930_2010.copy()

# On garde toutes les colonnes utiles, avec schéma harmonisé :
# edition, round, score, home_team, away_team, url, city, year, home_result, away_result, result, date

df_final_1930_2014_qualif.info()

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
     6   city         7299 non-null   str           
     7   year         7299 non-null   int64         
     8   home_result  7235 non-null   float64       
     9   away_result  7235 non-null   float64       
     10  result       7299 non-null   str           
     11  date         7299 non-null   datetime64[us]
    dtypes: datetime64[us](1), float64(2), int64(1), str(8)
    memory usage: 1.2 MB



```python
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
      <th>city</th>
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
      <td>1930-01-01</td>
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
      <td>United States</td>
      <td>1930-01-01</td>
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
      <td>Serbia</td>
      <td>1930-01-01</td>
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
      <td>1930-01-01</td>
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
      <td>1930-01-01</td>
    </tr>
  </tbody>
</table>
</div>



#### **12.2 Dataset 2014 (phase finale complète)**


```python
df_final_2014_finals = df_2014.copy()

# On garde toutes les colonnes, y compris datetime_raw (source) et date (datetime64)
df_final_2014_finals.info()
df_final_2014_finals.head()
```

    <class 'pandas.DataFrame'>
    RangeIndex: 64 entries, 0 to 63
    Data columns (total 21 columns):
     #   Column                Non-Null Count  Dtype         
    ---  ------                --------------  -----         
     0   year                  64 non-null     int64         
     1   datetime_raw          64 non-null     str           
     2   round                 64 non-null     str           
     3   stadium               64 non-null     str           
     4   city                  64 non-null     str           
     5   home_team             64 non-null     str           
     6   home_result           64 non-null     int64         
     7   away_result           64 non-null     int64         
     8   away_team             64 non-null     str           
     9   win_conditions        64 non-null     str           
     10  attendance            63 non-null     float64       
     11  half_time_home_goals  64 non-null     int64         
     12  half_time_away_goals  64 non-null     int64         
     13  referee               64 non-null     str           
     14  assistant_1           64 non-null     str           
     15  assistant_2           64 non-null     str           
     16  round_id              64 non-null     int64         
     17  match_id              64 non-null     int64         
     18  home_team_initials    64 non-null     str           
     19  away_team_initials    64 non-null     str           
     20  date                  64 non-null     datetime64[us]
    dtypes: datetime64[us](1), float64(1), int64(7), str(12)
    memory usage: 19.7 KB





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
      <th>year</th>
      <th>datetime_raw</th>
      <th>round</th>
      <th>stadium</th>
      <th>city</th>
      <th>home_team</th>
      <th>home_result</th>
      <th>away_result</th>
      <th>away_team</th>
      <th>win_conditions</th>
      <th>attendance</th>
      <th>half_time_home_goals</th>
      <th>half_time_away_goals</th>
      <th>referee</th>
      <th>assistant_1</th>
      <th>assistant_2</th>
      <th>round_id</th>
      <th>match_id</th>
      <th>home_team_initials</th>
      <th>away_team_initials</th>
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



#### **12.3 Harmonisation finale des schémas pour fusion (1930–2022)**


```python
### -----------------------------------------------------------
### 12.3 Harmonisation finale des schémas pour fusion (1930–2022)
### -----------------------------------------------------------

"""
Objectif :
Créer un schéma unique pour tous les datasets (1930–2014, 2014 finals, 2018, 2022)
afin de permettre la fusion dans le notebook 04.

Schéma final cible :
    home_team
    away_team
    home_result
    away_result
    result
    date
    round
    city
    stadium
    edition
"""

# -----------------------------
# 1) Harmonisation 1930–2014
# -----------------------------

df_final_1930_2014 = df_final_1930_2014_qualif.copy()

# Ajout colonne stadium absente dans ce dataset
df_final_1930_2014["stadium"] = None

# Réorganisation des colonnes selon le schéma final
df_final_1930_2014 = df_final_1930_2014[[
    "home_team", "away_team",
    "home_result", "away_result", "result",
    "date", "round", "city", "stadium", "edition"
]]


# -----------------------------
# 2) Harmonisation 2014 finals
# -----------------------------

df_final_2014 = df_final_2014_finals.copy()

# Recalcul du vainqueur (2014 n'avait pas de colonne result)
df_final_2014["result"] = df_final_2014.apply(
    lambda row: (
        row["home_team"] if row["home_result"] > row["away_result"]
        else row["away_team"] if row["home_result"] < row["away_result"]
        else "draw"
    ),
    axis=1
)

# Ajout de la colonne edition si absente
if "edition" not in df_final_2014.columns:
    df_final_2014["edition"] = "2014-BRAZIL"

# Réorganisation des colonnes
df_final_2014 = df_final_2014[[
    "home_team", "away_team",
    "home_result", "away_result", "result",
    "date", "round", "city", "stadium", "edition"
]]


# -----------------------------
# 3) Vérification stricte du schéma
# -----------------------------

schema_1930_2014 = list(df_final_1930_2014.columns)
schema_2014 = list(df_final_2014.columns)

assert schema_1930_2014 == schema_2014, "Les schémas 1930–2014 et 2014 ne correspondent pas !"

print("Schéma final harmonisé OK :")
print(schema_1930_2014)

```

    Schéma final harmonisé OK :
    ['home_team', 'away_team', 'home_result', 'away_result', 'result', 'date', 'round', 'city', 'stadium', 'edition']


### **13. Export des datasets nettoyés**


```python
# Export CSV + Parquet 1930–2014 (qualifs + finales jusqu'à 2010)
df_final_1930_2014.to_csv(DATA_CLEAN / "matches_1930_2014_clean.csv", index=False)
df_final_1930_2014.to_parquet(DATA_CLEAN / "matches_1930_2014_clean.parquet", index=False)
```


```python
# Export CSV + Parquet 2014 (phase finale)
df_final_2014.to_csv(DATA_CLEAN / "matches_2014_clean.csv", index=False)
df_final_2014.to_parquet(DATA_CLEAN / "matches_2014_clean.parquet", index=False)
```

### **14. Petite note SQL / cohérence de schéma**

- La colonne `year` est un entier dans tous les datasets.
- La colonne `date` est de type datetime :
  - `NaT` pour 1930–2010 (sera NULL en SQL dans la plupart des SGBD).
  - Datetime complet pour 2014.
- Les noms de colonnes sont harmonisés en `snake_case` :
  - `home_team`, `away_team`, `home_result`, `away_result`, `round`, `city`, `stadium`, etc.
- `city` est utilisé partout (ancien `venue` renommé).


```python

```
