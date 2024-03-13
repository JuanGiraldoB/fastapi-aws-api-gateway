from fastapi.testclient import TestClient
from app.test.conftest import app
from fastapi import status

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == "Server is running"
