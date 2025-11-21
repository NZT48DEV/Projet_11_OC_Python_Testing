import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

from gudlft_reservation.app import create_app


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

    # Patch de la vraie source de vérité (data_loader)
    import gudlft_reservation.models.data_loader as data_loader

    monkeypatch.setattr(data_loader, "load_clubs", lambda: test_clubs)
    monkeypatch.setattr(data_loader, "load_competitions", lambda: test_comps)

    return test_clubs, test_comps


# ---------------------------------------------------------
#  CLIENT FLASK (tests intégration + unité)
# ---------------------------------------------------------
@pytest.fixture
def client():
    app = create_app()
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
#  SERVEUR WSGI POUR TESTS FUNCTIONNELS
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def live_server(base_test_data):
    app = create_app()  # App FRESHEMENT créée après patch
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
#  SELENIUM CHROME HEADLESS
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
