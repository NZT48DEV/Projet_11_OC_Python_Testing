import threading
import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

import gudlft_reservation.server as app_server
from gudlft_reservation.server import app, loadClubs, loadCompetitions


@pytest.fixture
def wait_for_text_in_page():
    """Retourne une fonction utilitaire utilisable dans tous les tests."""

    def _wait(driver, text, timeout=10):
        expected = text.lower()
        WebDriverWait(driver, timeout).until(
            lambda d: expected in d.page_source.lower()
        )

    return _wait


@pytest.fixture(scope="function")
def live_server():
    """Lance un serveur Flask réel sur 127.0.0.1:5000 pour chaque test fonctionnel."""

    # 🔁 Très important : on reset les données globales AVANT de lancer le serveur
    app_server.clubs = loadClubs()
    app_server.competitions = loadCompetitions()

    server = make_server("127.0.0.1", 5000, app)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # petit délai de sécurité pour être sûr que le serveur écoute
    time.sleep(0.2)

    try:
        yield
    finally:
        server.shutdown()
        thread.join()


@pytest.fixture
def browser(live_server):
    """Lance Chrome en mode headless et garantit que le serveur est démarré."""

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
