from gudlft_reservation.server import can_book

# ---------- Helpers ----------
VALID_CLUB = {
    "name": "Test Club",
    "email": "test@club.com",
    "points": "10",
}

VALID_COMPETITION = {
    "name": "Comp A",
    "date": "2025-12-31 10:00:00",
    "numberOfPlaces": "8",
}


# ---------- Tests : points insuffisants ----------
def test_can_book_refuses_when_not_enough_points():
    club = {"name": "Test Club", "email": "test@club.com", "points": "5"}
    allowed, msg = can_book(club, VALID_COMPETITION, 6)

    assert allowed is False
    assert msg == (
        "Not enough points to book these places. "
        "You requested 6 places but only 5 points are available."
    )


def test_can_book_when_enough_points():
    allowed, msg = can_book(VALID_CLUB, VALID_COMPETITION, 5)

    assert allowed is True
    assert msg == ""


# ---------- Tests : valeurs invalides (club / competition non dict) ----------
def test_can_book_invalid_club():
    allowed, msg = can_book(None, VALID_COMPETITION, 5)

    assert allowed is False
    assert msg == "Invalid club data."


def test_can_book_invalid_competition():
    allowed, msg = can_book(VALID_CLUB, None, 5)

    assert allowed is False
    assert msg == "Invalid competition data."


def test_can_book_invalid_values_type_error():
    # club n'est pas un dict
    allowed, msg = can_book("abc", VALID_COMPETITION, 5)
    assert allowed is False
    assert msg == "Invalid club data."

    # competition n'est pas un dict
    allowed, msg = can_book(VALID_CLUB, "abc", 5)
    assert allowed is False
    assert msg == "Invalid competition data."

    # places n'est pas convertible en int -> déclenche le bloc except
    allowed, msg = can_book(VALID_CLUB, VALID_COMPETITION, "xyz")
    assert allowed is False
    assert msg == "Invalid number of places."


def test_can_book_invalid_points_valueerror():
    # points non convertibles en int -> déclenche aussi le bloc except
    club = {"name": "Test Club", "email": "test@club.com", "points": "abc"}
    allowed, msg = can_book(club, VALID_COMPETITION, 2)

    assert allowed is False
    assert msg == "Invalid number of places."


# ---------- Tests : règles métier ----------
def test_can_book_competition_not_enough_places():
    competition = {"name": "Comp B", "numberOfPlaces": "3", "date": "2025-12-31"}
    allowed, msg = can_book(VALID_CLUB, competition, 5)

    assert allowed is False
    assert msg == (
        "Not enough places available for this competition. "
        "You requested 5 places but only 3 places remain."
    )


def test_can_book_requested_zero_or_negative():
    allowed, msg = can_book(VALID_CLUB, VALID_COMPETITION, 0)
    assert allowed is False
    assert msg == "You must book at least one place."

    allowed, msg = can_book(VALID_CLUB, VALID_COMPETITION, -2)
    assert allowed is False
    assert msg == "You must book at least one place."
