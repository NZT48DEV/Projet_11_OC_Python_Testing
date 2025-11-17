def test_book_valid(client, sample_data):
    # Accès à la page booking
    response = client.get("/book/Comp A/Test Club")

    assert response.status_code == 200
    page = response.get_data(as_text=True).lower()

    assert "booking" in page
    assert "comp a" in page
    assert "test club" in page


def test_book_invalid_club(client, sample_data):
    response = client.get("/book/Comp A/ClubInexistant")
    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "unknown club or competition" in page


def test_book_invalid_competition(client, sample_data):
    response = client.get("/book/UnknownCompetition/Test Club")
    page = response.get_data(as_text=True).lower()

    assert response.status_code == 200
    assert "unknown club or competition" in page
