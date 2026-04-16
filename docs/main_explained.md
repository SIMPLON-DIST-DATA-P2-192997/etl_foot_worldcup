# 📄 **Documentation : main.py — Orchestration du pipeline ETL**

## 🎯 Rôle du fichier `main.py`

Le fichier `main.py` est **le point d’entrée unique** du pipeline ETL.  
Il orchestre les trois étapes principales :

1. **Extraction** du dataset nettoyé  
2. **Transformation** en tables normalisées  
3. **Chargement** dans MySQL  

Il assure également :

- la configuration du système de logs  
- le chargement de la configuration MySQL  
- la gestion des erreurs globales  
- la reproductibilité du pipeline  

---

## 🟦 1) Structure générale du fichier

```python
def main():
    setup_logging()
    df = extract_matches(...)
    tables = transform_matches(df)
    config = load_config(...)
    load_all_tables(tables, config)
```

Chaque étape est clairement séparée, ce qui rend le pipeline :

- lisible  
- maintenable  
- testable  
- conforme aux bonnes pratiques ETL  

---

## 🟦 2) Étape 1 — Logging

`setup_logging()` configure :

- un fichier `logs/etl.log`  
- un affichage console  
- un format standardisé  

Cela permet :

- de suivre l’exécution  
- de diagnostiquer les erreurs  
- de fournir une trace exploitable dans un rapport  

---

## 🟦 3) Étape 2 — Extraction

`extract_matches()` :

- lit le fichier CSV final  
- valide les colonnes  
- convertit la colonne date  
- renvoie un DataFrame Pandas  

Cette étape ne modifie pas les données :  
👉 elle garantit simplement que l’entrée est propre.

---

## 🟦 4) Étape 3 — Transformation

`transform_matches()` :

- génère les tables dimensionnelles  
- crée les mappings texte → identifiant  
- applique les mappings au DataFrame principal  
- construit la table de faits `match`  
- renvoie un dictionnaire de DataFrames  

Cette étape correspond à la **normalisation relationnelle**.

---

## 🟦 5) Étape 4 — Chargement MySQL

`load_all_tables()` :

- ouvre une connexion MySQL  
- démarre une transaction  
- insère les dimensions  
- insère la table de faits  
- commit si tout est OK  
- rollback en cas d’erreur  

Cette étape garantit :

- la cohérence des clés étrangères  
- l’intégrité du schéma  
- la reproductibilité du chargement  

---

## 🟦 6) Exécution du pipeline

Le bloc :

```python
if __name__ == "__main__":
    main()
```

permet d’exécuter le pipeline via :

```
python main.py
```

---

## 🟩 Conclusion

Le fichier `main.py` constitue la **colonne vertébrale** du pipeline ETL.  
Il assure une orchestration claire, robuste et professionnelle, parfaitement adaptée à un projet de data engineering.

---