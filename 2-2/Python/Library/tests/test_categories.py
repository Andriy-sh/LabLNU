from fastapi.testclient import TestClient
from sqlmodel import Session

def test_create_category(client: TestClient):
    category_data = {
        "name": "Fiction",
        "description": "Fiction books"
    }
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["description"] == category_data["description"]

def test_create_duplicate_category(client: TestClient):
    category_data = {
        "name": "Fiction",
        "description": "Fiction books"
    }
    # Create first category
    client.post("/categories/", json=category_data)
    
    # Try to create duplicate category
    response = client.post("/categories/", json=category_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Category already exists"

def test_get_category(client: TestClient):
    # First create a category
    category_data = {
        "name": "Fiction",
        "description": "Fiction books"
    }
    create_response = client.post("/categories/", json=category_data)
    created_category = create_response.json()
    
    response = client.get(f"/categories/{created_category['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["description"] == category_data["description"]

def test_get_category_not_found(client: TestClient):
    response = client.get("/categories/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Category not found"

def test_get_categories(client: TestClient):
    # Create multiple categories
    categories_data = [
        {
            "name": "Fiction",
            "description": "Fiction books"
        },
        {
            "name": "Non-Fiction",
            "description": "Non-fiction books"
        }
    ]
    
    for category_data in categories_data:
        client.post("/categories/", json=category_data)
    
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= len(categories_data)

def test_update_category(client: TestClient):
    # First create a category
    category_data = {
        "name": "Fiction",
        "description": "Fiction books"
    }
    create_response = client.post("/categories/", json=category_data)
    created_category = create_response.json()
    
    # Update the category
    update_data = {
        "name": "Updated Fiction",
        "description": "Updated fiction books"
    }
    response = client.put(f"/categories/{created_category['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]

def test_delete_category(client: TestClient):
    # First create a category
    category_data = {
        "name": "Fiction",
        "description": "Fiction books"
    }
    create_response = client.post("/categories/", json=category_data)
    created_category = create_response.json()
    
    # Delete the category
    response = client.delete(f"/categories/{created_category['id']}")
    assert response.status_code == 200
    
    # Verify category is deleted
    get_response = client.get(f"/categories/{created_category['id']}")
    assert get_response.status_code == 404