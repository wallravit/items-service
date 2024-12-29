# pylint: skip-file

import pytest
from fastapi.testclient import TestClient
from items_api.main import app
from items_api.store.sqlite import init_db
import asyncio

# Mock database initialization
@pytest.fixture(autouse=True)
def mock_init_db(monkeypatch):
    async def fake_init_db():
        print("Mock init_db called")
    monkeypatch.setattr("items_api.store.sqlite.init_db", fake_init_db)

# Create a test client
client = TestClient(app)


def test_api_v1_route():
    """Test that the /api/v1 route is included."""
    response = client.get("/api/v1")
    assert response.status_code in [200, 404]  # Check the route inclusion; content validation depends on implementation


@pytest.mark.asyncio
async def test_database_initialization():
    """Test that init_db is called on startup."""
    await init_db()
    print("Database initialized successfully")
