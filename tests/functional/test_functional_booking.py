import gudlft_reservation.config as config
from tests.functional.helpers import book_places, go_to_booking_page, login


def test_booking_page(browser, wait_for_text):
    """Vérifie que la page de réservation s'affiche correctement via l'URL directe."""
    browser.get("http://127.0.0.1:5000/book/Comp A/Simply Lift")

    wait_for_text(browser, "how many places?")

    page = browser.page_source.lower()

    assert "booking" in page
    assert "comp a" in page
    assert "simply lift" in page


def test_full_booking_flow(browser, wait_for_text):
    """Teste le scénario complet : connexion → réservation → validation."""
    login(browser, wait_for_text)
    go_to_booking_page(browser, wait_for_text)
    book_places(browser, 1)

    wait_for_text(browser, "great-booking complete!")

    page = browser.page_source.lower()
    assert "great-booking complete!" in page


def test_booking_more_than_max_places_requested(browser, wait_for_text):
    """Vérifie qu'une réservation dépassant la limite maximale est refusée."""
    login(browser, wait_for_text)
    go_to_booking_page(browser, wait_for_text)

    book_places(browser, config.MAX_PLACES_REQUESTED + 1)

    wait_for_text(
        browser, f"you cannot book more than {config.MAX_PLACES_REQUESTED} places."
    )

    page = browser.page_source.lower()

    assert "welcome, john@simplylift.co" in page
    assert f"you cannot book more than {config.MAX_PLACES_REQUESTED} places." in page


def test_booking_insufficient_points(browser, wait_for_text, base_test_data):
    """Vérifie qu'une réservation échoue si le club n’a pas assez de points."""
    base_test_data[0][1]["points"] = 5

    login(browser, wait_for_text)
    go_to_booking_page(browser, wait_for_text)

    book_places(browser, 10)

    wait_for_text(browser, "not enough points to book these places.")

    page = browser.page_source.lower()
    assert "not enough points to book these places." in page


def test_booking_past_competition(browser, base_test_data, wait_for_text):
    """Vérifie qu'une réservation est refusée si la compétition est déjà passée."""
    base_test_data[1][0]["date"] = "2020-10-22 13:30:00"

    login(browser, wait_for_text)
    go_to_booking_page(browser, wait_for_text)

    book_places(browser, 10)

    wait_for_text(browser, "you cannot book places for a past competition.")

    page = browser.page_source.lower()
    assert "you cannot book places for a past competition." in page
