def test_full_booking_flow(browser):
    # 1. Page d'accueil
    browser.get("http://127.0.0.1:5000/")

    # 2. Login
    browser.find_element("name", "email").send_keys("john@simplylift.co")
    browser.find_element("tag name", "button").click()

    page = browser.page_source.lower()
    assert "welcome" in page

    # 3. Cliquer sur le lien Book Places (TRÈS IMPORTANT)
    link = browser.find_element("link text", "Book Places")
    link.click()

    # Maintenant on est sur booking.html
    page = browser.page_source.lower()
    assert "how many places?" in page
    assert '<form action="/purchaseplaces"' in page

    # 4. Réserver une place
    browser.find_element("name", "places").send_keys("1")
    browser.find_element("tag name", "button").click()

    page = browser.page_source.lower()

    # 5. Retour welcome avec message succès
    assert "great-booking complete!" in page
