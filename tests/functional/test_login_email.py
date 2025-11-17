from selenium.webdriver.common.by import By


def test_login_invalid_email(browser, wait_for_text_in_page):
    # Accès page d'accueil
    browser.get("http://127.0.0.1:5000/")

    # Saisie d’un email invalide
    browser.find_element(By.NAME, "email").send_keys("user_inexistant@test.com")
    browser.find_element(By.TAG_NAME, "button").click()

    # Attente du message d’erreur
    wait_for_text_in_page(browser, "unknown email")

    page = browser.page_source.lower()

    # Vérifications robustes
    assert "unknown email" in page
    assert "please try again" in page


def test_login_valid_email(browser, wait_for_text_in_page):
    # Accès page d'accueil
    browser.get("http://127.0.0.1:5000/")

    # Saisie email valide
    browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
    browser.find_element(By.TAG_NAME, "button").click()

    # Attente de la page welcome
    wait_for_text_in_page(browser, "welcome, john@simplylift.co")

    page = browser.page_source.lower()

    # Vérifications robustes
    assert "welcome" in page
    assert "john@simplylift.co" in page
