def test_show_summary_invalid_club(client):
    # Accès via ?club=xxx (non existant)
    response = client.get("/showSummary?club=un_club_inexistant")

    assert response.status_code == 200
    text = response.data.decode().lower()

    assert "erreur : club inconnu" in text
    assert "please enter your secretary email" in text  # contenu de index.html
