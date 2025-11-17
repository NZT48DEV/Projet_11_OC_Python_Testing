from selenium.webdriver.common.by import By


def test_login_invalid_email(browser, wait_for_text_in_page):
    browser.get("http://127.0.0.1:5000/")

    email_input = browser.find_element(By.NAME, "email")
    email_input.send_keys("user_inexistant@test.com")

    browser.find_element(By.TAG_NAME, "button").click()

    # Attendre l'apparition du message d'erreur
    wait_for_text_in_page(browser, "unknown email")

    page = browser.page_source.lower()

    # Vérifications robustes basées sur les fragments réellement affichés
    assert "unknown email" in page
    assert "please try again" in page


def test_login_valid_email(browser, wait_for_text_in_page):
    browser.get("http://127.0.0.1:5000/")

    email_input = browser.find_element(By.NAME, "email")
    email_input.send_keys("john@simplylift.co")

    browser.find_element(By.TAG_NAME, "button").click()

    # welcome.html affiche "Welcome, <email>"
    wait_for_text_in_page(browser, "welcome, john@simplylift.co")

    page = browser.page_source.lower()
    assert "welcome" in page
    assert "john@simplylift.co" in page
