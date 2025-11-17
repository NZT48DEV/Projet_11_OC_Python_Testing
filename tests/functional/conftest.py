import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

# Import serveur + app Flask
import gudlft_reservation.server as app_server
from gudlft_reservation.server import app  # <- Import manquant ajouté ici

# -------------------------------------------------------------------
#  Monkeypatch global pour les tests fonctionnels
# -------------------------------------------------------------------


@pytest.fixture
def patch_server_data(monkeypatch):
    """
    Patch the global Flask server data BEFORE the live server starts.
    Ensures that functional tests always work with controlled fixtures.
    """
    test_clubs = [
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
        {"name": "Iron Temple", "email": "admin@iron.com", "points": 4},
    ]

    test_competitions = [
        {"name": "Spring Festival", "date": "2025-12-31", "numberOfPlaces": 25},
        {"name": "Fall Classic", "date": "2025-11-20", "numberOfPlaces": 12},
    ]

    monkeypatch.setattr(app_server, "clubs", test_clubs)
    monkeypatch.setattr(app_server, "competitions", test_competitions)

    return test_clubs, test_competitions


# -------------------------------------------------------------------
#  Helper Selenium
# -------------------------------------------------------------------


@pytest.fixture
def wait_for_text_in_page():
    """Return a helper function used by all functional tests."""

    def _wait(driver, text, timeout=10):
        expected = text.lower()
        WebDriverWait(driver, timeout).until(
            lambda d: expected in d.page_source.lower()
        )

    return _wait


# -------------------------------------------------------------------
#  Serveur Flask réel pour tests E2E
# -------------------------------------------------------------------


@pytest.fixture(scope="function")
def live_server(patch_server_data):
    """Start a real Flask server with patched data."""

    # patch_server_data already injected controlled data

    server = make_server("127.0.0.1", 5000, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # ensure server is listening
    time.sleep(0.2)

    try:
        yield
    finally:
        server.shutdown()
        thread.join()


# -------------------------------------------------------------------
#  Navigateur Chrome pour tests Selenium
# -------------------------------------------------------------------


@pytest.fixture
def browser(live_server):
    """Launch headless Chrome and ensure the server is running."""

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
