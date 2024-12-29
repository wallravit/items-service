import pytest
from httpx import AsyncClient
from items_api.main import app


@pytest.mark.asyncio
async def test_create_item():
    # Valid item creation
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/items",
            json={"name": "Test Item", "description": "This is a test item."},
        )
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"

    # Fail: Missing required fields
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/items", json={"description": "Missing name"})
    assert response.status_code == 422  # Unprocessable Entity

    # Fail: Empty payload
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/items", json={})
    assert response.status_code == 422  # Unprocessable Entity

    # Fail: Invalid payload type
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/items", json="Invalid payload")
    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_list_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/items")
        if len(response.json()) > 0:
            for item in response.json():
                await ac.delete(f"/api/v1/items/{item['id']}")
        empty_response = await ac.get("/api/v1/items")
    assert empty_response.status_code == 200
    assert len(empty_response.json()) == 0  # List should be empty


@pytest.mark.asyncio
async def test_get_item_by_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post(
            "/api/v1/items",
            json={"name": "Test Item", "description": "This is a test item."},
        )
        item_id = create_response.json()["id"]

        response = await ac.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/items/99999")  # Non-existent ID
    assert response.status_code == 404  # Not Found

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/api/v1/items/invalid-id")
    assert response.status_code == 422  # Unprocessable Entity


@pytest.mark.asyncio
async def test_update_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post(
            "/api/v1/items", json={"name": "Old Name", "description": "Old description"}
        )
        item_id = create_response.json()["id"]

        update_response = await ac.put(
            f"/api/v1/items/{item_id}",
            json={"name": "Updated Name", "description": "Updated description"},
        )
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "Updated Name"

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(
            "/api/v1/items/99999",
            json={"name": "Non-existent", "description": "This should fail"},
        )
    assert response.status_code == 404

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.put(f"/api/v1/items/{item_id}", json={"invalid": "data"})
    assert response.status_code == 422 


@pytest.mark.asyncio
async def test_delete_item():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        create_response = await ac.post(
            "/api/v1/items",
            json={"name": "To Be Deleted", "description": "This will be deleted."},
        )
        item_id = create_response.json()["id"]

        delete_response = await ac.delete(f"/api/v1/items/{item_id}")
        assert delete_response.status_code == 200

        get_response = await ac.get(f"/api/v1/items/{item_id}")
        assert get_response.status_code == 404

    # Fail: Delete non-existent item
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.delete("/api/v1/items/99999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_item_endpoints_with_large_payload():
    large_description = "x" * 10000
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/api/v1/items",
            json={"name": "Large Payload", "description": large_description},
        )
    assert response.status_code == 201
    assert response.json()["description"] == large_description

    item_id = response.json()["id"]
    async with AsyncClient(app=app, base_url="http://test") as ac:
        get_response = await ac.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 200
    assert get_response.json()["description"] == large_description
