from flask import Blueprint, flash, render_template, request

from gudlft_reservation.models.data_loader import load_clubs, load_competitions
from gudlft_reservation.services.booking_rules import can_book

bp = Blueprint("booking", __name__)


def get_clubs():
    clubs = load_clubs()
    for c in clubs:
        c["points"] = int(c["points"])
    return clubs


def get_competitions():
    comps = load_competitions()
    for c in comps:
        c["numberOfPlaces"] = int(c["numberOfPlaces"])
    return comps


@bp.route("/book/<competition>/<club>")
def book(competition, club):
    clubs = get_clubs()
    competitions = get_competitions()

    found_club = next((c for c in clubs if c["name"] == club), None)
    found_competition = next(
        (c for c in competitions if c["name"] == competition), None
    )

    if not found_club or not found_competition:
        flash("Unknown club or competition.")
        return (
            render_template(
                "welcome.html",
                club=found_club or {"name": "", "email": "", "points": 0},
                competitions=competitions,
            ),
            200,
        )

    return render_template(
        "booking.html", club=found_club, competition=found_competition
    )


@bp.route("/purchasePlaces", methods=["POST"])
def purchase_places():
    clubs = get_clubs()
    competitions = get_competitions()

    competition_name = request.form["competition"]
    club_name = request.form["club"]
    places_raw = request.form.get("places", "0")

    competition = next((c for c in competitions if c["name"] == competition_name), None)
    club = next((c for c in clubs if c["name"] == club_name), None)

    if club is None:
        flash("Unknown club.")
        return render_template("index.html"), 200

    if competition is None:
        flash("Unknown competition.")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            200,
        )

    is_allowed, error_message = can_book(club, competition, places_raw)

    if not is_allowed:
        flash(error_message)
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            200,
        )

    places_required = int(places_raw)
    club["points"] -= places_required
    competition["numberOfPlaces"] -= places_required

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)
