from flask import Blueprint, flash, redirect, render_template, request, url_for

import gudlft_reservation.models.data_loader as data_loader

bp = Blueprint("main", __name__)


def get_clubs():
    return data_loader.load_clubs()


def get_competitions():
    return data_loader.load_competitions()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/showSummary", methods=["GET", "POST"])
def show_summary():
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
    clubs_list = get_clubs()
    return render_template("points_board.html", clubs=clubs_list)


@bp.route("/logout")
def logout():
    return redirect(url_for("main.index"))
