from fastapi.testclient import TestClient
from fastapi import status

from api.test.conftest import app


client = TestClient(app=app)


def test_get_races_fail(year: dict):
    response = client.get(f"/races/{year['invalid_year']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_races_success(year: dict):
    response = client.get(f"/races/{year['valid_year']}")
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert isinstance(data, dict)
    assert "Bahrain" in data
    assert data["Australia"]["winner"] == "Carlos Sainz"


def test_get_fastest_laps_fail(year: dict):
    response = client.get(f"/races/fastest-laps/{year['invalid_year']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_fastest_laps_success(year: dict):
    response = client.get(f"/races/fastest-laps/{year['valid_year']}")
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert isinstance(data, dict)
    assert "Bahrain" in data
    assert data["Saudi Arabia"]["driver"] == "Charles Leclerc"
    assert data["Saudi Arabia"]["lap_time"] == "1:31.632"
