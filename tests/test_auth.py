import pytest
import jwt
import datetime
from unittest.mock import patch, MagicMock
from app.controllers.auth_controller import verify_jwt, SECRET_KEY

@pytest.fixture
def valid_token():
    payload = {"id": 1, "username": "testuser", "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def expired_token():
    payload = {"id": 1, "username": "testuser", "exp": datetime.datetime.utcnow() - datetime.timedelta(hours=1)}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@pytest.fixture
def invalid_token():
    return "invalid.jwt.token"

def test_verify_jwt_valid_token(valid_token):
    mock_request = MagicMock()
    mock_request.cookies.get.return_value = valid_token
    
    with patch('app.controllers.auth_controller.request', mock_request):
        payload, error = verify_jwt()
        assert error is None
        assert payload["id"] == 1
        assert payload["username"] == "testuser"
        assert "exp" in payload

def test_verify_jwt_missing_token():
    mock_request = MagicMock()
    mock_request.cookies.get.return_value = None
    
    with patch('app.controllers.auth_controller.request', mock_request):
        payload, error = verify_jwt()
        assert payload is None
        assert error == "Missing token"

def test_verify_jwt_expired_token(expired_token):
    mock_request = MagicMock()
    mock_request.cookies.get.return_value = expired_token
    
    with patch('app.controllers.auth_controller.request', mock_request):
        payload, error = verify_jwt()
        assert payload is None
        assert error == "Token expired"

def test_verify_jwt_invalid_token(invalid_token):
    mock_request = MagicMock()
    mock_request.cookies.get.return_value = invalid_token
    
    with patch('app.controllers.auth_controller.request', mock_request):
        payload, error = verify_jwt()
        assert payload is None
        assert error == "Invalid token"
