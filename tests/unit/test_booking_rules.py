from gudlft_reservation.server import can_book


def test_can_book_refuses_when_not_enough_points():
    club = {
        "name": "Test Club",
        "email": "test@club.com",
        "points": "5",
    }

    places_requested = 6

    result = can_book(club, places_requested)

    assert result is False


def test_can_book_when_enough_points():
    club = {"name": "Club Test", "points": "10"}

    result = can_book(club, 5)

    assert result is True


def test_can_book_invalid_values():
    """Forcer une TypeError / ValueError pour couvrir le bloc except."""

    # Valeurs invalides
    assert can_book(None, 5) is False  # TypeError
    assert can_book("abc", 2) is False  # ValueError
    assert can_book(10, "abc") is False  # ValueError
    assert can_book([], {}) is False  # TypeError


def test_can_book_invalid_points_valueerror():
    """Forcer une ValueError : points = 'abc'."""
    club = {"name": "Test Club", "points": "abc"}
    assert can_book(club, 1) is False
