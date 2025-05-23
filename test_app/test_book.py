from fastapi.testclient import TestClient
from main import app
from schemas.book import BookCreate, BookUpdate
import uuid

client = TestClient(app)

def test_get_books():
    response = client.get("/books")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_add_book():
    payload = BookCreate(
        title = "Johny bravo",
        author = "John Doe",
        year = 2023,
        pages = 500,
        language = "English"
    ).model_dump()

    response = client.post("/books", json=payload)
    data = response.json()
    assert data["message"] == "Book added successfully"
    assert data["data"]["title"] == "Johny bravo"


def test_get_book_by_id():
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 200
    assert get_book_data['id'] == book_id


def test_get_book_by_id_not_found():
    book_id = 1
    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()
    assert get_response.status_code == 404
    assert get_book_data['detail'] == "book not found."


def test_update_book():
    payload = BookCreate(
        title = "Johny bravo",
        author = "John Doe",
        year = 2023,
        pages = 500,
        language = "English"
    ).model_dump()

    updated_payload = BookUpdate(
        title = "Samurai Jack",
        author = "John Doe",
        year = 2023,
        pages = 500,
        language = "English"
    ).model_dump()

    
    response = client.post("/books", json=payload)
    add_book_data = response.json()
    book_id = add_book_data['data']['id']

    get_response = client.get(f"/books/{book_id}")
    get_book_data = get_response.json()

    put_response = client.put(f"/books/{book_id}", json= updated_payload)
    update_book_data = put_response.json()

    assert get_book_data['id'] == book_id
    assert put_response.status_code == 200
    assert update_book_data['message'] == "Book updated successfully"
    assert update_book_data['data']['title'] == 'Samurai Jack'


def test_update_book_by_id_not_found():
    book_id = uuid.uuid4()
    payload = {
        "title": "Johny bravo",
        "author": "John Doe",
        "year": 2023,
        "pages": 500,
        "language": "English"
    }
    put_response = client.put(f"/books/{book_id}", json=payload)
    update_book_data = put_response.json()
    
    assert put_response.status_code == 404
    assert update_book_data['detail'] == f"Book with id: {book_id} not found"

def test_delete_book():
    book_id = uuid.uuid4()
    # Create the book
    payload = BookCreate(
        title = "Johny bravo",
        author = "John Doe",
        year = 2023,
        pages = 500,
        language = "English"
    ).model_dump()
    
    
    response = client.post(f"/books/", json=payload)
    post_book_data = response.json()
    book_id = post_book_data['data']['id']

    # Delete the book
    delete_response = client.delete(f"/books/{book_id}")
    delete_book_data = delete_response.json()

    assert delete_response.status_code == 200
    assert delete_book_data['message'] == "Book deleted successfully"

def test_delete_book_by_id_not_found():
    book_id = uuid.uuid4()
    
    delete_response = client.delete(f"/books/{book_id}")
    update_book_data = delete_response.json()
    
    assert delete_response.status_code == 404
    assert update_book_data['detail'] == f"Book with id: {book_id} not found"

      
    


