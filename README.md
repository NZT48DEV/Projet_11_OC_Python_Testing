# 🏋️‍♂️ GudLFT --- Projet OpenClassrooms : Tests & Qualité logicielle

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)
![Pytest](https://img.shields.io/badge/tests-pytest-green)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
![Locust](https://img.shields.io/badge/Performance-Locust-orange)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-inactive)

Ce dépôt contient l'application **GudLFT Reservation** ainsi que
l'ensemble des tests permettant d'assurer une qualité applicative
élevée.

------------------------------------------------------------------------

# 📌 Contexte du projet

Dans le cadre du parcours **Développeur d'application Python**, ce
projet consiste à :

-   Identifier et corriger des bugs (7 issues au total)
-   Renforcer l'application avec des tests **unitaires, intégration,
    fonctionnels et performance**
-   Structurer un pipeline QA complet
-   Préparer le terrain pour traiter les issues suivantes de manière
    fiable

Ce README décrit les issues corrigées, ainsi que l'infrastructure mise
en place pour la suite.

------------------------------------------------------------------------

# Issue 1 --- Crash sur email invalide (corrigé)

### ❗ Problème

La route `/showSummary` plantait lorsqu'un utilisateur saisissait un
email inconnu.

### ✔ Correction

-   Remplacement du `[0]` par `next(..., None)` pour éviter l'IndexError
-   Gestion propre des erreurs
-   Ajout d'un message utilisateur via `flash()`
-   Support GET/POST pour `/showSummary`
-   Tests robustes sur 3 niveaux (unitaire, intégration, fonctionnel)

------------------------------------------------------------------------

# Issue 2 --- Empêcher la réservation si le club n'a pas assez de points (corrigé)

### ❗ Problème

Un club pouvait réserver plus de places que ses points disponibles.

### ✔ Correction

-   Ajout de la fonction **`can_book()`**\
-   Validation renforcée dans `/purchasePlaces`
-   Message d'erreur propre en cas de points insuffisants
-   Mise à jour des tests unitaires, intégration et fonctionnels
-   Ajout d'un test Selenium dédié

Tests maintenant **100 % green**.

------------------------------------------------------------------------

# Issue 3 --- Clubs should not be able to book more than the competition places available (corrigé)

### ❗ Problème

L'application permettait à un club de réserver un nombre de places
supérieur au nombre réellement disponible dans la compétition.

### ✔ Correction

-   Ajout d'une validation stricte dans la fonction métier
    **`can_book()`**
-   Vérification que les `numberOfPlaces` sont suffisants avant toute
    réservation\
-   Uniformisation des messages d'erreur
-   Gestion complète des cas invalides :
    -   compétition inexistante\
    -   club inexistant\
    -   valeur non numérique\
    -   valeur négative ou nulle\
-   Mise à jour de la route `/purchasePlaces` pour refuser toute
    réservation invalide

### 🧪 Tests mis à jour

-   **Unitaires :** couverture à 100% de la fonction `can_book`
-   **Intégration :** tests couvrant les cas insuffisants, valeurs
    invalides, edge cases
-   **Fonctionnels (Selenium) :**
    -   scénario complet de sur-réservation
    -   vérification du message utilisateur
    -   vérification que les points/places restent inchangés

➡️ Résultat : **comportement complètement corrigé**, aucun club ne peut
dépasser les places restantes.

------------------------------------------------------------------------

# Issue 4 --- Limit booking to a maximum of 12 places (corrigé)

### ❗ Problème

Un club pouvait réserver **plus de 12 places**, ce qui est interdit par
la règle métier officielle du projet.

### ✔ Correction

-   Ajout de la constante globale `MAX_PLACES_REQUESTED = 12`
-   Ajout d'un contrôle dans `can_book()` pour refuser toute réservation
    \> 12
-   Mise à jour de `/purchasePlaces` (affichage message + comportement
    cohérent)

### 🧪 Tests mis à jour

-   **Unitaires** : nouveaux tests dédiés à la limite des 12 places
-   **Intégration** : test vérifiant que l'API refuse correctement la
    réservation
-   **Fonctionnels (Selenium)** :
    -   Scénario complet avec helpers (login → booking → erreur
        affichée)
    -   Vérification que les points/places restent inchangés
    -   Vérification du message utilisateur exact

➡️ Résultat : **plus aucun contournement possible**, règle des 12 places
totalement respectée.

------------------------------------------------------------------------

# Issue 5 --- BUG: Booking places in past competitions (corrigé)

### ❗ Problème

Un club pouvait réserver des places dans une compétition déjà passée
(date inférieure à la date du jour).

### ✔ Correction

-   Ajout d'un parsing strict de la date avec `DATE_FORMAT`
-   Ajout d'une comparaison directe avec `CURRENT_DATETIME`
-   Ajout du message métier :\
    **"You cannot book places for a past competition."**
-   Ajout d'une validation dédiée dans `can_book()`

### 🧪 Tests mis à jour

-   **Unitaires :**
    -   Test dédié sur compétition passée\
    -   Vérification que la réservation est refusée et que le message
        exact apparaît\
-   **Intégration :**
    -   Mock de la date via `monkeypatch`\
    -   Vérification que la route `/purchasePlaces` renvoie l'erreur
        correcte\
    -   Vérification que les points/places ne sont pas modifiés\
-   **Fonctionnels (Selenium) :**
    -   Modification de la date dans la fixture globale
        `base_test_data`\
    -   Test end-to-end avec login → booking → erreur affichée\
    -   Validation du message affiché et absence de modifications des
        données

### 🔧 Architecture mise à jour

-   Mise en place d'une **fixture unique `base_test_data`**\
    pour tous les tests (unitaires, intégration, fonctionnels)
-   Nettoyage complet des anciennes fixtures (`sample_data`,
    `patch_server_data`)
-   Séparation claire entre helpers Selenium et fixtures
-   Code plus stable et reproductible
-   Serveur live parfaitement isolé pour Selenium

➡️ **Résultat :** plus aucune réservation n'est possible pour une
compétition passée.\
Tous les tests passent. Couverture backend **100%**.

------------------------------------------------------------------------

---

# 🏗 Architecture du projet

```
gudlft_reservation/
│── server.py
│── clubs.json
│── competitions.json
│── templates/
│     ├── index.html
│     ├── welcome.html
│     └── booking.html
│
tests/
│── unit/
│── integration/
│── functional/
│── performance/
│── conftest.py
│
Pipfile
Pipfile.lock
README.md
```

### 🔎 Architecture des tests

```
tests/
├── unit
│    ├── test_club_lookup.py
│    ├── test_competitions_lookup.py
│    └── test_loading_functions.py
│
├── integration
│    ├── test_show_summary_invalid_email.py
│    ├── test_show_summary_invalid_club.py
│    ├── test_purchase_places_valid.py
│    ├── test_book_valid.py
│    └── test_logout_redirects.py
│
├── functional
│    ├── test_login_valid_email.py
│    ├── test_login_invalid_email.py
│    ├── test_booking_page.py
│    └── test_full_booking_flow.py
│
├── performance
│    ├── locustfile.py
│    └── run_performance.py
```

---

# ⚙️ Installation & Lancement

## 1️⃣ Installation du projet

Le projet utilise **pipenv** :

```bash
pip install pipenv
pipenv install
```

---

## 2️⃣ Activer l’environnement

```bash
pipenv shell
```

---

## 3️⃣ Lancer le serveur

```bash
pipenv run python -m gudlft_reservation.server
```

Serveur accessible sur :

👉 http://127.0.0.1:5000

---

# 🧪 Exécuter les tests

### Tous les tests :

```bash
pytest
```

### Tests fonctionnels Selenium :

```bash
pytest tests/functional -s
```

### Tests de performance :

```bash
python tests/performance/run_performance.py
```

---

# 📊 Couverture du code

```bash
pytest --cov=gudlft_reservation --cov-report=html
```

Couverture actuelle : **100 %**  
(`app.run()` volontairement exclu)

---

------------------------------------------------------------------------

# 🧪 Stratégie de Tests

## 🔹 1. Tests unitaires (`tests/unit/`)

-   Chargement JSON
-   Lookups clubs/compétitions
-   Règles métier (`can_book`)
-   Gestion des erreurs

## 🔹 2. Tests d'intégration (`tests/integration/`)

-   Vérification complète des routes Flask
-   Cas d'erreurs (email inconnu, club inconnu, points insuffisants)
-   Réservations valides et invalides

## 🔹 3. Tests fonctionnels Selenium (`tests/functional/`)

-   Scénarios utilisateurs réels
-   Navigation, réservation, erreurs
-   Attente dynamique (`WebDriverWait`)
-   Helpers pour automatiser le login & booking

## 🔹 4. Tests de performance Locust (`tests/performance/`)

-   Scénarios simulant de nombreuses connexions
-   Serveur isolé lancé automatiquement


------------------------------------------------------------------------

# 🚀 Pour la suite : état d'avancement des issues

## ✅ Issues terminées

-   ✔ **Issue 1 --- ERROR: Entering an unknown email crashes the app**
-   ✔ **Issue 2 --- BUG: Clubs should not be able to use more than their
    points allowed**
-   ✔ **Issue 3 --- BUG: Clubs should not be able to book more than the
    competition places available**
-   ✔ **Issue 4 --- BUG: Clubs shouldn't be able to book more than 12
    places per competition**
-   ✔ **Issue 5 --- BUG: Booking places in past competitions**

## ⏳ Issues restantes à traiter

-   [ ] **Issue 6 --- BUG: Point updates are not reflected**
-   [ ] **Issue 7 --- FEATURE: Implement Points Display Board**

------------------------------------------------------------------------

# 🎯 Conclusion

Ce projet dispose désormais d'une véritable **architecture QA
professionnelle** :

-   Tests robustes\
-   Serveur stable pour les tests\
-   Selenium fiabilisé\
-   Performance testing isolé\
-   Code durci (gestion d'erreurs propre)
