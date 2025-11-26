from flask import Blueprint, flash, render_template, request

import gudlft_reservation.models.data_access as data_access
from gudlft_reservation.services.booking_rules import can_book

bp = Blueprint("booking", __name__)


def get_clubs():
    """Charge les clubs et convertit les points en entiers."""
    clubs = data_access.load_clubs()
    for c in clubs:
        c["points"] = int(c["points"])
    return clubs


def get_competitions():
    comps = data_access.load_competitions()
    for c in comps:
        c["numberOfPlaces"] = int(c["numberOfPlaces"])
        if "bookings" not in c:
            c["bookings"] = {}  # Nouveau : suivi des réservations par club
    return comps


@bp.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Affiche la page de réservation pour un club et une compétition donnés.
    Si l'un des deux est introuvable, renvoie une page d'accueil avec un message.
    """
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
    """
    Traite une demande de réservation :
    - Vérifie club et compétition
    - Applique les règles métier via can_book()
    - Met à jour les données si la réservation est valide
    """
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

    competition.setdefault("bookings", {})
    competition["bookings"][club_name] = (
        competition["bookings"].get(club_name, 0) + places_required
    )

    club["points"] -= places_required
    competition["numberOfPlaces"] -= places_required

    data_access.save_clubs(clubs)
    data_access.save_competitions(competitions)

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)
