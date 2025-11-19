from selenium.webdriver.common.by import By


def test_points_board_functional(browser, live_server):
    # Accès à la page publique
    browser.get("http://127.0.0.1:5000/pointsBoard")

    # Vérifie que la table existe
    table = browser.find_element(By.TAG_NAME, "table")
    assert table is not None

    page = browser.page_source

    # Ces clubs viennent de base_test_data dans conftest.py
    assert "Test Club" in page
    assert "Simply Lift" in page

    # Les points aussi (13 dans les fixtures)
    assert "13" in page
