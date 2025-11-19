import gudlft_reservation.config as config
from tests.functional.helpers import book_places, go_to_booking_page, login


def test_booking_page(browser, wait_for_text):
    # Accès direct à la page : /book/<competition>/<club>
    browser.get("http://127.0.0.1:5000/book/Spring Festival/Simply Lift")

    # On attend que la page booking soit chargée
    wait_for_text(browser, "how many places?")

    page = browser.page_source.lower()

    # Assertions robustes
    assert "booking" in page
    assert "spring festival" in page
    assert "simply lift" in page


def test_full_booking_flow(browser, wait_for_text):
    # Connexion via helper
    login(browser, wait_for_text)

    # Aller à la page de réservation via helper
    go_to_booking_page(browser, wait_for_text)

    # Réserver 1 place via helper
    book_places(browser, 1)

    # Vérification finale
    wait_for_text(browser, "great-booking complete!")

    page = browser.page_source.lower()
    assert "great-booking complete!" in page


def test_booking_more_than_max_places_requested(browser, wait_for_text):
    login(browser, wait_for_text)

    # Navigation vers la page de réservation
    go_to_booking_page(browser, wait_for_text)

    # Tentative de réservation de trop de places
    book_places(browser, config.MAX_PLACES_REQUESTED + 1)

    # Attendre le message d’erreur
    wait_for_text(
        browser, f"you cannot book more than {config.MAX_PLACES_REQUESTED} places."
    )

    page = browser.page_source.lower()

    assert "welcome, john@simplylift.co" in page
    assert f"you cannot book more than {config.MAX_PLACES_REQUESTED} places." in page


def test_booking_insufficient_points(browser, wait_for_text, base_test_data):
    # On modifie la fixture : Simply Lift n’a plus que 5 points
    base_test_data[0][1]["points"] = 5  # test_clubs[0]["points"] = 5

    # Connexion
    login(browser, wait_for_text)

    # Navigation vers page booking
    go_to_booking_page(browser, wait_for_text)

    # Demande de 10 places (<= 12 mais > points)
    book_places(browser, 10)

    # Attente du message d'erreur correct
    wait_for_text(browser, "not enough points to book these places.")

    page = browser.page_source.lower()

    assert "not enough points to book these places." in page


def test_booking_past_competition(browser, base_test_data, wait_for_text):
    # On modifie la fixture : Date de Spring Festival
    base_test_data[1][0]["date"] = "2020-10-22 13:30:00"

    # Connexion
    login(browser, wait_for_text)

    # Navigation vers page booking
    go_to_booking_page(browser, wait_for_text)

    # Demande de 10 places
    book_places(browser, 10)

    # Attente du message d'erreur correct
    wait_for_text(browser, "you cannot book places for a past competition.")

    page = browser.page_source.lower()

    assert "you cannot book places for a past competition." in page
