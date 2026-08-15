import json
from flask import Flask, render_template, request, redirect, flash, url_for
from datetime import datetime


def loadClubs():
    """Load the list of clubs from the clubs.json data file."""
    with open("clubs.json") as clubs_file:
        clubs_list = json.load(clubs_file)["clubs"]
        return clubs_list


def loadCompetitions():
    """Load the list of competitions from the competitions.json data file."""
    with open("competitions.json") as competitions_file:
        competitions_list = json.load(competitions_file)["competitions"]
        return competitions_list


app = Flask(__name__)
app.secret_key = "something_special"

# Load data into memory at startup (acting as our lightweight database)
competitions = loadCompetitions()
clubs = loadClubs()


@app.route("/")
def index():
    """Render the home/login page for club secretaries."""
    return render_template("index.html")


@app.route("/showSummary", methods=["POST"])
def showSummary():
    """
    Handle secretary login by email.
    If the email is found, redirect to the dashboard.
    If not, flash an error and redirect back to the home page.
    """
    # Search for a club matching the submitted email
    matching_clubs = [club for club in clubs if club["email"] == request.form["email"]]

    # If no club matches, notify the user and redirect to the login page
    if not matching_clubs:
        flash("Email not found. Please try again.")
        return redirect(url_for("index"))

    # Retrieve the first (and only) matching club
    club = matching_clubs[0]
    return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/book/<competition>/<club>")
def book(competition, club):
    """
    Display the booking form for a specific competition and club.
    Validates that both the club and competition exist, and that the
    competition has not already taken place.
    """
    # Look up the club and competition by name from the in-memory data
    selected_club = [c for c in clubs if c["name"] == club][0]
    selected_competition = [c for c in competitions if c["name"] == competition][0]

    if selected_club and selected_competition:
        # Parse the competition date string into a datetime object for comparison
        competition_date = datetime.strptime(
            selected_competition["date"], "%Y-%m-%d %H:%M:%S"
        )

        # Prevent booking for competitions that have already taken place
        if competition_date < datetime.now():
            flash("You cannot book places for a past competition.")
            return render_template(
                "welcome.html", club=selected_club, competitions=competitions
            )

        # Calculate the maximum bookable places:
        # limited by the 12-place rule, the club's available points,
        # and remaining competition spots
        max_places = min(
            12,
            int(selected_club["points"]),
            int(selected_competition["numberOfPlaces"]),
        )
        return render_template(
            "booking.html",
            club=selected_club,
            competition=selected_competition,
            max_places=max_places,
        )
    else:
        flash("Something went wrong - please try again.")
        return render_template("welcome.html", club=club, competitions=competitions)


@app.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    """
    Process a booking request submitted from the booking form.
    Runs multiple validations before confirming and deducting points:
        - Competition must not be in the past
        - Number of places must be at least 1
        - Number of places must not exceed 12 (fairness rule)
        - Club must have enough points
        - Competition must have enough places remaining
    """
    # Retrieve the competition and club objects from the form data
    selected_competition = [
        c for c in competitions if c["name"] == request.form["competition"]
    ][0]
    selected_club = [c for c in clubs if c["name"] == request.form["club"]][0]

    # --- Validation 1: Competition must not be in the past ---
    competition_date = datetime.strptime(
        selected_competition["date"], "%Y-%m-%d %H:%M:%S"
    )
    if competition_date < datetime.now():
        flash("You cannot book places for a past competition.")
        return render_template(
            "welcome.html", club=selected_club, competitions=competitions
        )

    places_requested = int(request.form["places"])

    # --- Validation 2: Must request at least 1 place ---
    if places_requested <= 0:
        flash("You must book at least 1 place.")
        return render_template(
            "welcome.html", club=selected_club, competitions=competitions
        )

    # --- Validation 3: Cannot exceed the 12-place fairness limit ---
    if places_requested > 12:
        flash("You cannot book more than 12 places in a single competition.")
        return render_template(
            "welcome.html", club=selected_club, competitions=competitions
        )

    # --- Validation 4: Club must have enough points ---
    if places_requested > int(selected_club["points"]):
        flash("You do not have enough points to book this many places.")
        return render_template(
            "welcome.html", club=selected_club, competitions=competitions
        )

    # --- Validation 5: Competition must have enough places remaining ---
    if places_requested > int(selected_competition["numberOfPlaces"]):
        flash("There are not enough places available in this competition.")
        return render_template(
            "welcome.html", club=selected_club, competitions=competitions
        )

    # All validations passed: deduct places and points
    selected_competition["numberOfPlaces"] = (
        int(selected_competition["numberOfPlaces"]) - places_requested
    )
    selected_club["points"] = int(selected_club["points"]) - places_requested

    flash("Great-booking complete!")
    return render_template(
        "welcome.html", club=selected_club, competitions=competitions
    )


@app.route("/logout")
def logout():
    """Log out the current secretary and redirect to the home page."""
    return redirect(url_for("index"))


@app.route("/points")
def points():
    """
    Display the public points board.
    This page is accessible without logging in, showing all clubs and their points.
    """
    return render_template("points.html", clubs=clubs)
