from gudlft_reservation.server import loadCompetitions

# --------- Helpers ---------


def get_competition_by_name(comps, name):
    return next((c for c in comps if c["name"] == name), None)


# --------- Tests de base / existence ---------


def test_load_competitions_returns_list():
    comps = loadCompetitions()
    assert isinstance(comps, list)
    assert len(comps) > 0


def test_competition_has_expected_fields():
    comp = loadCompetitions()[0]
    assert "name" in comp
    assert "date" in comp
    assert "numberOfPlaces" in comp


# --------- Tests lookup name ---------


def test_get_competition_found():
    comps = loadCompetitions()
    result = get_competition_by_name(comps, "Spring Festival")
    assert result is not None
    assert result["name"] == "Spring Festival"


def test_get_competition_not_found():
    comps = loadCompetitions()
    result = get_competition_by_name(comps, "Unknown Competition")
    assert result is None
