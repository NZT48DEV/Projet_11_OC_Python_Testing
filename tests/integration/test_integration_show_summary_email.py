def test_show_summary_invalid_email(client):
    response = client.post("/showSummary", data={"email": "wrong@email.com"})

    assert response.status_code == 200

    page = response.get_data(as_text=True).lower()

    # Vérifie que le message apparaît
    assert "unknown email" in page

    # Vérifie qu'on est revenu sur index.html
    assert "please enter your secretary email" in page

    # Vérifie que le formulaire showSummary est bien affiché
    assert '<form action="showsummary"' in page

    # Vérifie qu'il y a bien un bouton submit
    assert '<button type="submit">' in page


def test_show_summary_valid_email(client, base_test_data):
    clubs, competitions = base_test_data  # conftest.py

    # On fixe l'email du premier club pour correspondre au test
    clubs[0]["email"] = "john@simplylift.co"

    response = client.post("/showSummary", data={"email": "john@simplylift.co"})

    assert response.status_code == 200
    page = response.get_data(as_text=True).lower()

    # On doit être sur welcome.html
    assert "welcome" in page

    # L'email doit apparaître
    assert "john@simplylift.co" in page

    # Aucune erreur ne doit apparaître
    assert "unknown email" not in page
    assert "unknown club" not in page
