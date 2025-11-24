import shutil
import threading
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from werkzeug.serving import make_server

from gudlft_reservation.app import create_app


# ---------------------------------------------------------
#  FIXTURE : Isolation des fichiers JSON pour tous les tests
# ---------------------------------------------------------
@pytest.fixture(autouse=True)
def isolate_json_files(tmp_path, monkeypatch):
    """
    Isole les fichiers JSON pour chaque test en copiant les données
    dans un répertoire temporaire et en redirigeant BASE_DIR.
    """
    import gudlft_reservation.models.data_access as data_access

    original_dir = Path(data_access.BASE_DIR)

    # Répertoire temporaire pour ce test
    tmp_data_dir = tmp_path / "data"
    tmp_data_dir.mkdir()

    # Copier les fichiers JSON d’origine
    shutil.copy(original_dir / "clubs.json", tmp_data_dir / "clubs.json")
    shutil.copy(original_dir / "competitions.json", tmp_data_dir / "competitions.json")

    # Patch : on redirige BASE_DIR vers le dossier temporaire
    monkeypatch.setattr(data_access, "BASE_DIR", str(tmp_data_dir))

    yield  # test runs here

    # Pytest gère automatiquement tmp_path -> cleanup automatique


# ---------------------------------------------------------
#  FIXTURE GLOBALE POUR LES DONNÉES DE TEST (intégration/functional)
# ---------------------------------------------------------
@pytest.fixture
def base_test_data(monkeypatch):
    """Fournit un jeu de clubs et compétitions commun à plusieurs tests."""
    test_clubs = [
        {"name": "Test Club", "email": "test@mail.com", "points": 13},
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": 13},
    ]

    test_comps = [
        {"name": "Comp A", "date": "2030-12-31 10:00:00", "numberOfPlaces": 25},
        {"name": "Comp B", "date": "2030-12-31 10:00:00", "numberOfPlaces": 10},
    ]

    # Patch des fonctions load_* pour les tests d’intégration
    import gudlft_reservation.models.data_access as data_access

    monkeypatch.setattr(data_access, "load_clubs", lambda: test_clubs)
    monkeypatch.setattr(data_access, "load_competitions", lambda: test_comps)

    return test_clubs, test_comps


# ---------------------------------------------------------
#  CLIENT FLASK (tests intégration + unité)
# ---------------------------------------------------------
@pytest.fixture
def client():
    """Retourne un client de test Flask configuré pour le projet."""
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


# ---------------------------------------------------------
#  WAIT FUNCTIONNEL
# ---------------------------------------------------------
@pytest.fixture
def wait_for_text():
    """Expose le helper wait_for_text aux tests fonctionnels."""
    from tests.functional.helpers import wait_for_text

    return wait_for_text


# ---------------------------------------------------------
#  SERVEUR WSGI POUR TESTS FUNCTIONNELS
# ---------------------------------------------------------
@pytest.fixture(scope="function")
def live_server(base_test_data):
    """Lance un serveur WSGI local pour les tests fonctionnels Selenium."""
    app = create_app()
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
    """Fournit un navigateur Chrome headless connecté au live_server."""
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
