import gudlft_reservation.views.main as main_views
from gudlft_reservation.app import app
from gudlft_reservation.views.main import points_board


def test_points_board_unit(monkeypatch):
    test_clubs = [{"name": "Unit Club", "email": "unit@mail.com", "points": 10}]

    monkeypatch.setattr(main_views, "load_clubs", lambda: test_clubs)

    def fake_render(template, **kwargs):
        assert template == "points_board.html"
        assert kwargs["clubs"] == test_clubs
        return "HTML_OK"

    monkeypatch.setattr(main_views, "render_template", fake_render)

    with app.test_request_context():
        result = points_board()

    assert result == "HTML_OK"
