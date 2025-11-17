from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def test_full_booking_flow(browser, wait_for_text_in_page):
    # Accès à la page d'accueil
    browser.get("http://127.0.0.1:5000/")

    # Connexion
    browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
    browser.find_element(By.TAG_NAME, "button").click()

    wait_for_text_in_page(browser, "welcome, john@simplylift.co")

    # Aller à la page de réservation
    browser.find_element(By.LINK_TEXT, "Book Places").click()
    wait_for_text_in_page(browser, "how many places?")

    # Réserver 1 place
    places_input = browser.find_element(By.NAME, "places")
    places_input.clear()
    places_input.send_keys("1")

    # Clic sur le bouton "Book"
    button = browser.find_element(By.TAG_NAME, "button")
    ActionChains(browser).click(button).perform()

    # Vérification finale
    wait_for_text_in_page(browser, "great-booking complete!")
