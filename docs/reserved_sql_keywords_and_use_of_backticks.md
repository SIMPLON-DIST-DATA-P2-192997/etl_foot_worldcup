---

# 🎯 Pourquoi écrire :

```sql
DROP TABLE IF EXISTS `match`;
```

et **pas** :

```sql
DROP TABLE IF EXISTS match;
```

La réponse tient en **un seul point** :

# 🟥 **`match` est un mot réservé en SQL (MySQL, PostgreSQL, Oracle, etc.)**

Dans MySQL, `MATCH` est utilisé pour :

- `MATCH ... AGAINST` (full‑text search)
- la syntaxe de recherche booléenne
- certaines clauses internes du parser SQL

Donc, quand on écrit :

```sql
DROP TABLE IF EXISTS match;
```

MySQL lit :

- `DROP TABLE IF EXISTS` → OK  
- `match` → ❌ *mot réservé, ambigu, MySQL ne sait pas si tu veux utiliser la clause MATCH ou un identifiant*

C’est exactement ce qui a provoqué ton erreur précédente :

```
ERROR 1064 ... near 'match ( ... )'
```

---

# 🟩 Comment MySQL sait que tu parles d’un **nom de table** et non d’un mot réservé ?

👉 En utilisant les **backticks** :

```
`match`
```

Les backticks signifient :

> « Ceci est un identifiant SQL, pas un mot réservé. »

C’est la même logique que pour :

- `order`  
- `group`  
- `user`  
- `rank`  
- `index`  
- `key`  
- `value`  

Tous ces mots peuvent être des noms de colonnes ou de tables **si** tu les écris entre backticks.

---

# 🟦 Donc :  
### ✔ `DROP TABLE IF EXISTS \`match\`;` → correct  
### ❌ `DROP TABLE IF EXISTS match;` → erreur potentielle

---

# 🟧 Bonus : Vérifier la liste complète des mots réservés MySQL

Dans MySQL :

```sql
SHOW KEYWORDS;
```

`MATCH` est dans la liste.

---