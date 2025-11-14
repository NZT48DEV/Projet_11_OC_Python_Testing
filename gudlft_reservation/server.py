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
    # Récupération des données
    competition = next(
        c for c in competitions if c["name"] == request.form["competition"]
    )
    club = next(c for c in clubs if c["name"] == request.form["club"])

    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired

    flash("Great-booking complete!")

    # IMPORTANT : on RENVOIE directement welcome.html (status 200)
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/logout")
def logout():
    return redirect(url_for("index"))


if __name__ == "__main__":  # pragma: no cover
    app.run(host="127.0.0.1", port=5000, debug=False)
