import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

import gudlft_reservation.views.booking as booking_views
import gudlft_reservation.views.main as main_views
from gudlft_reservation.app import app

# ---------------------------------------------------------
#  FIXTURE GLOBALE POUR LES DONNÉES DE TEST
# ---------------------------------------------------------


@pytest.fixture
def base_test_data(monkeypatch):

    test_clubs = [
        {"name": "Test Club", "email": "test@mail.com", "points": 13},
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
    ]

    test_comps = [
        {"name": "Comp A", "date": "2030-12-31 10:00:00", "numberOfPlaces": 25},
        {"name": "Comp B", "date": "2030-12-31 10:00:00", "numberOfPlaces": 10},
    ]

    # Patch des getters used by all views
    monkeypatch.setattr(main_views, "get_clubs", lambda: test_clubs)
    monkeypatch.setattr(main_views, "get_competitions", lambda: test_comps)

    monkeypatch.setattr(booking_views, "get_clubs", lambda: test_clubs)
    monkeypatch.setattr(booking_views, "get_competitions", lambda: test_comps)

    return test_clubs, test_comps


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
