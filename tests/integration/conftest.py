import pytest

from gudlft_reservation.server import app


@pytest.fixture
def sample_data(monkeypatch):
    """
    Fixture globale pour monkeypatcher les données clubs et competitions
    avec un jeu de données simple et contrôlé.
    """
    clubs = [
        {"name": "Test Club", "email": "test@mail.com", "points": 10},
        {"name": "Other Club", "email": "other@mail.com", "points": 5},
    ]

    competitions = [
        {"name": "Comp A", "date": "2025-12-31", "numberOfPlaces": 5},
        {"name": "Comp B", "date": "2025-11-15", "numberOfPlaces": 2},
    ]

    monkeypatch.setattr("gudlft_reservation.server.clubs", clubs)
    monkeypatch.setattr("gudlft_reservation.server.competitions", competitions)

    # On retourne les données si un test veut les lire
    return clubs, competitions


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client
