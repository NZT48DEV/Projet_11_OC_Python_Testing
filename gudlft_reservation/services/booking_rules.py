from datetime import datetime

import gudlft_reservation.config as config


def can_book(club, competition, places_requested):
    try:
        if not isinstance(club, dict):
            return False, "Invalid club data."

        if not isinstance(competition, dict):
            return False, "Invalid competition data."

        requested = int(places_requested)
        available_points = int(club.get("points", 0))
        competition_places = int(competition.get("numberOfPlaces", 0))
        competition_date = datetime.strptime(competition["date"], config.DATE_FORMAT)

        if competition_date < config.CURRENT_DATETIME:
            return False, "You cannot book places for a past competition."

        if requested <= 0:
            return False, "You must book at least one place."

        if requested > config.MAX_PLACES_REQUESTED:
            return (
                False,
                f"You cannot book more than {config.MAX_PLACES_REQUESTED} places.",
            )

        already_booked = competition.get("bookings", {}).get(club["name"], 0)

        if already_booked + requested > config.MAX_PLACES_REQUESTED:
            return (
                False,
                (
                    f"You already booked {already_booked} places for this competition. "
                    f"Maximum allowed is {config.MAX_PLACES_REQUESTED}."
                ),
            )

        if requested > available_points:
            return False, (
                "Not enough points to book these places. "
                f"You requested {requested} places but only {available_points} points are available."
            )

        if requested > competition_places:
            return False, (
                "Not enough places available for this competition. "
                f"You requested {requested} places but only {competition_places} places remain."
            )

        return True, ""

    except (TypeError, ValueError):
        return False, "Invalid number of places."
