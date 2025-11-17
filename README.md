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

# Issue 3 — Clubs should not be able to book more than the competition places available (corrigé)

### ❗ Problème  
L’application permettait à un club de réserver un nombre de places supérieur au nombre réellement disponible dans la compétition.

### ✔ Correction  
- Ajout d’une validation stricte dans la fonction métier **`can_book()`**
- Vérification que les `numberOfPlaces` sont suffisants avant toute réservation  
- Uniformisation des messages d’erreur
- Gestion complète des cas invalides :
  - compétition inexistante  
  - club inexistant  
  - valeur non numérique  
  - valeur négative ou nulle  
- Mise à jour de la route `/purchasePlaces` pour refuser toute réservation invalide  

### 🧪 Tests mis à jour
- **Unitaires :** couverture à 100% de la fonction `can_book`
- **Intégration :** tests couvrant les cas insuffisants, valeurs invalides, edge cases
- **Fonctionnels (Selenium) :**
  - scénario complet de sur-réservation
  - vérification du message utilisateur
  - vérification que les points/places restent inchangés

➡️ Résultat : **comportement complètement corrigé**, aucun club ne peut dépasser les places restantes.

---

# Issue 4 — Limit booking to a maximum of 12 places (corrigé)

### ❗ Problème  
Un club pouvait réserver **plus de 12 places**, ce qui est interdit par la règle métier officielle du projet.

### ✔ Correction  
- Ajout de la constante globale `MAX_PLACES_REQUESTED = 12`
- Ajout d’un contrôle dans `can_book()` pour refuser toute réservation > 12
- Mise à jour de `/purchasePlaces` (affichage message + comportement cohérent)

### 🧪 Tests mis à jour
- **Unitaires** : nouveaux tests dédiés à la limite des 12 places
- **Intégration** : test vérifiant que l’API refuse correctement la réservation
- **Fonctionnels (Selenium)** :
  - Scénario complet avec helpers (login → booking → erreur affichée)
  - Vérification que les points/places restent inchangés
  - Vérification du message utilisateur exact

➡️ Résultat : **plus aucun contournement possible**, règle des 12 places totalement respectée.

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
- Helpers pour automatiser le login & booking

## 🔹 4. Tests de performance Locust (`tests/performance/`)
- Scénarios simulant de nombreuses connexions
- Serveur isolé lancé automatiquement

---

# 🚀 Pour la suite : état d’avancement des issues

Le projet comporte **7 issues officielles** (source : dépôt OpenClassrooms).  
Grâce à toute l’infrastructure de test mise en place, la progression sera fluide et sécurisée.

## ✅ Issues terminées
- ✔ **Issue 1 — ERROR: Entering an unknown email crashes the app**
- ✔ **Issue 2 — BUG: Clubs should not be able to use more than their points allowed**
- ✔ **Issue 3 — BUG: Clubs should not be able to book more than the competition places available**
- ✔ **Issue 4 — BUG: Clubs shouldn't be able to book more than 12 places per competition**

## ⏳ Issues restantes à traiter
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
