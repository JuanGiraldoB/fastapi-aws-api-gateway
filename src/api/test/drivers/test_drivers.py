from fastapi.testclient import TestClient
from fastapi import status

from api.test.conftest import app


client = TestClient(app=app)


def test_get_drivers_fail(year: dict):
    response = client.get(f"/drivers/{year['invalid_year']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_drivers_success(year: dict):
    response = client.get(f"/drivers/{year['valid_year']}")
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert isinstance(data, dict)
    assert "VER" in data
    assert data["LEC"]["car"] == "Ferrari"
