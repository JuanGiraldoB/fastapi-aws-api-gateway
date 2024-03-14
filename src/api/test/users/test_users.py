from fastapi.testclient import TestClient
from fastapi import status

from api.test.conftest import app


client = TestClient(app=app)


def test_read_user_fail(user: dict):
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_create_user(user: dict):
    response = client.post(
        "/users/",
        json=user,
    )
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["contact_info"] == "somewhere"
    assert "id" in data


def test_read_user(user: dict):
    response = client.get(f"/users/{user['id']}")
    assert response.status_code == status.HTTP_200_OK, response.text

    data = response.json()
    assert data["email"] == "deadpool@example.com"
    assert data["contact_info"] == "somewhere"
    assert data["id"] == 1


def test_read_users():
    response = client.get("/users/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_update_user(user: dict):
    new_user = {
        "name": "Wolverine",
        "email": "wolverine@example.com",
        "contact_info": "here"
    }

    response = client.put(f"/users/{user['id']}", json=new_user)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "Wolverine"
    assert data["email"] == "wolverine@example.com"
    assert data["contact_info"] == "here"


def test_create_dog_for_user(dog: dict):
    response = client.post(f"/users/{dog['owner_id']}/dogs/", json=dog)
    data = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data["name"] == "Rocket"
    assert data["breed"] == "Chanda"


def test_delete_user(user: dict):
    response = client.delete(f"/users/{user['id']}")
    data_valid_user = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert data_valid_user["detail"] == "User deleted"

    response = client.delete(f"/users/{5}")
    data_invalid_user = response.json()
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert data_invalid_user["detail"] == "User does not exist"
