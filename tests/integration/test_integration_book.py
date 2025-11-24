def test_book_valid(client, base_test_data):
    """Vérifie qu'une page de réservation valide s'affiche correctement."""
    response = client.get("/book/Comp A/Test Club")

    assert response.status_code == 200
    page = response.get_data(as_text=True).lower()

    assert "booking" in page
    assert "comp a" in page
    assert "test club" in page


def test_book_invalid_club(client, base_test_data):
    """Vérifie que l'accès échoue si le club est inconnu."""
    response = client.get("/book/Comp A/ClubInexistant")
    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "unknown club or competition" in page


def test_book_invalid_competition(client, base_test_data):
    """Vérifie que l'accès échoue si la compétition est inconnue."""
    response = client.get("/book/UnknownCompetition/Test Club")
    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "unknown club or competition" in page
