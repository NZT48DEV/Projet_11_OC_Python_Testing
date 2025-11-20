import gudlft_reservation.views.main as main_views


def test_points_board_integration(client, monkeypatch):
    test_clubs = [
        {"name": "Alpha", "email": "alpha@mail.com", "points": 33},
        {"name": "Beta", "email": "beta@mail.com", "points": 5},
    ]

    monkeypatch.setattr(main_views, "load_clubs", lambda: test_clubs)

    resp = client.get("/pointsBoard")
    html = resp.get_data(as_text=True)

    assert "Alpha" in html
    assert "Beta" in html
