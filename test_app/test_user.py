from fastapi.testclient import TestClient
from main import app
from schemas.user import UserCreate, UserUpdate
from uuid import uuid4



client = TestClient(app)


def test_create_user():
    payload = UserCreate(
        name="Alice", 
        email="alice@example.com", 
        age=30).model_dump()

    response = client.post("/users", json=payload)
    data = response.json()
    assert response.status_code == 200
    assert data['message'] == "User created successfully"
    assert data['data']['name'] == "Alice"

def test_get_user():
    payload = UserCreate(
        name="Bob", 
        email="bob@example.com", 
        age=25).model_dump()
    
    response = client.post("/users", json=payload)
    user_id = response.json()['data']['id']

    get_response = client.get(f"/users/{user_id}")

    print(response.json())
    assert get_response.status_code == 200
    assert get_response.json()['data']['email'] == "bob@example.com"

def test_update_user():
    payload = UserCreate(
        name="Carol", 
        email="carol@example.com", 
        age=40).model_dump()
    
    response = client.post("/users", json=payload)
    user_id = response.json()['data']['id']

    update_payload = UserUpdate(
        name="Carol Updated", 
        email="carol_new@example.com", 
        age=41).model_dump()
    
    put_response = client.put(f"/users/{user_id}", json=update_payload)
    data = put_response.json()
    assert put_response.status_code == 200
    assert data['data']['name'] == "Carol Updated"

def test_delete_user():
    payload = UserCreate(
        name="Dave", 
        email="dave@example.com", 
        age=50).model_dump()
    
    response = client.post("/users", json=payload)
    user_id = response.json()['data']['id']

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()['message'] == "User deleted successfully"


def test_get_user_not_found():
    fake_id = uuid4()
    response = client.get(f"/users/{fake_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == f"User with id: {fake_id} not found"