def test_index_page_loads(client):
    """Vérifie que la page d'accueil se charge correctement."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.get_data(as_text=True)
