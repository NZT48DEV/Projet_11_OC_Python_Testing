def test_show_summary_invalid_club(client):
    # Accès via ?club=xxx (non existant)
    response = client.get("/showSummary?club=un_club_inexistant")

    assert response.status_code == 200
    text = response.data.decode().lower()

    assert "unknown club" in text
    assert "please enter your secretary email" in text  # contenu de index.html


def test_show_summary_valid_club(client, base_test_data):
    clubs, competitions = base_test_data  # conftest.py

    # --- Requête GET avec un club valide ---
    response = client.get("/showSummary?club=Test Club")

    assert response.status_code == 200
    page = response.get_data(as_text=True).lower()

    # On doit être sur welcome.html
    assert "welcome" in page

    # Le club doit apparaître dans les liens du template
    # (URL encoded : "test%20club")
    assert "test%20club" in page

    # Le nom de compétition doit apparaître
    assert "comp a" in page

    # Aucune erreur affichée
    assert "unknown email" not in page
    assert "unknown club" not in page
