from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def test_full_booking_flow(browser, wait_for_text_in_page):
    browser.get("http://127.0.0.1:5000/")

    browser.find_element(By.NAME, "email").send_keys("john@simplylift.co")
    browser.find_element(By.TAG_NAME, "button").click()

    wait_for_text_in_page(browser, "welcome, john@simplylift.co")

    link = WebDriverWait(browser, 3).until(
        EC.presence_of_element_located((By.LINK_TEXT, "Book Places"))
    )
    link.click()

    wait_for_text_in_page(browser, "how many places?")

    places_input = browser.find_element(By.NAME, "places")
    places_input.clear()
    places_input.send_keys("1")

    button = browser.find_element(By.TAG_NAME, "button")
    ActionChains(browser).move_to_element(button).click(button).perform()

    wait_for_text_in_page(browser, "great-booking complete!")
