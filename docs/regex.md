---

# 🎯 1) Comprendre les regex (vraiment, simplement)

Les regex (*expressions régulières*) sont un mini‑langage pour reconnaître des motifs dans du texte.

---

## 🟦 A. Les parenthèses : `(...)`

Elles servent à **capturer** une partie du texte.

Exemple dans ton code :

```python
r"(\d+)-(\d+)"
```

Cela signifie :

- `(\d+)` → capture un ou plusieurs chiffres  
- `-` → un tiret littéral  
- `(\d+)` → capture un ou plusieurs chiffres  

Donc la regex reconnaît :

- `4-1`
- `12-0`
- `3-2`

Et `match.group(1)` = score équipe 1  
`match.group(2)` = score équipe 2

---

## 🟦 B. Le point d’interrogation : `?`

Il signifie “**0 ou 1 fois**”.

Dans ton nettoyage :

```python
r"\(.*?\)"
```

Décomposons :

- `\(` → parenthèse ouvrante littérale  
- `.*?` → n’importe quel caractère, le moins possible  
- `\)` → parenthèse fermante littérale  

Donc ça supprime :

- `(Brasil)`  
- `(România)`  
- `(België)`  
- `(MÉXICO)`  

C’est exactement ce qu’il faut pour nettoyer les noms d’équipes dans 1930–2010.

---

## 🟦 C. Le `*` : “0 ou plusieurs fois”

Dans `.*?` :

- `.` = n’importe quel caractère  
- `*` = répété 0, 1, 2, … fois  
- `?` = version “non gourmande” (prend le minimum)

---

## 🟦 D. Le `|` : OU logique

Dans :

```python
"Ã|Ð|¿|�"
```

Cela signifie :  
→ “contient **Ã** OU **Ð** OU **¿** OU **�**”

C’est une technique simple pour détecter les artefacts d’encodage.

---
