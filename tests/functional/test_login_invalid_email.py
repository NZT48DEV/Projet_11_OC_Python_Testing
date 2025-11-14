from selenium.webdriver.common.by import By


def test_login_invalid_email(browser, wait_for_text_in_page):
    browser.get("http://127.0.0.1:5000/")

    email_input = browser.find_element(By.NAME, "email")
    email_input.send_keys("user_inexistant@test.com")

    browser.find_element(By.TAG_NAME, "button").click()

    wait_for_text_in_page(browser, "erreur : email inconnu")

    page = browser.page_source.lower()
    assert "please enter your secretary email" in page
    assert "erreur : email inconnu" in page
