import pytest

import gudlft_reservation.server as app_server


@pytest.fixture(autouse=True)
def reset_globals():
    """Reset les données globales pour TOUS les tests."""
    app_server.clubs = app_server.loadClubs()
    app_server.competitions = app_server.loadCompetitions()
