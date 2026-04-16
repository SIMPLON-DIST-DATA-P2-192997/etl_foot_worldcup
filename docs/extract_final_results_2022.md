## **Extraction des scores finaux**

```python
df_2022_raw["home_result"] = df_2022_raw["score"].apply(lambda s: s.get("ft", [None, None])[0])
df_2022_raw["away_result"] = df_2022_raw["score"].apply(lambda s: s.get("ft", [None, None])[1])
```

---

### 🟦 1) Pourquoi cette ligne existe ?

Dans le JSON 2022, chaque match contient un champ `score` :

```json
"score": {"ft": [0, 2], "ht": [0, 2]}
```

Ce champ est un **dictionnaire**, pas une valeur simple.

On doit donc extraire :

- le score final de l’équipe 1 → `ft[0]`
- le score final de l’équipe 2 → `ft[1]`

Mais attention :  
👉 certains matchs n’ont **pas** de score complet (ex : match annulé, données manquantes, ou structure différente comme les tirs au but).

Donc on doit écrire un code **robuste**, qui ne plante jamais.

---

### 🟦 2) Décomposition de la ligne

Prenons :

```python
df_2022_raw["score"].apply(lambda s: s.get("ft", [None, None])[0])
```

#### ✔️ Étape 1 — `df_2022_raw["score"]`  
C’est une colonne contenant des dictionnaires :

```python
{'ft': [0, 2], 'ht': [0, 2]}
{'ft': [1, 1]}
{'ft': [3, 0], 'ht': [2, 0], 'et': [3, 0]}
{'p': [4, 2], 'et': [3, 3], 'ft': [2, 2]}
```

#### ✔️ Étape 2 — `.apply(lambda s: ...)`  
On applique une fonction à chaque dictionnaire `s`.

#### ✔️ Étape 3 — `s.get("ft", [None, None])`  
`.get()` est utilisé pour éviter une erreur si `"ft"` n’existe pas.

- Si `"ft"` existe → retourne `[home, away]`
- Si `"ft"` n’existe pas → retourne `[None, None]`

Exemples :

| score | s.get("ft", [None, None]) |
|-------|----------------------------|
| `{"ft": [1,2]}` | `[1,2]` |
| `{"p": [4,2], "et": [3,3]}` | `[None, None]` |
| `{}` | `[None, None]` |

👉 **C’est une sécurité indispensable**.

#### ✔️ Étape 4 — `[0]` ou `[1]`  
On prend :

- `[0]` → score de l’équipe 1  
- `[1]` → score de l’équipe 2  

---

### 🟦 3) Résultat final

On obtient deux colonnes propres :

| team1 | team2 | score | home_result | away_result |
|-------|--------|--------|--------------|--------------|
| Qatar | Ecuador | {"ft":[0,2]} | 0 | 2 |
| Senegal | Netherlands | {"ft":[0,2]} | 0 | 2 |
| Japan | Croatia | {"p":[1,3],"ft":[1,1]} | 1 | 1 |
| Morocco | Spain | {"p":[3,0],"ft":[0,0]} | 0 | 0 |

Même dans les cas complexes (prolongations, tirs au but), on récupère **le score final réglementaire**, ce qui est cohérent avec ton dataset 1930–2018.

---

### 🟦 4) Pourquoi ne pas utiliser les tirs au but ?

Parce que :

- 1930–2018 n’a **jamais** stocké les tirs au but  
- ton modèle SQL futur ne prévoit pas de colonnes pour les tirs au but  
- les tirs au but ne sont pas des “buts” mais une procédure de départage  
- pour l’analyse statistique, on utilise toujours le score réglementaire

---