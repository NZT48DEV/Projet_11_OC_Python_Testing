# 🏎️ Rapport de Performance — Projet Gudlft

## 🎯 Objectifs de performance (exigences OC)

Conformément aux consignes officielles du projet :

1.  **Même pour un MVP**, viser un code rapide et propre.
2.  **Temps de chargement maximum : 5 secondes** (routes GET).
3.  **Temps d'opération maximum : 2 secondes** (POST /showSummary).
4.  **Tests exécutés avec au moins 6 utilisateurs simulés** (Locust).

Notre suite Locust a été améliorée pour tester désormais **toutes les routes critiques :**

-   `/`
-   `/pointsBoard`
-   `/book/<competition>/<club>`
-   `/purchasePlaces`
-   `/showSummary`

## 🧪 Méthodologie de test

- Outil utilisé : **Locust 2.42**
- Nombre d'utilisateurs simulés : **6**
- Taux de spawn : **1 utilisateur/seconde**
- Test en local : `http://127.0.0.1:5000`
- Scénarios réalistes sans temporisation

## 📊 Résultats détaillés

### 1. Page d'accueil — `GET /`

| Métrique | Valeur |
|---------|---------|
| Médiane | **2 ms** |
| 95ᵉ     | **4 ms** |
| Max     | **4 ms** |
| Échecs  | **0** |

### 2. Page booking — `GET /book/<competition>/<club>`

| Métrique | Valeur |
|---------|---------|
| Médiane | **3 ms** |
| 95ᵉ     | **6 ms** |
| Max     | **6 ms** |
| Échecs  | **0** |

### 3. Tableau des points — `GET /pointsBoard`

| Métrique | Valeur |
|---------|---------|
| Médiane | **3 ms** |
| 95ᵉ     | **4 ms** |
| Max     | **4 ms** |
| Échecs  | **0** |

### 4. Achat de places — `POST /purchasePlaces`

| Métrique | Valeur |
|---------|---------|
| Médiane | **3 ms** |
| 95ᵉ     | **7 ms** |
| Max     | **7 ms** |
| Échecs  | **0** |

### 5. Connexion — `POST /showSummary`

| Métrique | Valeur |
|---------|---------|
| Médiane | **3 ms** |
| 95ᵉ     | **8 ms** |
| Max     | **8 ms** |
| Échecs  | **0** |

## 📌 Synthèse globale

| Route             | Type | Médiane | Max | Limite OC | Conforme ? |
|-------------------|------|---------|-----|-----------|------------|
| `/`               | GET  | 2 ms    | 4 ms | < 5 s     | ✔️ |
| `/book/...`       | GET  | 3 ms    | 6 ms | < 5 s     | ✔️ |
| `/pointsBoard`    | GET  | 3 ms    | 4 ms | < 5 s     | ✔️ |
| `/purchasePlaces` | POST | 3 ms    | 7 ms | < 2 s     | ✔️ |
| `/showSummary`    | POST | 3 ms    | 8 ms | < 2 s     | ✔️ |

## 🟢 Conclusion

L'application respecte pleinement les exigences de performance et reste stable même sous charge simulée.
