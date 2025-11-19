# Rapport de Performance — Projet Güdlft

## 🎯 Objectif

Conformément aux exigences de la phase 2 :

-   **le temps de chargement ne doit jamais dépasser 5 secondes**
-   **les mises à jour ne doivent pas dépasser 2 secondes**
-   testés via **Locust**, avec un minimum de **6 utilisateurs
    simultanés**

------------------------------------------------------------------------

## 🧪 Méthodologie

Les tests ont été réalisés avec **6 utilisateurs simultanés**,
conformément à la recommandation OC d'un test léger, sur :

-   Endpoint public : `GET /pointsBoard`
-   Mise à jour légère : `POST /showSummary`

Le serveur testé est l'application Flask locale fournie.

------------------------------------------------------------------------

## 📊 Résultats

### **1. Chargement des pages (GET /pointsBoard)**

  Metric           Valeur
  ---------------- -----------
  Médiane          **4 ms**
  95e percentile   **6 ms**
  Max              **7 ms**
  Fails            **0**

➡️ **Résultat : largement en dessous du seuil de 5 secondes.**

------------------------------------------------------------------------

### **2. Mises à jour (POST /showSummary)**

  Metric           Valeur
  ---------------- -----------
  Médiane          **4 ms**
  95e percentile   **6 ms**
  Max              **14 ms**
  Fails            **0**

➡️ **Résultat : conforme au seuil de 2 secondes.**

------------------------------------------------------------------------

### **3. Stabilité**

-   **0 erreurs** sur plus de **50 requêtes**
-   Temps de réponse stables
-   RPS moyen : 0

➡️ Le serveur Flask tient parfaitement la charge prévue.

------------------------------------------------------------------------

## 🟢 Conclusion

✔️ Les temps de chargement sont inférieurs à 5 secondes
✔️ Les mises à jour sont inférieures à 2 secondes
✔️ Aucun échec
✔️ Application stable et conforme aux exigences QA

> *"Les performances de l'application Güdlft sont validées."*
