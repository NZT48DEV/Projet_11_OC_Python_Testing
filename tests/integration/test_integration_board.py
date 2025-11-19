import gudlft_reservation.server as server


def test_points_board_integration(client, monkeypatch):
    # Données contrôlées pour le test
    fake_clubs = [
        {"name": "Alpha Club", "email": "alpha@mail.com", "points": 15},
        {"name": "Beta Club", "email": "beta@mail.com", "points": 7},
    ]

    # Mock loadClubs pour contrôler le contenu de la page
    monkeypatch.setattr(server, "loadClubs", lambda: fake_clubs)

    # Appel réel de la route Flask
    response = client.get("/pointsBoard")

    # Statut correct
    assert response.status_code == 200

    # Vérification du rendu
    html = response.data.decode()

    assert "Alpha Club" in html
    assert "15" in html
    assert "Beta Club" in html
    assert "7" in html

    # Vérifie que le tableau est présent
    assert "<table" in html.lower()
