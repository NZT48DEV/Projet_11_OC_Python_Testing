def test_booking_page(browser, wait_for_text_in_page):
    # Accès direct à la page : /book/<competition>/<club>
    browser.get("http://127.0.0.1:5000/book/Spring Festival/Simply Lift")

    # On attend que la page booking soit chargée
    wait_for_text_in_page(browser, "how many places?")

    page = browser.page_source.lower()

    # Assertions robustes
    assert "booking" in page
    assert "spring festival" in page
    assert "simply lift" in page
