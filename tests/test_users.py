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
        'https://localhost:5000/auth/login',
        data = json.dumps({'username': 'magkur1', 'password': 'fail'}),
        content_type='application/json',
    )
    assert response.status_code == 401