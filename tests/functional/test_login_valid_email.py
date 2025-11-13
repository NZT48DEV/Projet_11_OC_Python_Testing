def test_login_valid_email(browser):
    browser.get("http://127.0.0.1:5000/")

    # Entrer un email valide
    email_input = browser.find_element("name", "email")
    email_input.send_keys("john@simplylift.co")

    browser.find_element("tag name", "button").click()

    page = browser.page_source.lower()

    assert "welcome" in page
    assert "john@simplylift.co" in page
