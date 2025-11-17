import json
import os

from flask import Flask, flash, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def loadClubs():
    path = os.path.join(BASE_DIR, "clubs.json")
    with open(path) as c:
        return json.load(c)["clubs"]


def loadCompetitions():
    path = os.path.join(BASE_DIR, "competitions.json")
    with open(path) as comps:
        return json.load(comps)["competitions"]


def can_book(club: dict, places_requested: int) -> bool:
    """
    Retourne True si le club peut réserver `places_requested` places.
    Gère club None, club invalide, points invalides, places invalides, etc.
    """
    try:
        # Club doit être un dictionnaire valide
        if not isinstance(club, dict):
            return False

        available_points = int(club.get("points", 0))
        requested = int(places_requested)

        return available_points >= requested

    except (TypeError, ValueError):
        return False


app = Flask(__name__)
app.secret_key = "something_special"

competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/showSummary", methods=["GET", "POST"])
def showSummary():
    # --- Détection email POST (login normal) ---
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        club = next((c for c in clubs if c["email"].strip().lower() == email), None)
        if club is None:
            flash("Erreur : email inconnu. Veuillez réessayer.")
            return render_template("index.html"), 200

    # --- Détection club GET (retour après /purchasePlaces) ---
    else:
        club_name = request.args.get("club", "").strip().lower()
        club = next((c for c in clubs if c["name"].strip().lower() == club_name), None)
        if club is None:
            flash("Erreur : club inconnu.")
            return render_template("index.html"), 200

    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    foundClub = next((c for c in clubs if c["name"] == club), None)
    foundCompetition = next((c for c in competitions if c["name"] == competition), None)

    if not foundClub or not foundCompetition:
        flash("Something went wrong")
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
    # Récupération des noms envoyés par le formulaire
    competition_name = request.form["competition"]
    club_name = request.form["club"]
    places_raw = request.form.get("places", "0")

    # Recherche du club et de la compétition
    competition = next(c for c in competitions if c["name"] == competition_name)
    club = next(c for c in clubs if c["name"] == club_name)

    # Utilisation de la règle métier centralisée
    if not can_book(club, places_raw):
        flash("You do not have enough points to book these places.")
        return (
            render_template("welcome.html", club=club, competitions=competitions),
            200,
        )

    # À partir d’ici, on sait que la réservation est valide
    places_required = int(places_raw)
    club_points = int(club.get("points", 0))

    # Mise à jour des points du club
    club["points"] = club_points - places_required

    # Mise à jour des places de la compétition
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - places_required

    flash("Great-booking complete!")

    # IMPORTANT : on renvoie directement welcome.html (status 200)
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":  # pragma: no cover
    app.run(host="127.0.0.1", port=5000, debug=False)
