import gudlft_reservation.models.data_access as data_access
import gudlft_reservation.views.main as main_views
from gudlft_reservation.app import create_app


def test_points_board_unit(monkeypatch):
    test_clubs = [{"name": "Unit Club", "email": "unit@mail.com", "points": 10}]

    monkeypatch.setattr(data_access, "load_clubs", lambda: test_clubs)

    def fake_render(template, **kwargs):
        assert template == "points_board.html"
        assert kwargs["clubs"] == test_clubs
        return "HTML_OK"

    monkeypatch.setattr(main_views, "render_template", fake_render)

    app = create_app()
    with app.test_request_context():
        result = main_views.points_board()

    assert result == "HTML_OK"
