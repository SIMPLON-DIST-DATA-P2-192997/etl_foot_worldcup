### **Imports + configuration**


```python
import pandas as pd
from pathlib import Path

DATA_CLEAN = Path("..") / "data_clean"

pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 100)
```

### **Chargement des fichiers propres**


```python
df_1930_2014 = pd.read_csv(DATA_CLEAN / "matches_1930_2014_clean.csv")
df_2014 = pd.read_csv(DATA_CLEAN / "matches_2014_clean.csv")
df_2018 = pd.read_csv(DATA_CLEAN / "matches_2018_clean.csv")
df_2022 = pd.read_csv(DATA_CLEAN / "matches_2022_clean.csv")

df_1930_2014.head(), df_2014.head(), df_2018.head(), df_2022.head()
```




    (       home_team away_team  home_result  away_result         result  \
     0         France    Mexico          4.0          1.0         France   
     1  United States   Belgium          3.0          0.0  United States   
     2         Serbia    Brazil          2.0          1.0         Serbia   
     3        Romania      Peru          3.0          1.0        Romania   
     4      Argentina    France          1.0          0.0      Argentina   
     
              date        round        city  stadium       edition  
     0  1930-01-01  group_stage  Montevideo      NaN  1930-URUGUAY  
     1  1930-01-01  group_stage  Montevideo      NaN  1930-URUGUAY  
     2  1930-01-01  group_stage  Montevideo      NaN  1930-URUGUAY  
     3  1930-01-01  group_stage  Montevideo      NaN  1930-URUGUAY  
     4  1930-01-01  group_stage  Montevideo      NaN  1930-URUGUAY  ,
       home_team    away_team  home_result  away_result       result  \
     0    Brazil      Croatia            3            1       Brazil   
     1    Mexico     Cameroon            1            0       Mexico   
     2     Spain  Netherlands            1            5  Netherlands   
     3     Chile    Australia            3            1        Chile   
     4  Colombia       Greece            3            0     Colombia   
     
                       date        round            city             stadium  \
     0  2014-06-12 17:00:00  group_stage       Sao Paulo  Arena de Sao Paulo   
     1  2014-06-13 13:00:00  group_stage           Natal   Estadio das Dunas   
     2  2014-06-13 16:00:00  group_stage        Salvador    Arena Fonte Nova   
     3  2014-06-13 18:00:00  group_stage          Cuiaba      Arena Pantanal   
     4  2014-06-14 13:00:00  group_stage  Belo Horizonte    Estadio Mineirao   
     
            edition  
     0  2014-BRAZIL  
     1  2014-BRAZIL  
     2  2014-BRAZIL  
     3  2014-BRAZIL  
     4  2014-BRAZIL  ,
       home_team     away_team  home_result  away_result   result  \
     0    Russia  Saudi Arabia            5            0   Russia   
     1     Egypt       Uruguay            0            1  Uruguay   
     2    Russia         Egypt            3            1   Russia   
     3   Uruguay  Saudi Arabia            1            0  Uruguay   
     4   Uruguay        Russia            3            0  Uruguay   
     
                       date    round              city             stadium  \
     0  2018-06-14 15:00:00  Group A            Moscow    Luzhniki Stadium   
     1  2018-06-15 12:00:00  Group A     Yekaterinburg     Central Stadium   
     2  2018-06-19 18:00:00  Group A  Saint Petersburg  Krestovsky Stadium   
     3  2018-06-20 15:00:00  Group A     Rostov-on-Don        Rostov Arena   
     4  2018-06-25 14:00:00  Group A            Samara        Cosmos Arena   
     
            edition  
     0  2018-RUSSIA  
     1  2018-RUSSIA  
     2  2018-RUSSIA  
     3  2018-RUSSIA  
     4  2018-RUSSIA  ,
          home_team    away_team  home_result  away_result       result  \
     0        Qatar      Ecuador            0            2      Ecuador   
     1      Senegal  Netherlands            0            2  Netherlands   
     2        Qatar      Senegal            1            3      Senegal   
     3  Netherlands      Ecuador            1            1         draw   
     4      Ecuador      Senegal            1            2      Senegal   
     
                       date        round       city                        stadium  \
     0  2022-11-20 19:00:00   Matchday 1    Al Khor                Al Bayt Stadium   
     1  2022-11-21 19:00:00   Matchday 2       Doha             Al Thumama Stadium   
     2  2022-11-25 16:00:00   Matchday 6       Doha             Al Thumama Stadium   
     3  2022-11-25 19:00:00   Matchday 6  Al Rayyan  Khalifa International Stadium   
     4  2022-11-29 18:00:00  Matchday 10  Al Rayyan  Khalifa International Stadium   
     
           edition  
     0  2022-QATAR  
     1  2022-QATAR  
     2  2022-QATAR  
     3  2022-QATAR  
     4  2022-QATAR  )



