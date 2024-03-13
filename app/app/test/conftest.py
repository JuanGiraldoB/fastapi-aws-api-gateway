import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base
from app.main import app
from app.dependencies import get_db

# SQLALCHEMY_DATABASE_URL = "sqlite:///test.db"

# In memory database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def dog():
    return {
        "id": 1,
        "name": "Rocket",
        "breed": "Chanda",
        "owner_id": 1,
    }


@pytest.fixture()
def user():
    return {
        "id": 1,
        "email": "deadpool@example.com",
        "password": "chimichangas4life",
        "name": "deadpool",
        "contact_info": "somewhere"
    }
