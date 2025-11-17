from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_booking_insufficient_points(browser, wait_for_text_in_page):
    browser.get("http://127.0.0.1:5000/")

    browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
    browser.find_element(By.TAG_NAME, "button").click()

    wait_for_text_in_page(browser, "welcome, john@simplylift.co")

    link = WebDriverWait(browser, 5).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Book Places"))
    )
    link.click()

    wait_for_text_in_page(browser, "how many places?")

    places_input = browser.find_element(By.NAME, "places")
    places_input.clear()
    places_input.send_keys("20")

    browser.find_element(By.TAG_NAME, "button").click()

    wait_for_text_in_page(
        browser,
        "not enough points to book these places.",
    )

    page = browser.page_source.lower()

    assert "welcome, john@simplylift.co" in page
    assert "not enough points to book these places." in page
