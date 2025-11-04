import pytest

from gudlft_reservation.server import app


@pytest.fixture
def client():
    """Fixture qui crée un client de test Flask"""
    with app.test_client() as client:
        yield client


def test_show_summary_with_invalid_email(client):
    """
    GIVEN un utilisateur entre un email invalide
    WHEN le formulaire de connexion est soumis
    THEN l'application ne plante pas et affiche un message d'erreur
    """
    response = client.post("/showSummary", data={"email": "unknown@email.com"})
    assert response.status_code == 200
    assert "Erreur : email inconnu. Veuillez réessayer." in response.get_data(
        as_text=True
    )
