# pylint: skip-file

from starlette.testclient import TestClient
from items_api.main import app

client = TestClient(app)

def test_create_item():
    response = client.post("/api/v1/items", json={"name": "Test Item", "description": "This is a test item."})
    assert response.status_code == 201
    assert response.json()["name"] == "Test Item"

def test_get_items():
    response = client.get("/api/v1/items")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_item_by_id():
    # Create an item first
    create_response = client.post("/api/v1/items", json={"name": "Test Item", "description": "This is a test item."})
    item_id = create_response.json()["id"]

    # Fetch the item by ID
    response = client.get(f"/api/v1/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["id"] == item_id

def test_update_item():
    # Create an item first
    create_response = client.post("/api/v1/items", json={"name": "Old Name", "description": "Old description"})
    item_id = create_response.json()["id"]

    # Update the item
    update_response = client.put(f"/api/v1/items/{item_id}", json={"name": "New Name", "description": "New description"})
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "New Name"

def test_delete_item():
    # Create an item first
    create_response = client.post("/api/v1/items", json={"name": "To Be Deleted", "description": "Will be deleted"})
    item_id = create_response.json()["id"]

    # Delete the item
    delete_response = client.delete(f"/api/v1/items/{item_id}")
    assert delete_response.status_code == 200

    # Verify the item is deleted
    get_response = client.get(f"/api/v1/items/{item_id}")
    assert get_response.status_code == 404
