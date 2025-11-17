import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for

from gudlft_reservation.config import MAX_PLACES_REQUESTED

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def loadClubs():
    path = os.path.join(BASE_DIR, "clubs.json")
    with open(path) as c:
        return json.load(c)["clubs"]


def loadCompetitions():
    path = os.path.join(BASE_DIR, "competitions.json")
    with open(path) as comps:
        return json.load(comps)["competitions"]


def can_book(club: dict, competition: dict, places_requested: int):
    """
    Returns (True, "") if booking is allowed.
    Otherwise (False, "error message").
    Handles:
      - invalid club
      - invalid competition
      - insufficient points
      - insufficient competition places
    """
    try:
        if not isinstance(club, dict):
            return False, "Invalid club data."

        if not isinstance(competition, dict):
            return False, "Invalid competition data."

        requested = int(places_requested)
        available_points = int(club.get("points", 0))
        competition_places = int(competition.get("numberOfPlaces", 0))

        if requested <= 0:
            return False, "You must book at least one place."

        if requested > MAX_PLACES_REQUESTED:
            return False, f"You cannot book more than {MAX_PLACES_REQUESTED} places."

        if requested > available_points:
            return (
                False,
                (
                    "Not enough points to book these places. "
                    f"You requested {requested} places but only {available_points} points are available."
                ),
            )

        if requested > competition_places:
            return (
                False,
                (
                    "Not enough places available for this competition. "
                    f"You requested {requested} places but only {competition_places} places remain."
                ),
            )

        return True, ""

    except (TypeError, ValueError):
        return False, "Invalid number of places."


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["GET", "POST"])
def showSummary():
    # POST: login with email
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        club = next((c for c in clubs if c["email"].strip().lower() == email), None)

        if club is None:
            flash("Unknown email. Please try again.")
            return render_template("index.html"), 200

    # GET: retrieve club by name
    else:
        club_name = request.args.get("club", "").strip().lower()
        club = next((c for c in clubs if c["name"].strip().lower() == club_name), None)

        if club is None:
            flash("Unknown club.")
            return render_template("index.html"), 200

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = next((c for c in clubs if c["name"] == club), None)
    foundCompetition = next((c for c in competitions if c["name"] == competition), None)

    if not foundClub or not foundCompetition:
        flash("Unknown club or competition.")
        return (
            render_template(
                "welcome.html",
                club=foundClub or {"name": "", "email": "", "points": 0},
                competitions=competitions,
            ),
            200,
        )

    return render_template("booking.html", club=foundClub, competition=foundCompetition)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition_name = request.form["competition"]
    club_name = request.form["club"]
    places_raw = request.form.get("places", "0")

    # Safe lookup
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

    # Business logic
    is_allowed, error_message = can_book(club, competition, places_raw)

    if not is_allowed:
        flash(error_message)
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            200,
        )

    # Apply booking
    places_required = int(places_raw)
    club["points"] = int(club["points"]) - places_required
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required

    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))
