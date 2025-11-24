def test_show_summary_invalid_email(client):
    """Vérifie qu'un email invalide renvoie une erreur et recharge la page d'accueil."""
    response = client.post("/showSummary", data={"email": "wrong@email.com"})

    assert response.status_code == 200

    page = response.get_data(as_text=True).lower()

    assert "unknown email" in page
    assert "please enter your secretary email" in page
    assert '<form action="showsummary"' in page
    assert '<button type="submit">' in page


def test_show_summary_valid_email(client, base_test_data):
    """Vérifie qu'un email valide permet d'accéder à la page de résumé (welcome)."""
    clubs, competitions = base_test_data

    clubs[0]["email"] = "john@simplylift.co"

    response = client.post("/showSummary", data={"email": "john@simplylift.co"})

    assert response.status_code == 200
    page = response.get_data(as_text=True).lower()

    assert "welcome" in page
    assert "john@simplylift.co" in page
    assert "unknown email" not in page
    assert "unknown club" not in page
