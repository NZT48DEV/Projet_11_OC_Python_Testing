import json
import os
from io import StringIO

import gudlft_reservation.models.data_access as data_access


def test_save_clubs_writes_correct_json_and_uses_correct_file(monkeypatch):
    # Fake open() pour capturer le chemin et les options
    fake_file = StringIO()
    open_call = {}

    def fake_open(path, mode="r", encoding=None):
        open_call["path"] = path
        open_call["mode"] = mode
        open_call["encoding"] = encoding
        return fake_file

    monkeypatch.setattr("builtins.open", fake_open)

    # Fake json.dump() pour capturer les données
    dumped_data = {}

    def fake_dump(data, file, indent=None):
        dumped_data["data"] = data
        dumped_data["indent"] = indent

    monkeypatch.setattr(json, "dump", fake_dump)

    # Données à sauvegarder
    clubs = [{"name": "Test Club", "email": "a@b.c", "points": 10}]

    # Appel de la fonction testée
    data_access.save_clubs(clubs)

    # Assertions sur json.dump
    assert dumped_data["data"] == {"clubs": clubs}
    assert dumped_data["indent"] == 4

    # Assertions sur le fichier utilisé
    expected_path = os.path.join(data_access.BASE_DIR, "clubs.json")
    assert open_call["path"] == expected_path
    assert open_call["mode"] == "w"
    assert open_call["encoding"] == "utf-8"


def test_save_competitions_writes_correct_json_and_uses_correct_file(monkeypatch):
    fake_file = StringIO()
    open_call = {}

    def fake_open(path, mode="r", encoding=None):
        open_call["path"] = path
        open_call["mode"] = mode
        open_call["encoding"] = encoding
        return fake_file

    monkeypatch.setattr("builtins.open", fake_open)

    dumped_data = {}

    def fake_dump(data, file, indent=None):
        dumped_data["data"] = data
        dumped_data["indent"] = indent

    monkeypatch.setattr(json, "dump", fake_dump)

    competitions = [
        {"name": "Comp A", "date": "2030-05-01 10:00:00", "numberOfPlaces": 30}
    ]

    data_access.save_competitions(competitions)

    assert dumped_data["data"] == {"competitions": competitions}
    assert dumped_data["indent"] == 4

    expected_path = os.path.join(data_access.BASE_DIR, "competitions.json")
    assert open_call["path"] == expected_path
    assert open_call["mode"] == "w"
    assert open_call["encoding"] == "utf-8"
