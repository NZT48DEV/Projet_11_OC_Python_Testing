"""
Helpers Selenium pour les tests fonctionnels :
- Attentes explicites
- Connexion utilisateur
- Navigation dans l'interface
- Actions sur les formulaires
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# -----------------------------------------------------------
#  WAIT HELPERS
# -----------------------------------------------------------


def wait_for_text(driver, text, timeout=3):
    """Attend qu'un texte spécifique apparaisse dans la page."""
    expected = text.lower()
    WebDriverWait(driver, timeout).until(lambda d: expected in d.page_source.lower())


# -----------------------------------------------------------
#  LOGIN HELPERS
# -----------------------------------------------------------


def login(driver, wait, email="john@simplylift.co"):
    """Effectue une connexion avec l'email fourni."""
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.TAG_NAME, "button").click()

    wait(driver, f"welcome, {email.lower()}")


def login_expect_failure(driver, wait, email):
    """Tente une connexion avec un email invalide et vérifie l'erreur attendue."""
    driver.get("http://127.0.0.1:5000/")

    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.TAG_NAME, "button").click()

    wait(driver, "unknown email")
    return driver.page_source.lower()


# -----------------------------------------------------------
#  NAVIGATION HELPERS
# -----------------------------------------------------------


def go_to_booking_page(driver, wait):
    """Navigue vers la page de réservation et attend son affichage."""
    link = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Book Places"))
    )
    link.click()

    wait(driver, "how many places?")


# -----------------------------------------------------------
#  ACTION HELPERS
# -----------------------------------------------------------


def book_places(driver, places):
    """Renseigne le formulaire de réservation puis le soumet."""
    field = driver.find_element(By.NAME, "places")
    field.clear()
    field.send_keys(str(places))

    driver.find_element(By.TAG_NAME, "button").click()
