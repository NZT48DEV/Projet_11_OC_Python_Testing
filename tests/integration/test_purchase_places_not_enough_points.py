from gudlft_reservation.server import clubs, competitions


def test_purchase_places_insufficient_points(client):
    """
    Vérifie qu'un club ne peut pas réserver plus de places
    que son nombre de points.
    """
    # Simply Lift a 13 points -> on demande 20 places
    response = client.post(
        "/purchasePlaces",
        data={
            "competition": "Spring Festival",
            "club": "Simply Lift",
            "places": 20,
        },
    )

    # On reste sur welcome.html, pas de redirect
    assert response.status_code == 200

    page = response.data.decode().lower()

    # Message d’erreur affiché
    assert "you do not have enough points to book these places." in page

    # Les points NE doivent PAS avoir changé !
    # On recharge depuis server.competitions et server.clubs
    club = next(c for c in clubs if c["name"] == "Simply Lift")
    competition = next(c for c in competitions if c["name"] == "Spring Festival")

    assert int(club["points"]) == 13
    assert int(competition["numberOfPlaces"]) == 25
