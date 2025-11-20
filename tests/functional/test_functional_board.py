import gudlft_reservation.views.main as main_views


def test_points_board_functional(browser, base_test_data, monkeypatch):
    test_clubs, _ = base_test_data

    monkeypatch.setattr(main_views, "load_clubs", lambda: test_clubs)

    browser.get("http://127.0.0.1:5000/pointsBoard")

    page = browser.page_source

    assert "Test Club" in page
    assert "Simply Lift" in page
    assert "13" in page
