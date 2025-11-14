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

- Identifier et corriger des bugs (7 issues au total, l’issue 1 est terminée)
- Renforcer l’application avec des tests **unitaires, intégration, fonctionnels et performance**
- Structurer un pipeline QA complet
- Préparer le terrain pour traiter les issues suivantes de manière fiable

Ce README décrit le travail effectué pour l’issue 1 et pose les fondations pour les prochaines.

---

# 🐞 Issue 1 — Crash sur email invalide

### ❗ Problème

La route `/showSummary` plantait lorsqu’un utilisateur saisissait un email inconnu.

### ✔ Correction

- Remplacement du `[0]` par `next(..., None)`
- Gestion des erreurs propres
- Message utilisateur avec **flash()**
- Retour cohérent vers `index.html`
- Support GET / POST pour `/showSummary`
- Tests multi-niveaux garantissant l'absence de régression

---

# 🧪 Stratégie de Tests (complète)

Même si seule l’issue 1 a été corrigée, nous avons mis en place **tous les tests** pour sécuriser le code existant et préparer les futures issues.

## 1. Tests unitaires

📁 `tests/unit/`

- Vérification du chargement JSON
- Lookup de clubs et compétitions
- Fonctions utilitaires

## 2. Tests d’intégration

📁 `tests/integration/`

- Routes Flask
- Gestion d’erreurs
- Tests complets des réponses HTTP

## 3. Tests fonctionnels (Selenium)

📁 `tests/functional/`

- Simulation d’un utilisateur réel
- Navigation et réservation
- Attente dynamique (`WebDriverWait`)
- Fonction utilitaire mutualisée : `wait_for_text_in_page()`

## 4. Tests de performance (Locust)

📁 `tests/performance/`

- Simulation de charge
- Script dédié lançant automatiquement un serveur pour éviter tout conflit

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

# 🚀 Pour la suite : issues restantes

Seule **l’issue 1** est corrigée, mais **toute l’infrastructure de test est prête** pour traiter les 6 autres :

- Toutes les routes sont testées
- Le navigateur headless est stable
- Les helpers Selenium sont centralisés
- L’architecture de test est complète
- Le serveur est isolé pour performance & functional testing


---

# 🎯 Conclusion

Ce projet dispose désormais d’une véritable **architecture QA professionnelle** :

- Tests robustes  
- Serveur stable pour les tests  
- Selenium fiabilisé  
- Performance testing isolé  
- Code durci (gestion d’erreurs propre)