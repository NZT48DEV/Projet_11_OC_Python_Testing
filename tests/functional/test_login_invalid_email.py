def test_login_invalid_email(browser):
    browser.get("http://127.0.0.1:5000/")

    # Email invalide
    email_input = browser.find_element("name", "email")
    email_input.send_keys("wrong@email.com")

    browser.find_element("tag name", "button").click()

    page = browser.page_source.lower()

    # On reste sur index.html (le titre de la page d'accueil est toujours là)
    assert "welcome to the gudlft registration portal" in page

    # Le formulaire de login est toujours présent
    assert '<form action="showsummary"' in page
    assert 'name="email"' in page

    # On NE voit PAS le texte spécifique de la page welcome (page club connecté)
    assert "points available" not in page
    assert "logout" not in page
