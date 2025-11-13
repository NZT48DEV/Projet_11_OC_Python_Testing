import json

import pytest

from gudlft_reservation.server import loadClubs, loadCompetitions


@pytest.fixture(
    params=[
        (loadClubs, "clubs.json", {"email", "name", "points"}),
        (loadCompetitions, "competitions.json", {"name", "date", "numberOfPlaces"}),
    ]
)
def loader(request):
    """Fixture paramétrée : (fonction, nom fichier, clés attendues)."""
    return request.param


def test_loading_functions_return_list(loader):
    func, _, _ = loader
    data = func()
    assert isinstance(data, list)
    assert len(data) > 0


def test_loaded_items_have_expected_fields(loader):
    func, _, expected_keys = loader
    item = func()[0]
    assert set(item.keys()) >= expected_keys


def test_loading_invalid_json(monkeypatch, tmp_path, loader):
    func, filename, _ = loader
    fake_file = tmp_path / filename
    fake_file.write_text("{ invalid json ")

    monkeypatch.setattr("gudlft_reservation.server.BASE_DIR", str(tmp_path))

    with pytest.raises(json.JSONDecodeError):
        func()


def test_loading_missing_file(monkeypatch, tmp_path, loader):
    func, _, _ = loader

    monkeypatch.setattr("gudlft_reservation.server.BASE_DIR", str(tmp_path))

    with pytest.raises(FileNotFoundError):
        func()
