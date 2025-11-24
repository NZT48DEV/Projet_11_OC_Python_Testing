from flask import Blueprint, flash, redirect, render_template, request, url_for

import gudlft_reservation.models.data_access as data_access

bp = Blueprint("main", __name__)


def get_clubs():
    """Charge et retourne la liste des clubs."""
    return data_access.load_clubs()


def get_competitions():
    """Charge et retourne la liste des compétitions."""
    return data_access.load_competitions()


@bp.route("/")
def index():
    """Affiche la page d'accueil et le formulaire de connexion."""
    return render_template("index.html")


@bp.route("/showSummary", methods=["GET", "POST"])
def show_summary():
    """
    Affiche le tableau de bord d'un club :
    - Authentification par email (POST)
    - Accès direct via nom du club (GET)
    """
    clubs = get_clubs()
    competitions = get_competitions()

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        club = next((c for c in clubs if c["email"].lower() == email), None)

        if club is None:
            flash("Unknown email. Please try again.")
            return render_template("index.html"), 200

    else:
        club_name = request.args.get("club", "").strip().lower()
        club = next((c for c in clubs if c["name"].lower() == club_name), None)

        if club is None:
            flash("Unknown club.")
            return render_template("index.html"), 200

    return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/pointsBoard")
def points_board():
    """Affiche le tableau récapitulatif des points de tous les clubs."""
    clubs_list = get_clubs()
    return render_template("points_board.html", clubs=clubs_list)


@bp.route("/logout")
def logout():
    """Déconnecte l’utilisateur et le renvoie vers la page d’accueil."""
    return redirect(url_for("main.index"))
