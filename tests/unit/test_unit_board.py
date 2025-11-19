import gudlft_reservation.server as server


def test_points_board_unit(monkeypatch):
    fake_clubs = [{"name": "Unit Club", "email": "unit@club.com", "points": 10}]

    # Mock loadClubs()
    monkeypatch.setattr(server, "loadClubs", lambda: fake_clubs)

    # Mock render_template()
    def fake_render(template, clubs):
        assert template == "points_board.html"
        assert clubs == fake_clubs
        return "HTML_OK"

    monkeypatch.setattr(server, "render_template", fake_render)

    # Appel de la fonction
    result = server.points_board()

    assert result == "HTML_OK"
