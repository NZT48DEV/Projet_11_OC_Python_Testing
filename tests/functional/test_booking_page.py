def test_booking_page(browser):
    browser.get("http://127.0.0.1:5000/book/Spring Festival/Simply Lift")

    page = browser.page_source.lower()

    assert "booking" in page
    assert "spring festival" in page
    assert "simply lift" in page
