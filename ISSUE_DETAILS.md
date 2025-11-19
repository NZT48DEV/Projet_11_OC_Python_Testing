# ISSUE DETAILS — Güdlft Project

## Issue 1 — Crash sur email invalide (corrigé)

### ❗ Problème

La route `/showSummary` plantait lorsqu'un utilisateur saisissait un
email inconnu.

### ✔ Correction

-   Remplacement du `[0]` par `next(..., None)` pour éviter l'IndexError
-   Gestion propre des erreurs
-   Utilisation de `flash()` pour informer l'utilisateur
-   Support GET/POST pour `/showSummary`
-   Tests unitaires, intégration et fonctionnels complets

------------------------------------------------------------------------

## Issue 2 — Empêcher la réservation si le club n'a pas assez de points (corrigé)

### ❗ Problème

Un club pouvait réserver plus de places que ses points disponibles.

### ✔ Correction

-   Ajout de la fonction `can_book()`
-   Validation stricte dans `/purchasePlaces`
-   Messages d'erreur clairs pour l'utilisateur
-   Tests multi-niveaux mis à jour

------------------------------------------------------------------------

## Issue 3 — Booking au-delà des places de compétition (corrigé)

### ❗ Problème

Un club pouvait réserver plus de places que celles réellement
disponibles.

### ✔ Correction

-   Validation stricte dans `can_book()`
-   Vérification des places restantes
-   Gestion des cas invalides (club inconnu, compétition inexistante,
    valeurs invalides)
-   Mise à jour des routes et messages

### 🧪 Tests

-   Unitaires : couverture complète
-   Intégration : sur-réservation, cas invalides
-   Fonctionnels : test complet Selenium

------------------------------------------------------------------------

## Issue 4 — Limite de 12 places maximum (corrigé)

### ❗ Problème

Un club pouvait réserver plus de 12 places.

### ✔ Correction

-   Ajout de `MAX_PLACES_REQUESTED = 12`
-   Contrôle intégré à `can_book()`
-   Mise à jour des tests

### 🧪 Tests

-   Unitaires
-   Intégration
-   Fonctionnels Selenium

------------------------------------------------------------------------

## Issue 5 — Réservation dans une compétition passée (corrigé)

### ❗ Problème

Les réservations étaient possibles pour des compétitions déjà passées.

### ✔ Correction

-   Parsing strict des dates
-   Comparaison avec la date actuelle
-   Message utilisateur dédié
-   Validation dans `can_book()`

### 🧪 Tests

-   Unitaires (compétition passée)
-   Intégration (mock de date)
-   Fonctionnels (scénario complet Selenium)

------------------------------------------------------------------------

## Issue 6 — Mise à jour des points non reflétée (corrigé)

### ❗ Problème

Les points semblaient ne pas se mettre à jour malgré une réservation
valide.

### ✔ Correction

-   La logique était correcte, mais non testée
-   Ajout d'un test unitaire dédié
-   Vérification de la mise à jour réelle dans `/purchasePlaces`

### 🧪 Tests

-   Unitaires : déduction des points
-   Intégration : cohérence points et places
-   Fonctionnels : test complet Selenium

------------------------------------------------------------------------

## Issue 7 — FEATURE: Public Points Display Board (implémenté)

### ⭐ Objectif

Créer un tableau public affichant les points de chaque club, accessible
sans login, conforme aux exigences de la phase 2 : - lecture seule -
accessible publiquement - temps de chargement \< 5 sec

### ✔ Implémentation

-   Nouvelle route `/pointsBoard`
-   Nouveau template `points_board.html`
-   Données chargées via `loadClubs()`
-   Affichage responsive propre

``` python
@app.route('/pointsBoard')
def points_board():
    clubs = loadClubs()
    return render_template('points_board.html', clubs=clubs)
```

------------------------------------------------------------------------

### 🧪 Tests

#### 🔹 Unitaires

-   Mock de `loadClubs()` et `render_template()`
-   Vérification du rendu correct

#### 🔹 Intégration

-   Appel réel `client.get("/pointsBoard")`
-   Données injectées via `base_test_data`

#### 🔹 Fonctionnels (Selenium)

-   Chargement réel dans un navigateur
-   Vérification de la table et du contenu affiché

#### 🔹 Performance (Locust)

-   GET `/pointsBoard` \< 5 sec (mesuré : 6--12 ms)
-   POST `/showSummary` \< 2 sec (mesuré : 6--13 ms)
-   Aucun échec Locust
-   Script automatisé avec variables d'environnement

------------------------------------------------------------------------

### 🎉 Résultat final

La fonctionnalité est : 
- stable
- testée (4 niveaux)
- performante
- conforme à 100 % aux exigences du projet
