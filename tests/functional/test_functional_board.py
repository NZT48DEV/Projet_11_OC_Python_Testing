import gudlft_reservation.models.data_access as data_access


def test_points_board_functional(browser, base_test_data, monkeypatch):
    """Vérifie que le tableau des points affiche bien tous les clubs et leurs valeurs."""
    test_clubs, _ = base_test_data

    monkeypatch.setattr(data_access, "load_clubs", lambda: test_clubs)

    browser.get("http://127.0.0.1:5000/pointsBoard")
    page = browser.page_source

    assert "Test Club" in page
    assert "Simply Lift" in page
    assert "13" in page
