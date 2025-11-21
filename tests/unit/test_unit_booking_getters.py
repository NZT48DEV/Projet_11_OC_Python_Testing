import gudlft_reservation.models.data_loader as data_loader
import gudlft_reservation.views.booking as booking_views


def test_get_clubs_calls_load_clubs(monkeypatch):
    called = {"value": False}

    def fake_load():
        called["value"] = True
        return [{"name": "Unit Club", "email": "a@b.c", "points": "13"}]

    monkeypatch.setattr(data_loader, "load_clubs", fake_load)

    result = booking_views.get_clubs()

    assert called["value"] is True
    assert result[0]["points"] == 13


def test_get_competitions_calls_load_competitions(monkeypatch):
    called = {"value": False}

    def fake_load():
        called["value"] = True
        return [
            {"name": "Comp X", "date": "2030-01-01 10:00:00", "numberOfPlaces": "50"}
        ]

    monkeypatch.setattr(data_loader, "load_competitions", fake_load)

    result = booking_views.get_competitions()

    assert called["value"] is True
    assert result[0]["numberOfPlaces"] == 50
