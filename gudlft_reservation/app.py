from flask import Flask


def create_app():
    """Crée et configure l’application Flask avec les blueprints du projet."""
    app = Flask(__name__)
    app.secret_key = "something_special"

    from gudlft_reservation.views.booking import bp as booking_bp
    from gudlft_reservation.views.main import bp as main_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(booking_bp)

    return app
