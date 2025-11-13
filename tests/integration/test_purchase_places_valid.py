def test_purchase_places_valid(client):
    response = client.post(
        "/purchasePlaces",
        data={"competition": "Spring Festival", "club": "Simply Lift", "places": 1},
    )

    assert response.status_code == 200
    page = response.get_data(as_text=True)

    assert "Great-booking complete!" in page
