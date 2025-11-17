from tests.functional.helpers import book_places, go_to_booking_page, login


def test_booking_insufficient_points(browser, wait_for_text_in_page, patch_server_data):
    # On modifie la fixture : Simply Lift n’a plus que 5 points
    patch_server_data[0][0]["points"] = 5  # test_clubs[0]["points"] = 5

    # Connexion
    login(browser, wait_for_text_in_page)

    # Navigation vers page booking
    go_to_booking_page(browser, wait_for_text_in_page)

    # Demande de 10 places (<= 12 mais > points)
    book_places(browser, 10)

    # Attente du message d'erreur correct
    wait_for_text_in_page(browser, "not enough points to book these places.")

    page = browser.page_source.lower()

    assert "not enough points to book these places." in page
