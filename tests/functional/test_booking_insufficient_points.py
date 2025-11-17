from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_booking_insufficient_points(browser, wait_for_text_in_page):
    # 1️⃣ Page d'accueil
    browser.get("http://127.0.0.1:5000/")

    # 2️⃣ Login avec un email valide
    browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
    browser.find_element(By.TAG_NAME, "button").click()

    # On attend explicitement la page welcome
    wait_for_text_in_page(browser, "welcome, john@simplylift.co")

    # 3️⃣ Aller sur la page de réservation via "Book Places"
    link = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Book Places"))
    )
    link.click()

    # Vérifier qu'on est bien sur booking.html
    wait_for_text_in_page(browser, "how many places?")

    # 4️⃣ Demander plus de places que les points disponibles (ex: 20 > 13)
    places_input = browser.find_element(By.NAME, "places")
    places_input.clear()
    places_input.send_keys("20")

    # Soumettre le formulaire
    browser.find_element(By.TAG_NAME, "button").click()

    # 5️⃣ Vérifier qu'on revient sur la page de résumé AVEC le message d'erreur
    wait_for_text_in_page(
        browser, "you do not have enough points to book these places."
    )

    page = browser.page_source.lower()

    # Toujours sur la page de welcome (club connecté)
    assert "welcome, john@simplylift.co" in page
    assert "points available" in page

    # Message d'erreur bien affiché
    assert "you do not have enough points to book these places." in page
