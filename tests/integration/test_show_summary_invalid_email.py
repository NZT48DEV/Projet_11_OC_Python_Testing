def test_show_summary_invalid_email(client):
    response = client.post("/showSummary", data={"email": "wrong@email.com"})

    assert response.status_code == 200

    page = response.get_data(as_text=True).lower()

    # Vérifie que le message d’erreur Flash apparaît
    assert "erreur" in page or "error" in page

    # Vérifie qu'on est revenu sur index.html
    assert "welcome to the gudlft registration portal" in page

    # Vérifie que le formulaire showSummary est bien affiché
    assert '<form action="showsummary"' in page

    # Vérifie qu'il y a bien un bouton submit
    assert '<button type="submit">' in page


def test_show_summary_valid_email(client):
    response = client.post("/showSummary", data={"email": "john@simplylift.co"})

    assert response.status_code == 200
    page = response.get_data(as_text=True)

    # On doit arriver sur la page welcome
    assert "Welcome" in page or "welcome" in page.lower()
    assert "john@simplylift.co" in page
