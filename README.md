# 🏋️‍♂️ GudLFT — Projet OpenClassrooms : Tests & Qualité logicielle

![Python](https://img.shields.io/badge/Python-3.13-blue)
![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey)
![Pytest](https://img.shields.io/badge/tests-pytest-green)
![Coverage](https://img.shields.io/badge/Coverage-100%25-brightgreen)
![Locust](https://img.shields.io/badge/Performance-Locust-orange)
![CI](https://img.shields.io/badge/CI-GitHub%20Actions-inactive)

Ce dépôt contient l’application **GudLFT Reservation** ainsi que l’ensemble des tests permettant d’assurer une qualité applicative élevée.

---

# 📌 Contexte du projet

Dans le cadre du parcours **Développeur d'application Python**, ce projet consiste à :

- Identifier et corriger des bugs (7 issues au total)
- Renforcer l’application avec des tests **unitaires, intégration, fonctionnels et performance**
- Structurer un pipeline QA complet
- Préparer le terrain pour traiter les issues suivantes de manière fiable

Ce README décrit les issues corrigées, ainsi que l’infrastructure mise en place pour la suite.

---

# Issue 1 — Crash sur email invalide (corrigé)

### ❗ Problème
La route `/showSummary` plantait lorsqu’un utilisateur saisissait un email inconnu.

### ✔ Correction
- Remplacement du `[0]` par `next(..., None)` pour éviter l’IndexError
- Gestion propre des erreurs
- Ajout d’un message utilisateur via `flash()`
- Support GET/POST pour `/showSummary`
- Tests robustes sur 3 niveaux (unitaire, intégration, fonctionnel)

---

# Issue 2 — Empêcher la réservation si le club n’a pas assez de points (corrigé)

### ❗ Problème
Un club pouvait réserver plus de places que ses points disponibles.

### ✔ Correction
- Ajout de la fonction **`can_book()`**  
- Validation renforcée dans `/purchasePlaces`
- Message d’erreur propre en cas de points insuffisants
- Mise à jour des tests unitaires, intégration et fonctionnels
- Ajout d’un test Selenium dédié

Tests maintenant **100 % green**.

---

# 🧪 Stratégie de Tests

## 🔹 1. Tests unitaires (`tests/unit/`)
- Chargement JSON
- Lookups clubs/compétitions
- Règles métier (`can_book`)
- Gestion des erreurs

## 🔹 2. Tests d’intégration (`tests/integration/`)
- Vérification complète des routes Flask
- Cas d’erreurs (email inconnu, club inconnu, points insuffisants)
- Réservations valides et invalides

## 🔹 3. Tests fonctionnels Selenium (`tests/functional/`)
- Scénarios utilisateurs réels
- Navigation, réservation, erreurs
- Attente dynamique (`WebDriverWait`)
- Fonction commune : `wait_for_text_in_page`

## 🔹 4. Tests de performance Locust (`tests/performance/`)
- Scénarios simulant de nombreuses connexions
- Serveur isolé lancé automatiquement

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

---

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

## 1️⃣ Installer l’environnement
```bash
pip install pipenv
pipenv install
```

## 2️⃣ Activer l’environnement
```bash
pipenv shell
```

## 3️⃣ Lancer le serveur
```bash
pipenv run python -m gudlft_reservation.server
```

Serveur local :  
👉 http://127.0.0.1:5000

---

# 🧪 Lancer les tests

### Tous les tests
```bash
pytest
```

### Fonctionnels (Selenium)
```bash
pytest tests/functional -s
```

### Tests performance
```bash
python tests/performance/run_performance.py
```

### Couverture
```bash
pytest --cov=gudlft_reservation --cov-report=html
```

👉 Couverture actuelle : **100 %**

---

# 🚀 Pour la suite : état d’avancement des issues

Le projet comporte **7 issues officielles** (source : dépôt OpenClassrooms).  
Grâce à toute l’infrastructure de test mise en place, la progression sera fluide et sécurisée.

## ✅ Issues terminées
- ✔ **Issue 1 — ERROR: Entering an unknown email crashes the app**  
  *(corrigée et entièrement testée : unitaires, intégration, fonctionnels)*  
- ✔ **Issue 2 — BUG: Clubs should not be able to use more than their points allowed**  
  *(validation, refactor, tests complets et couverture totale)*

## ⏳ Issues restantes à traiter
- ☐ **Issue 3 — BUG: Clubs should not be able to book more than the competition places available**  
- ☐ **Issue 4 — BUG: Clubs shouldn't be able to book more than 12 places per competition**  
- ☐ **Issue 5 — BUG: Booking places in past competitions**  
- ☐ **Issue 6 — BUG: Point updates are not reflected**  
- ☐ **Issue 7 — FEATURE: Implement Points Display Board**

---

# 🎯 Conclusion

Ce projet dispose désormais d’une véritable **architecture QA professionnelle** :

- Tests robustes  
- Serveur stable pour les tests  
- Selenium fiabilisé  
- Performance testing isolé  
- Code durci (gestion d’erreurs propre)