### **Vérification du schéma**


```python
datasets = {
    "1930_2014": df_1930_2014,
    "2014_finals": df_2014,
    "2018": df_2018,
    "2022": df_2022
}

for name, df in datasets.items():
    print(f"Colonnes {name} :", df.columns.tolist())

# Vérification stricte
all_same_schema = len({tuple(df.columns) for df in datasets.values()}) == 1
all_same_schema
```

    Colonnes 1930_2014 : ['home_team', 'away_team', 'home_result', 'away_result', 'result', 'date', 'round', 'city', 'stadium', 'edition']
    Colonnes 2014_finals : ['home_team', 'away_team', 'home_result', 'away_result', 'result', 'date', 'round', 'city', 'stadium', 'edition']
    Colonnes 2018 : ['home_team', 'away_team', 'home_result', 'away_result', 'result', 'date', 'round', 'city', 'stadium', 'edition']
    Colonnes 2022 : ['home_team', 'away_team', 'home_result', 'away_result', 'result', 'date', 'round', 'city', 'stadium', 'edition']





    True



### **Fusion des datasets**


```python
df_all = pd.concat(
    [df_1930_2014, df_2014, df_2018, df_2022],
    ignore_index=True
)

df_all.head()
df_all[df_all["date"].isna()].head(20)
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



### **Vérifications de qualité globales**

#### **Inspection s'il y a des NaN**


```python
df_all.isna().sum()
```




    home_team         0
    away_team         0
    home_result      64
    away_result      64
    result            0
    date              0
    round             0
    city              0
    stadium        7299
    edition           0
    dtype: int64



#### **Inspection s'il y a des doublons**


```python
df_all.duplicated().sum()
```




    np.int64(1)



#### **Vérification des types**


```python
df_all.dtypes
```




    home_team          str
    away_team          str
    home_result    float64
    away_result    float64
    result             str
    date               str
    round              str
    city               str
    stadium         object
    edition            str
    dtype: object



#### **Inspection s'il y a des scores négatifs**


```python
df_all[(df_all["home_result"] < 0) | (df_all["away_result"] < 0)]
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



#### **Vérification que les éditions sont présentes**


```python
df_all["edition"].value_counts()
```




    edition
    2014-BRAZIL          948
    2010-SOUTH AFRICA    917
    2006-GERMANY         911
    2002-KOREA/JAPAN     841
    1998-FRANCE          708
    1994-USA             550
    1990-ITALY           367
    1986-MEXICO          364
    1982-SPAIN           358
    1978-ARGENTINA       290
    1974-FRG             263
    1970-MEXICO          204
    1966-ENGLAND         159
    1958-SWEDEN          125
    1962-CHILE           124
    1954-SWITZERLAND      83
    2018-RUSSIA           64
    2022-QATAR            64
    1950-BRAZIL           50
    1934-ITALY            43
    1938-FRANCE           40
    1930-URUGUAY          18
    Name: count, dtype: int64



### **Export du dataset fusionné**


```python
output_csv = DATA_CLEAN / "matches_1930_2022_clean.csv"
output_parquet = DATA_CLEAN / "matches_1930_2022_clean.parquet"

df_all.to_csv(output_csv, index=False)
df_all.to_parquet(output_parquet, index=False)
```


```python

```
