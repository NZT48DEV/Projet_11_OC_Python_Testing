import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_clubs():
    with open(os.path.join(BASE_DIR, "clubs.json")) as f:
        return json.load(f)["clubs"]


def load_competitions():
    with open(os.path.join(BASE_DIR, "competitions.json")) as f:
        return json.load(f)["competitions"]
