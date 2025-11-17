from gudlft_reservation.config import MAX_PLACES_REQUESTED
from tests.functional.helpers import book_places, go_to_booking_page, login


def test_cannot_book_more_than_max_places_requested(browser, wait_for_text_in_page):
    login(browser, wait_for_text_in_page)

    # Navigation vers la page de réservation
    go_to_booking_page(browser, wait_for_text_in_page)

    # Tentative de réservation de trop de places
    book_places(browser, MAX_PLACES_REQUESTED + 1)

    # Attendre le message d’erreur
    wait_for_text_in_page(
        browser, f"you cannot book more than {MAX_PLACES_REQUESTED} places."
    )

    page = browser.page_source.lower()

    assert "welcome, john@simplylift.co" in page
    assert f"you cannot book more than {MAX_PLACES_REQUESTED} places." in page
