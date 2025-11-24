import gudlft_reservation.models.data_access as data_access


def test_points_board_integration(client, monkeypatch):
    """Vérifie que la route /pointsBoard affiche correctement les clubs fournis par load_clubs()."""
    test_clubs = [
        {"name": "Alpha", "email": "alpha@mail.com", "points": 33},
        {"name": "Beta", "email": "beta@mail.com", "points": 5},
    ]

    monkeypatch.setattr(data_access, "load_clubs", lambda: test_clubs)

    resp = client.get("/pointsBoard")
    html = resp.get_data(as_text=True)

    assert "Alpha" in html
    assert "Beta" in html
