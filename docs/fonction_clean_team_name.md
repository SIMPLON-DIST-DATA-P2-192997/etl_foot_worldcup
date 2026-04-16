---

# 🟦 1) Explication détaillée : `if pd.isna(name): return name`

Dans la fonction clean_team_name() :

```python
if pd.isna(name):
    return name
```

👉 **Ce test sert à éviter une erreur si la valeur est NaN.**

Pourquoi ?

- `unidecode(name)` plante si `name = NaN`
- `.strip()` plante aussi
- `.get(name, name)` ne pose pas de problème, mais on n’y arriverait jamais

Donc cette ligne signifie :

> “Si la valeur est manquante, je la renvoie telle quelle et je ne tente pas de la nettoyer.”

C’est une **bonne pratique** dans toutes les fonctions de nettoyage.

---

# 🟦 2) Explication détaillée : `TEAM_MAPPING.get(name, name)`

Dans Python, un dictionnaire `.get()` fonctionne comme ceci :

```python
TEAM_MAPPING.get(clef, valeur_par_defaut)
```

Donc :

```python
TEAM_MAPPING.get(name, name)
```

signifie :

> “Si `name` est une clé du dictionnaire TEAM_MAPPING, renvoie la valeur associée.  
> Sinon, renvoie `name` tel quel.”

Exemples :

```python
TEAM_MAPPING = {"USA": "United States"}

TEAM_MAPPING.get("USA", "USA")  → "United States"
TEAM_MAPPING.get("France", "France") → "France"
```

C’est une manière élégante d’appliquer un mapping **sans if/else**.

---