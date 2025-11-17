from gudlft_reservation.config import MAX_PLACES_REQUESTED


def test_purchase_places_invalid_club(client, sample_data):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "ClubInexistant", "places": 2},
    )

    page = response.get_data(as_text=True).lower()

    assert "unknown club" in page
    assert "please enter your secretary email" in page


def test_purchase_places_valid(client, sample_data):
    clubs, competitions = sample_data  # conftest.py

    # On s'assure des valeurs de départ
    clubs[0]["points"] = 10
    competitions[0]["numberOfPlaces"] = 5

    # Action : réserver 2 places
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 2},
    )

    assert response.status_code == 200
    page = response.get_data(as_text=True)

    # Le message de succès doit apparaître
    assert "Great-booking complete!" in page

    # Vérification des mises à jour
    assert clubs[0]["points"] == 8  # 10 - 2
    assert competitions[0]["numberOfPlaces"] == 3  # 5 - 2


def test_purchase_places_insufficient_points(client, sample_data):
    clubs, competitions = sample_data  # conftest.py

    # On règle les valeurs nécessaires au scénario
    clubs[0]["points"] = 5
    competitions[0]["numberOfPlaces"] = 20

    # Test : demande trop élevée
    resp = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 10},
    )

    page = resp.data.decode().lower()

    assert resp.status_code == 200
    assert "not enough points" in page

    # Données inchangées
    assert clubs[0]["points"] == 5
    assert competitions[0]["numberOfPlaces"] == 20


def test_purchase_places_not_enough_competition_places(client, sample_data):
    clubs, competitions = sample_data

    clubs[0]["points"] = 50  # assez de points
    competitions[0]["numberOfPlaces"] = 5  # pas assez de places

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 10},
    )

    page = response.get_data(as_text=True).lower()

    assert "not enough places available for this competition." in page
    assert "you requested 10 places but only 5 places remain." in page

    # Données inchangées
    assert competitions[0]["numberOfPlaces"] == 5
    assert clubs[0]["points"] == 50


def test_purchase_places_zero_or_negative(client, sample_data):
    clubs, competitions = sample_data

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


def test_purchase_places_invalid_number(client, sample_data):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": "abc"},
    )

    page = response.get_data(as_text=True).lower()

    assert "invalid number of places" in page


def test_purchase_places_invalid_competition(client, sample_data):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "UnknownCompetition", "club": "Test Club", "places": 2},
    )

    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "unknown competition" in page


def test_purchase_places_exactly_remaining(client, sample_data):
    clubs, competitions = sample_data

    clubs[0]["points"] = 10
    competitions[0]["numberOfPlaces"] = 3

    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 3},
    )

    page = response.get_data(as_text=True).lower()

    assert "great-booking complete" in page

    # Vérifications
    assert clubs[0]["points"] == 7  # 10 - 3
    assert competitions[0]["numberOfPlaces"] == 0


def test_cannot_purchase_more_than_max_places_requested(client, sample_data):
    clubs, competitions = sample_data

    clubs[0]["points"] = 13
    competitions[0]["numberOfPlaces"] = 13
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Comp A", "club": "Test Club", "places": 13},
    )
    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert f"you cannot book more than {MAX_PLACES_REQUESTED} places." in page

    # Données NON modifiées
    assert clubs[0]["points"] == 13
    assert competitions[0]["numberOfPlaces"] == 13

    assert "welcome" in page
