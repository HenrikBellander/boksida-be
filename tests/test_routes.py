import pytest
from flask.testing import FlaskClient
from run import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    return app.test_client()

def test_get_categories_route(client: FlaskClient):
    """Testar att få alla kategorier"""
    response = client.get('/api/')
    assert response.status_code == 200
    assert isinstance(response.json, list)

    categories = [item["book_category"] for item in response.json]
    assert "Travel" in categories
    assert "Fiction" in categories

def test_show_books_by_category_route(client: FlaskClient):
    """Testar boklistning per kategori"""
    response = client.get('/api/category/Fiction')
    assert response.status_code == 200
    assert isinstance(response.json, list)  
    assert len(response.json) > 0 

def test_search_route(client: FlaskClient):
    """Testar sökfunktionalitet"""
    response = client.get('/api/search?q=Most Wanted')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    if len(response.json) > 0: 
        assert response.json[0]["book_title"] == "Most Wanted"

def test_book_detail_route(client: FlaskClient):
    """Testar bokdetaljer"""
    response = client.get('/api/book/1')
    assert response.status_code == 200
    assert response.json["book_title"] == "It's Only the Himalayas"
    assert response.json["book_category"] == "Travel"

def test_book_detail_route_not_found(client: FlaskClient):
    """Testar 404-hantering"""
    response = client.get('/api/book/999')
    assert response.status_code == 404
    assert response.json["error"] == "Boken hittades inte"