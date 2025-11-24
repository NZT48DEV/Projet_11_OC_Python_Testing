def test_show_summary_invalid_club(client):
    """Vérifie qu'un club inexistant via paramètre GET renvoie un message d'erreur."""
    response = client.get("/showSummary?club=un_club_inexistant")

    assert response.status_code == 200
    text = response.data.decode().lower()

    assert "unknown club" in text
    assert "please enter your secretary email" in text  # contenu de index.html


def test_show_summary_valid_club(client, base_test_data):
    """Vérifie qu'un club valide accède bien à la page de résumé (welcome)."""
    clubs, competitions = base_test_data

    response = client.get("/showSummary?club=Test Club")

    assert response.status_code == 200
    page = response.get_data(as_text=True).lower()

    assert "welcome" in page
    assert "test%20club" in page  # présence dans les URL du template
    assert "comp a" in page

    assert "unknown email" not in page
    assert "unknown club" not in page
