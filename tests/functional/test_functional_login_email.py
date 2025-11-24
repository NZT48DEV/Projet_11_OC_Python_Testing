from selenium.webdriver.common.by import By


def test_login_invalid_email(browser, wait_for_text):
    """Vérifie que la connexion échoue avec un email invalide et affiche un message d'erreur."""
    browser.get("http://127.0.0.1:5000/")

    browser.find_element(By.NAME, "email").send_keys("user_inexistant@test.com")
    browser.find_element(By.TAG_NAME, "button").click()

    wait_for_text(browser, "unknown email")

    page = browser.page_source.lower()

    assert "unknown email" in page
    assert "please try again" in page


def test_login_valid_email(browser, wait_for_text):
    """Vérifie qu'un email valide permet de se connecter et d'afficher la page d'accueil."""
    browser.get("http://127.0.0.1:5000/")

    browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
    browser.find_element(By.TAG_NAME, "button").click()

    wait_for_text(browser, "welcome, john@simplylift.co")

    page = browser.page_source.lower()

    assert "welcome" in page
    assert "john@simplylift.co" in page
