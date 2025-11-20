# 🏋️‍♂️ GudLFT — Projet OpenClassrooms : Tests & Qualité logicielle

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

---

# 🏗 Architecture du projet

```
gudlft_reservation/
    │── models/
    │     └── data_loader.py
    │── services/
    │     └── booking_rules.py
    │── static/
    │     └── style/
    │           └── points_board.css 
    │── templates/
    │     ├── booking.html
    │     ├── index.html
    │     ├── points_board.html
    │     └── welcome.html
    │── views/
    │     ├── booking.py
    │     └── main.py
    │── app.py
    │── clubs.json
    │── competitions.json
    │── config.py
    │── server.py
   tests/
    │── conftest.py
    │── functional/
    │── integration/
    │── performance/
    └── unit/
.flake8
.gitignore
.pre-commit-config.yaml
ISSUE_DETAILS.md
PERFORMANCE_DETAILS.md
Pipfile
Pipfile.lock
pyproject.toml
pytest.ini
README.md
run_performance_tests.bat
```

### 🔎 Architecture des tests

```
tests/
├── unit
│    ├── test_unit_booking_rules.py
│    ├── test_unit_booking_getters.py
│    ├── test_unit_club_lookup.py
│    ├── test_unit_competitions_lookup.py
│    ├── test_unit_board.py
│    └── test_unit_loading_functions.py
│
├── integration
│    ├── test_integration_show_summary_email.py
│    ├── test_integration_show_summary_club.py
│    ├── test_integration_purchase_places.py
│    ├── test_integration_book_valid.py
│    ├── test_integration_index_page_loads.py
│    ├── test_integration_board.py
│    └── test_integration_logout_redirects.py
│
├── functional
│    ├── helpers.py
│    ├── test_functional_booking.py
│    ├── test_functional_board.py
│    └── test_functional_login_email.py
│
├── performance
│    ├── locustfile.py
│    └── run_performance_tests.py
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

### Tests de performance (à exécuter depuis CMD / PowerShell uniquement)

⚠️ **Important :**  
Les tests de performance Locust **ne doivent pas être lancés depuis Git Bash (MINGW64)** car cela casse les chemins Windows et perturbe `subprocess` ainsi que WebDriver.

➡️ **Utilisez impérativement :**
- **CMD.exe**  
ou
- **PowerShell**

```bash
python tests/performance/run_performance_tests.py
```

# 📊 Couverture du code

```bash
pytest --cov=gudlft_reservation --cov-report=html
```

Couverture actuelle : **100 %**  
(`app.run()` volontairement exclu)

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

-   ✔ **Issue 1 — ERROR: Entering an unknown email crashes the app**
-   ✔ **Issue 2 — BUG: Clubs should not be able to use more than their
    points allowed**
-   ✔ **Issue 3 — BUG: Clubs should not be able to book more than the
    competition places available**
-   ✔ **Issue 4 — BUG: Clubs shouldn't be able to book more than 12
    places per competition**
-   ✔ **Issue 5 — BUG: Booking places in past competitions**
-   ✔ **Issue 6 — BUG: Point updates are not reflected**
-   ✔ **Issue 7 — FEATURE: Implement Points Display Board**

## ⏳ Issues restantes à traiter

-   Aucunes

------------------------------------------------------------------------

# 📄 Issues

Voir les détails complets des issues : [ISSUES_DETAILS.md](ISSUES_DETAILS.md)

------------------------------------------------------------------------

# ⚡ Performances

Voir les détails du rapport des tests de performances : [PERFORMANCE_DETAILS.md](PERFORMANCE_DETAILS.md)

# 🎯 Conclusion

Ce projet dispose désormais d'une véritable **architecture QA
professionnelle** :

-   Tests robustes
-   Serveur stable pour les tests
-   Selenium fiabilisé
-   Performance testing isolé
-   Code durci (gestion d'erreurs propre)
