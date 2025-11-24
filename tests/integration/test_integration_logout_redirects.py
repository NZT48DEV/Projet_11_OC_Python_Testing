def test_logout_redirects(client):
    """Vérifie que la route /logout redirige correctement vers la page d'accueil."""
    response = client.get("/logout")

    assert response.status_code == 302
    assert response.location.endswith("/")
