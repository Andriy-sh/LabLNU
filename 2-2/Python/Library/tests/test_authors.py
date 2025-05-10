from fastapi.testclient import TestClient
from sqlmodel import Session

def test_create_author(client: TestClient):
    author_data = {
        "first_name": "William",
        "last_name": "Shakespeare"
    }
    response = client.post("/authors/", json=author_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == author_data["first_name"]
    assert data["last_name"] == author_data["last_name"]
    assert "id" in data

def test_create_duplicate_author(client: TestClient):
    author_data = {
        "first_name": "William",
        "last_name": "Shakespeare"
    }
    # Create first author
    client.post("/authors/", json=author_data)
    
    # Try to create duplicate author
    response = client.post("/authors/", json=author_data)
    assert response.status_code == 400
    assert response.json()["detail"] == "Author already exists"

def test_get_author(client: TestClient):
    # First create an author
    author_data = {
        "first_name": "William",
        "last_name": "Shakespeare"
    }
    create_response = client.post("/authors/", json=author_data)
    created_author = create_response.json()
    
    # Then get the author
    response = client.get(f"/authors/{created_author['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == author_data["first_name"]
    assert data["last_name"] == author_data["last_name"]

def test_get_author_not_found(client: TestClient):
    response = client.get("/authors/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Author not found"

def test_get_authors(client: TestClient):
    # Create multiple authors
    authors_data = [
        {
            "first_name": "William",
            "last_name": "Shakespeare"
        },
        {
            "first_name": "Jane",
            "last_name": "Austen"
        }
    ]
    
    for author_data in authors_data:
        client.post("/authors/", json=author_data)
    
    response = client.get("/authors/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(authors_data)