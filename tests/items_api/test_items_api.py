# pylint: skip-file

import pytest
from httpx import AsyncClient
from items_api.main import app

@pytest.mark.asyncio
async def test_create_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/items", json={"name": "Test Item", "description": "This is a test item."})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"

@pytest.mark.asyncio
async def test_get_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_get_item_by_id():
    # Create an item first
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post("/api/v1/items", json={"name": "Test Item", "description": "This is a test item."})
        item_id = create_response.json()["id"]

        # Fetch the item by ID
        response = await ac.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

@pytest.mark.asyncio
async def test_update_item():
    # Create an item first
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post("/api/v1/items", json={"name": "Old Name", "description": "Old description"})
        item_id = create_response.json()["id"]

        # Update the item
        update_response = await ac.put(f"/api/v1/items/{item_id}", json={"name": "New Name", "description": "New description"})
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "New Name"

@pytest.mark.asyncio
async def test_delete_item():
    # Create an item first
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post("/api/v1/items", json={"name": "To Be Deleted", "description": "Will be deleted"})
        item_id = create_response.json()["id"]

        # Delete the item
        delete_response = await ac.delete(f"/api/v1/items/{item_id}")
        assert delete_response.status_code == 200

        # Verify the item is deleted
        get_response = await ac.get(f"/api/v1/items/{item_id}")
        assert get_response.status_code == 404
