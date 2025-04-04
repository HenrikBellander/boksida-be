import pytest
from flask import Flask
from app.routes.basket_routes import basket  # Import the blueprint from app/basket_routes.py
from app import create_app

# Create a Flask application fixture and register the basket blueprint.
# @pytest.fixture
# def app():
#     app = Flask(__name__)
#     app.register_blueprint(basket)
#     return app

# # Create a test client fixture.
# @pytest.fixture
# def client(app):
#     return app.test_client()

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
    # Monkeypatch add_item_to_basket to simulate a successful addition (returning a dummy basket id)
    monkeypatch.setattr(
        "app.controllers.basket_controller.add_item_to_basket",
        lambda user_id, book_id, quantity: 123
    )
    payload = {"user_id": 3, "book_id": 10, "quantity": 2}
    response = client.post("/api/basket", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "basket_id" in data
    assert data["basket_id"] == 123

def test_new_item_failure(client, monkeypatch):
    # Simulate failure by having add_item_to_basket return a falsy value (None)
    monkeypatch.setattr(
        "app.controllers.basket_controller.add_item_to_basket",
        lambda user_id, book_id, quantity: None
    )
    payload = {"user_id": 3, "book_id": 10, "quantity": 2}
    response = client.post("/api/basket", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

# ----------------------------
# Tests for the DELETE /api/basket/<int:book_id> route (removing an item)
# ----------------------------

def test_del_item_success(client, monkeypatch):
    # Simulate successful removal by having remove_item_from_basket return True.
    monkeypatch.setattr(
        "app.controllers.basket_controller.remove_item_from_basket",
        lambda user_id, book_id: True
    )
    response = client.delete("/api/basket/10")
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("message") == "Book removed from basket"

def test_del_item_failure(client, monkeypatch):
    # Simulate failure by having remove_item_from_basket return False.
    monkeypatch.setattr(
        "app.controllers.basket_controller.remove_item_from_basket",
        lambda user_id, book_id: False
    )
    response = client.delete("/api/basket/10")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data

# ----------------------------
# Tests for the GET /api/basket/<int:user_id> route (showing the basket)
# ----------------------------

def test_show_basket_success(client, monkeypatch):
    # Prepare dummy basket items.
    dummy_items = [
        {"book_price": "10.5", "book_title": "Book A", "book_category": "Fiction"},
        {"book_price": "20", "book_title": "Book B", "book_category": "Non-fiction"}
    ]
    # Monkeypatch get_basket_items to return the dummy items.
    monkeypatch.setattr(
        "app.controllers.basket_controller.get_basket_items",
        lambda user_id: dummy_items
    )
    response = client.get("/api/basket/3")
    assert response.status_code == 200
    data = response.get_json()
    assert "basket_items" in data
    assert "total" in data
    # Total should equal 10.5 + 20 = 30.5 after converting to float.
    assert data["total"] == 30.5

def test_show_basket_empty(client, monkeypatch):
    # Simulate an empty basket by returning an empty list.
    monkeypatch.setattr(
        "app.controllers.basket_controller.get_basket_items",
        lambda user_id: []
    )
    response = client.get("/api/basket/3")
    assert response.status_code == 404
    data = response.get_json()
    assert "error" in data