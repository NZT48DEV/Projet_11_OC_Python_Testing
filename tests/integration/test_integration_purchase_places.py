import json
import os

import gudlft_reservation.config as config
import gudlft_reservation.models.data_access as data_access


def test_purchase_places_persists_to_json(client):
    """Vérifie que la réservation persiste bien les données dans les fichiers JSON."""
    clubs_seed = [{"name": "File Club", "email": "file@club.com", "points": 10}]
    competitions_seed = [
        {
            "name": "File Comp",
            "date": "2030-01-01 10:00:00",  # futur pour ne pas être considérée comme passée
            "numberOfPlaces": 5,
        }
    ]

    clubs_path = os.path.join(data_access.BASE_DIR, "clubs.json")
    comps_path = os.path.join(data_access.BASE_DIR, "competitions.json")

    # On écrit ces données dans les fichiers JSON TEMPORAIRES
    # (isolate_json_files a déjà redirigé BASE_DIR vers un tmp dir)
    with open(clubs_path, "w", encoding="utf-8") as f:
        json.dump({"clubs": clubs_seed}, f, indent=4)

    with open(comps_path, "w", encoding="utf-8") as f:
        json.dump({"competitions": competitions_seed}, f, indent=4)

    # --- Act : on effectue une réservation valable (2 places) ---
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "File Comp",
            "club": "File Club",
            "places": 2,
        },
    )

    assert response.status_code == 200

    # --- Assert : on RECHARGE depuis le disque et on vérifie la persistance ---
    clubs_after = data_access.load_clubs()
    comps_after = data_access.load_competitions()

    assert clubs_after[0]["name"] == "File Club"
    assert int(clubs_after[0]["points"]) == 8  # 10 - 2

    assert comps_after[0]["name"] == "File Comp"
    assert int(comps_after[0]["numberOfPlaces"]) == 3  # 5 - 2


def test_purchase_places_invalid_club(client, base_test_data):
    """Vérifie qu'un club inexistant est refusé avec le bon message d'erreur."""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "ClubInexistant", "places": 2},
    )

    page = response.get_data(as_text=True).lower()

    assert "unknown club" in page
    assert "please enter your secretary email" in page


def test_purchase_places_valid(client, base_test_data):
    """Vérifie qu'une réservation valide met à jour points et places correctement."""
    clubs, competitions = base_test_data  # conftest.py

    clubs[0]["points"] = 10
    competitions[0]["numberOfPlaces"] = 5

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 2},
    )

    assert response.status_code == 200
    page = response.get_data(as_text=True)

    assert "Great-booking complete!" in page
    assert clubs[0]["points"] == 8  # 10 - 2
    assert competitions[0]["numberOfPlaces"] == 3  # 5 - 2


def test_purchase_places_insufficient_points(client, base_test_data):
    """Vérifie qu'une réservation échoue si le club n'a pas assez de points."""
    clubs, competitions = base_test_data  # conftest.py

    clubs[0]["points"] = 5
    competitions[0]["numberOfPlaces"] = 20

    resp = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 10},
    )

    page = resp.data.decode().lower()

    assert resp.status_code == 200
    assert "not enough points" in page
    assert clubs[0]["points"] == 5
    assert competitions[0]["numberOfPlaces"] == 20


def test_purchase_places_not_enough_competition_places(client, base_test_data):
    """Vérifie qu'on ne peut pas réserver plus de places que celles restantes."""
    clubs, competitions = base_test_data

    clubs[0]["points"] = 50  # assez de points
    competitions[0]["numberOfPlaces"] = 5  # pas assez de places

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 10},
    )

    page = response.get_data(as_text=True).lower()

    assert "not enough places available for this competition." in page
    assert "you requested 10 places but only 5 places remain." in page
    assert competitions[0]["numberOfPlaces"] == 5
    assert clubs[0]["points"] == 50


def test_purchase_places_zero_or_negative(client, base_test_data):
    """Vérifie que 0 ou un nombre négatif de places sont refusés."""
    clubs, competitions = base_test_data

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 0},
    )
    page = response.get_data(as_text=True).lower()
    assert "you must book at least one place" in page

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": -5},
    )
    page = response.get_data(as_text=True).lower()
    assert "you must book at least one place" in page


def test_purchase_places_invalid_number(client, base_test_data):
    """Vérifie que les valeurs non numériques sont rejetées proprement."""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": "abc"},
    )

    page = response.get_data(as_text=True).lower()

    assert "invalid number of places" in page


def test_purchase_places_invalid_competition(client, base_test_data):
    """Vérifie qu'une compétition inconnue renvoie le bon message d'erreur."""
    response = client.post(
        "/purchasePlaces",
        data={"competition": "UnknownCompetition", "club": "Test Club", "places": 2},
    )

    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "unknown competition" in page


def test_purchase_places_exactly_remaining(client, base_test_data):
    """Vérifie qu'on peut réserver exactement le nombre de places restantes."""
    clubs, competitions = base_test_data

    clubs[0]["points"] = 10
    competitions[0]["numberOfPlaces"] = 3

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 3},
    )

    page = response.get_data(as_text=True).lower()

    assert "great-booking complete" in page
    assert clubs[0]["points"] == 7  # 10 - 3
    assert competitions[0]["numberOfPlaces"] == 0


def test_purchase_more_than_max_places_requested(client, base_test_data):
    """Vérifie qu'on ne peut pas dépasser la limite MAX_PLACES_REQUESTED."""
    clubs, competitions = base_test_data

    clubs[0]["points"] = 13
    competitions[0]["numberOfPlaces"] = 13

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 13},
    )
    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert f"you cannot book more than {config.MAX_PLACES_REQUESTED} places." in page
    assert clubs[0]["points"] == 13
    assert competitions[0]["numberOfPlaces"] == 13
    assert "welcome" in page


def test_purchase_places_for_past_competition(client, base_test_data, monkeypatch):
    """Vérifie qu'on ne peut pas réserver pour une compétition déjà passée."""
    clubs, competitions = base_test_data

    competitions[0]["date"] = "2000-01-01 10:00:00"

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 4},
    )

    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "you cannot book places for a past competition."
    assert clubs[0]["points"] == 13
    assert competitions[0]["numberOfPlaces"] == 25
    assert "welcome" in page


def test_purchase_places_exceeds_total_limit(client, base_test_data, monkeypatch):
    """Vérifie qu'un club ne peut pas dépasser la limite totale de places réservées pour une compétition."""
    clubs, competitions = base_test_data

    clubs[0]["points"] = 50
    competitions[0]["numberOfPlaces"] = 30

    competitions[0]["bookings"] = {"Test Club": 12}

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 1},
    )

    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "already booked 12 places" in page
    assert str(config.MAX_PLACES_REQUESTED) in page

    assert clubs[0]["points"] == 50
    assert competitions[0]["numberOfPlaces"] == 30
    assert competitions[0]["bookings"]["Test Club"] == 12
