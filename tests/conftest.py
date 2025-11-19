import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

import gudlft_reservation.server as app_server
from gudlft_reservation.server import app


# ---------------------------------------------------------
#  FIXTURE GLOBALE POUR TOUTES LES DONNÉES
# ---------------------------------------------------------
@pytest.fixture(autouse=True)
def base_test_data(monkeypatch):
    test_clubs = [
        {"name": "Test Club", "email": "test@mail.com", "points": 13},
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
    ]

    test_competitions = [
        {"name": "Comp A", "date": "2030-12-31 10:00:00", "numberOfPlaces": 25},
        {
            "name": "Spring Festival",
            "date": "2030-12-31 10:00:00",
            "numberOfPlaces": 25,
        },
        {"name": "Fall Classic", "date": "2030-12-31 10:00:00", "numberOfPlaces": 12},
    ]

    # Patch des données globales en mémoire
    monkeypatch.setattr(app_server, "clubs", test_clubs)
    monkeypatch.setattr(app_server, "competitions", test_competitions)

    # 🔥 Patch des fonctions loadClubs / loadCompetitions
    monkeypatch.setattr(app_server, "loadClubs", lambda: test_clubs)
    monkeypatch.setattr(app_server, "loadCompetitions", lambda: test_competitions)

    return test_clubs, test_competitions


# ---------------------------------------------------------
#  CLIENT FLASK
# ---------------------------------------------------------
@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


# ---------------------------------------------------------
#  WAIT FUNCTIONNEL
# ---------------------------------------------------------
@pytest.fixture
def wait_for_text():
    from tests.functional.helpers import wait_for_text

    return wait_for_text


# ---------------------------------------------------------
#  SERVEUR POUR TESTS FUNCTIONNELS
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def live_server(base_test_data):
    server = make_server("127.0.0.1", 5000, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    time.sleep(0.2)
    try:
        yield
    finally:
        server.shutdown()
        thread.join()


# ---------------------------------------------------------
#  BROWSER SELENIUM
# ---------------------------------------------------------
@pytest.fixture
def browser(live_server):
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )

    try:
        yield driver
    finally:
        driver.quit()
