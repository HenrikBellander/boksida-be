import pytest
from app.routes.basket_routes import basket
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# ----------------------------
# Tests for the POST /api/basket route (adding an item)
# ----------------------------

def test_new_item_success(client, monkeypatch):
    # Patch the function in the routes module
    monkeypatch.setattr(
        "app.routes.basket_routes.add_item_to_basket",
        lambda user_id, book_id, quantity: 123
    )
    payload = {"user_id": 3, "book_id": 10, "quantity": 2}
    response = client.post("/api/basket", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "basket_id" in data
    # Expect 123 as per our monkeypatch
    assert data["basket_id"] == 123

def test_new_item_failure(client, monkeypatch):
    # Simulate failure by returning a falsy value
    monkeypatch.setattr(
        "app.routes.basket_routes.add_item_to_basket",
        lambda user_id, book_id, quantity: None
    )
    payload = {"user_id": 3, "book_id": 10, "quantity": 2}
    response = client.post("/api/basket", json=payload)
    # When add_item_to_basket returns None, the route returns 400
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

# ----------------------------
# Tests for the DELETE /api/basket/<int:book_id> route (removing an item)
# ----------------------------

def test_del_item_success(client, monkeypatch):
    # Patch removal function in the routes module
    monkeypatch.setattr(
        "app.routes.basket_routes.remove_item_from_basket",
        lambda user_id, book_id: True
    )
    # Provide the user_id query parameter
    response = client.delete("/api/basket/10?user_id=3")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("message") == "Book removed from basket"

def test_del_item_failure(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.basket_routes.remove_item_from_basket",
        lambda user_id, book_id: False
    )
    response = client.delete("/api/basket/10?user_id=3")
    # When removal returns False, the route returns 404
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

# ----------------------------
# Tests for the GET /api/basket/<int:user_id> route (showing the basket)
# ----------------------------

def test_show_basket_success(client, monkeypatch):
    dummy_items = [
        {"book_price": "10.5", "book_title": "Book A", "book_category": "Fiction"},
        {"book_price": "20", "book_title": "Book B", "book_category": "Non-fiction"}
    ]
    monkeypatch.setattr(
        "app.routes.basket_routes.get_basket_items",
        lambda user_id: dummy_items
    )
    response = client.get("/api/basket/3")
    assert response.status_code == 200
    data = response.get_json()
    assert "basket_items" in data
    assert "total" in data
    # The total should be 10.5 + 20 = 30.5
    assert data["total"] == 30.5

def test_show_basket_empty(client, monkeypatch):
    monkeypatch.setattr(
        "app.routes.basket_routes.get_basket_items",
        lambda user_id: []
    )
    response = client.get("/api/basket/3")
    # When the basket is empty, the route returns 404
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data