from fastapi.testclient import TestClient
from sqlmodel import Session

def test_create_user(client: TestClient):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_create_user_duplicate_email(client: TestClient):
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    # Create first user
    client.post("/users/", json=user_data)
    
    # Try to create user with same email
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"

def test_get_user(client: TestClient):
    # First create a user
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    }
    create_response = client.post("/users/", json=user_data)
    created_user = create_response.json()
    
    # Then get the user
    response = client.get(f"/users/{created_user['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == user_data["first_name"]
    assert data["last_name"] == user_data["last_name"]
    assert data["email"] == user_data["email"]

def test_get_user_not_found(client: TestClient):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_users(client: TestClient):
    # Create multiple users
    users_data = [
        {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        },
        {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }
    ]
    
    for user_data in users_data:
        client.post("/users/", json=user_data)
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(users_data)