import os
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ["DATABASE_URL"] = "sqlite:///./test_careerpath.db"

from app.database import init_db, engine, Base, SessionLocal  # noqa: E402
from app.seed.seeder import run_seed  # noqa: E402
from app.main import app  # noqa: E402


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    init_db()
    run_seed()
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        os.remove("test_careerpath.db")
    except OSError:
        pass


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture()
def auth_client(client):
    """A client authenticated as a fresh test user."""
    import random
    suffix = random.randint(100000, 999999)
    resp = client.post("/api/v1/auth/register", json={
        "email": f"test{suffix}@example.com",
        "username": f"tester{suffix}",
        "password": "Passw0rd123",
        "full_name": "Test User",
    })
    assert resp.status_code == 200, resp.text
    token = resp.json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture()
def career_id():
    return 1  # AI/ML Engineer seeded first


@pytest.fixture()
def selected_auth_client(auth_client, career_id):
    resp = auth_client.put("/api/v1/auth/me", json={"selected_career_id": career_id})
    assert resp.status_code == 200
    return auth_client
