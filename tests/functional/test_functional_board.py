import gudlft_reservation.models.data_loader as data_loader


def test_points_board_functional(browser, base_test_data, monkeypatch):
    test_clubs, _ = base_test_data

    monkeypatch.setattr(data_loader, "load_clubs", lambda: test_clubs)

    browser.get("http://127.0.0.1:5000/pointsBoard")
    page = browser.page_source

    assert "Test Club" in page
    assert "Simply Lift" in page
    assert "13" in page
