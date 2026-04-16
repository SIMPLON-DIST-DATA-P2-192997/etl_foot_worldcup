Explication : comment `pd.concat()` fusionne deux colonnes

Voici une cellule de notebook où l'on utilise cette méthode :

```python
teams_1930_2010 = pd.concat([df_1930_2010["team1"], df_1930_2010["team2"]]).unique()
```

👉 **pd.concat() empile les deux colonnes l’une sous l’autre.**

Visuellement :

```
team1
France
USA
Yugoslavia
...

team2
Mexico
Belgium
Brazil
...
```

Après concaténation :

```
France
USA
Yugoslavia
...
Mexico
Belgium
Brazil
...
```

Puis `.unique()` enlève les doublons.

C’est la méthode la plus simple pour obtenir **la liste complète des équipes** présentes dans un dataset.

---
