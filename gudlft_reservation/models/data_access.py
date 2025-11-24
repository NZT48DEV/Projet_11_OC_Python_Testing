import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_clubs():
    """Charge et retourne la liste des clubs depuis le fichier JSON."""
    with open(os.path.join(BASE_DIR, "clubs.json"), encoding="utf-8") as f:
        return json.load(f)["clubs"]


def load_competitions():
    """Charge et retourne la liste des compétitions depuis le fichier JSON."""
    with open(os.path.join(BASE_DIR, "competitions.json"), encoding="utf-8") as f:
        return json.load(f)["competitions"]


def save_clubs(clubs):
    """Enregistre la liste des clubs dans le fichier JSON."""
    with open(os.path.join(BASE_DIR, "clubs.json"), "w", encoding="utf-8") as f:
        json.dump({"clubs": clubs}, f, indent=4)


def save_competitions(competitions):
    """Enregistre la liste des compétitions dans le fichier JSON."""
    with open(os.path.join(BASE_DIR, "competitions.json"), "w", encoding="utf-8") as f:
        json.dump({"competitions": competitions}, f, indent=4)
