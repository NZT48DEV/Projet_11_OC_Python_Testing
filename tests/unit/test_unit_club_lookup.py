from gudlft_reservation.models.data_loader import load_clubs

# --------- Helpers ---------


def get_club_by_email(clubs, email):
    return next((c for c in clubs if c["email"] == email), None)


def get_club_by_name(clubs, name):
    return next((c for c in clubs if c["name"] == name), None)


# --------- Tests de base / existence ---------


def test_load_clubs_returns_list():
    clubs = load_clubs()
    assert isinstance(clubs, list)
    assert len(clubs) > 0


def test_club_has_expected_fields():
    club = load_clubs()[0]
    assert "email" in club
    assert "name" in club
    assert "points" in club


# --------- Tests lookup email ---------


def test_get_club_by_email_found():
    clubs = load_clubs()
    result = get_club_by_email(clubs, "john@simplylift.co")
    assert result is not None
    assert result["email"] == "john@simplylift.co"


def test_get_club_by_email_not_found():
    clubs = load_clubs()
    result = get_club_by_email(clubs, "unknown@email.com")
    assert result is None


# --------- Tests lookup name ---------


def test_get_club_by_name_found():
    clubs = load_clubs()
    result = get_club_by_name(clubs, "Simply Lift")
    assert result is not None
    assert result["name"] == "Simply Lift"


def test_get_club_by_name_not_found():
    clubs = load_clubs()
    result = get_club_by_name(clubs, "Unknown Club")
    assert result is None
