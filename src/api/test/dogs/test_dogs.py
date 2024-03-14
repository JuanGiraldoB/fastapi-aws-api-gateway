from fastapi.testclient import TestClient
from fastapi import status

from api.models import User, Dog
from api.test.conftest import app, TestingSessionLocal


client = TestClient(app=app)


def test_read_dogs():
    response = client.get("/dogs/")
    assert response.status_code == status.HTTP_200_OK
    assert isinstance(response.json(), list)


def test_read_dog(dog: dict):
    response = client.get(f"/dogs/{dog['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == dog['name']
    assert data['breed'] == dog['breed']
    assert data['owner_id'] == dog['owner_id']
    assert data['id'] == dog['id']


def test_update_dog(dog: dict):
    new_dog = {"name": "Goldie", "breed": "Golden Retriever"}
    response = client.put(f"/dogs/{dog['id']}", json=new_dog)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['name'] == "Goldie"
    assert data['breed'] == "Golden Retriever"


def test_delete_dog(dog: dict):
    response = client.delete(f"/dogs/{dog['id']}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["detail"] == "Dog deleted"


def setup_module():
    user_data = {
        "id": 1,
        "email": "deadpool@example.com",
        "password": "chimichangas4life",
        "name": "deadpool",
        "contact_info": "somewhere"
    }

    dog_data = {
        "id": 1,
        "name": "Rocket",
        "breed": "Chanda",
        "owner_id": 1,
    }

    db = TestingSessionLocal()

    user = User(**user_data)
    dog = Dog(**dog_data)

    db.add(user)
    db.add(dog)

    db.commit()

    db.refresh(user)
    db.refresh(dog)

    db.close()


def teardown_module():
    db = TestingSessionLocal()
    user = db.query(User).first()
    db.delete(user)
    db.commit()
