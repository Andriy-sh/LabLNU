from fastapi.testclient import TestClient
from sqlmodel import Session
from datetime import datetime

def test_create_book(client: TestClient):
    book_data = {
        "title": "Test Book",
        "isbn": "1234567890",
        "publication_year": 2023,
        "copies_available": 5,
        "author_ids": [],
        "category_ids": []
    }
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["isbn"] == book_data["isbn"]
    assert data["publication_year"] == book_data["publication_year"]
    assert data["copies_available"] == book_data["copies_available"]

def test_get_book(client: TestClient):
    # First create a book
    book_data = {
        "title": "Test Book",
        "isbn": "1234567890",
        "publication_year": 2023,
        "copies_available": 5,
        "author_ids": [],
        "category_ids": []
    }
    create_response = client.post("/books/", json=book_data)
    created_book = create_response.json()
    
    response = client.get(f"/books/{created_book['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == book_data["title"]
    assert data["isbn"] == book_data["isbn"]

def test_get_book_not_found(client: TestClient):
    response = client.get("/books/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Book not found"

def test_get_books(client: TestClient):
    # Create multiple books
    books_data = [
        {
            "title": "Test Book 1",
            "isbn": "1234567890",
            "publication_year": 2023,
            "copies_available": 5,
            "author_ids": [],
            "category_ids": []
        },
        {
            "title": "Test Book 2",
            "isbn": "0987654321",
            "publication_year": 2022,
            "copies_available": 3,
            "author_ids": [],
            "category_ids": []
        }
    ]
    
    for book_data in books_data:
        client.post("/books/", json=book_data)
    
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= len(books_data)

def test_update_book(client: TestClient):
    # First create a book
    book_data = {
        "title": "Test Book",
        "isbn": "1234567890",
        "publication_year": 2023,
        "copies_available": 5,
        "author_ids": [],
        "category_ids": []
    }
    create_response = client.post("/books/", json=book_data)
    created_book = create_response.json()
    
    # Update the book
    update_data = {
        "title": "Updated Book",
        "isbn": "0987654321",
        "publication_year": 2022,
        "copies_available": 3,
        "author_ids": [],
        "category_ids": []
    }
    response = client.put(f"/books/{created_book['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == update_data["title"]
    assert data["isbn"] == update_data["isbn"]

def test_delete_book(client: TestClient):
    # First create a book
    book_data = {
        "title": "Test Book",
        "isbn": "1234567890",
        "publication_year": 2023,
        "copies_available": 5,
        "author_ids": [],
        "category_ids": []
    }
    create_response = client.post("/books/", json=book_data)
    created_book = create_response.json()
    
    # Delete the book
    response = client.delete(f"/books/{created_book['id']}")
    assert response.status_code == 200
    
    # Verify book is deleted
    get_response = client.get(f"/books/{created_book['id']}")
    assert get_response.status_code == 404