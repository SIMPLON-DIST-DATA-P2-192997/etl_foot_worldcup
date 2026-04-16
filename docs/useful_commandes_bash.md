## **Commandes bash utiles**

### 🟩 **Convertir un notebook dans un autre format**

jupyter nbconvert --to markdown file.ipynb

jupyter nbconvert --to html file.ipynb

---

## 🟩 **Afficher les premières lignes d’un fichier**

```bash
head -n 20 worldcup_2022.json
```

---

## 🟩 **Afficher les dernières lignes**

```bash
tail -n 20 worldcup_2022.json
```

---

## 🟩 **Rechercher un mot dans un fichier**

```bash
grep "score" worldcup_2022.json
```

---

## 🟩 **Rechercher un motif avec contexte**

```bash
grep -n "goals" worldcup_2022.json
```

---

## 🟩 **Compter les occurrences**

```bash
grep -c "Matchday" worldcup_2022.json
```

---

## 🟩 **Afficher les lignes contenant un mot, avec numéros**

```bash
grep -n "Argentina" worldcup_2022.json
```

---

## 🟩 **Afficher la structure JSON avec jq (si installé)**

```bash
jq '.' worldcup_2022.json
```

---

## 🟩 **Créer les tables d'une base de données (bdd) déjà créée sous MySQL à partir d'un fichier sql**

```bash
mysql -u root -p bdd_name < path/file.sql
```
