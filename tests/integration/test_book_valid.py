def test_book_valid(client):
    response = client.get("/book/Spring Festival/Simply Lift")

    assert response.status_code == 200
    page = response.get_data(as_text=True).lower()

    # booking.html contient "booking"
    assert "booking" in page
    assert "spring festival" in page
    assert "simply lift" in page


def test_book_invalid_club(client):
    response = client.get("/book/Spring Festival/ClubInexistant")
    assert response.status_code == 200
    assert "something went wrong" in response.get_data(as_text=True).lower()


def test_book_invalid_competition(client):
    response = client.get("/book/UnknownCompetition/Simply Lift")
    assert response.status_code == 200
    assert "something went wrong" in response.get_data(as_text=True).lower()
