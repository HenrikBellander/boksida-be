import pytest  # type: ignore
from app import create_app
from flask import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_connection(client):
    response = client.get('/api/')
    assert response.status_code == 200

def test_login(client):
    response = client.post(
        '/auth/login',
        data=json.dumps({'username': 'magkur1', 'password': '123'}),
        content_type='application/json',
    )
    assert response.status_code == 200
    cookies = response.headers.getlist("Set-Cookie")  
    token_cookie = next((c for c in cookies if "token=" in c), None)

    assert token_cookie is not None, "Token cookie was not set!"

def test_wrong_pw(client):
    response = client.post(
        '/auth/login',
        data = json.dumps({'username': 'magkur1', 'password': 'fail'}),
        content_type='application/json',
    )
    assert response.status_code == 401

def test_create_user(client):
    response = client.post(
        '/users/',
        data = json.dumps({'username': 'test-user', 'password': '123', 'email': '123'}),
        content_type='application/json',
    )
    print(response)
    assert response.status_code == 201

def test_get_all_users(client):
    response = client.get('/users/')
    users = response.json[0]
    assert any(user['username'] == 'test-user' for user in users)
    assert any(user['username'] == 'magkur6' for user in users)

# def test_update_user(client):
#     pass

# def test_delete_user(client):
#     pass