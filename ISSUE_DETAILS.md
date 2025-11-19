# Issue 1 — Crash sur email invalide (corrigé)

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

# Issue 2 — Empêcher la réservation si le club n'a pas assez de points (corrigé)

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

# Issue 3 — Clubs should not be able to book more than the competition places available (corrigé)

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

# Issue 4 — Limit booking to a maximum of 12 places (corrigé)

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

# Issue 5 — BUG: Booking places in past competitions (corrigé)

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

# Issue 6 — BUG: Point updates are not reflected (corrigé)

### ❗ Problème

Après une réservation, les points du club ne semblaient pas être mis à jour, laissant penser que la déduction des points ne fonctionnait pas correctement.

### ✔ Correction

En réalité, la logique métier était déjà correctement implémentée :

- Déduction des points du club dans `/purchasePlaces`
- Mise à jour du nombre de places disponibles
- Comportement aligné sur les règles métier
- Ajout d’un test unitaire dédié pour verrouiller la règle

```python
# Apply booking
places_required = int(places_raw)
club["points"] = int(club["points"]) - places_required
competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required
```

### 🧪 Tests mis à jour

- **Unitaires :**
  - `test_points_are_deducted_correctly` ajouté
  - Vérification stricte du calcul des points restants
  - Cas invalides autour des points et conversions couvertes

- **Intégration :**
  - Vérification que `/purchasePlaces` modifie bien les points et les places

- **Fonctionnels (Selenium) :**
  - Scénario complet de réservation valide
  - Vérification que les points affichés correspondent bien au nouveau solde

### 🔧 Architecture mise à jour

- Consolidation de toutes les validations dans `can_book()`
- Ajout d’un test dédié pour éviter toute régression future

➡️ **Résultat :** la mise à jour des points est fonctionnelle, validée et désormais protégée par des tests.