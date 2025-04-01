# basket_routes.py
from flask import Blueprint, jsonify, request
from .controllers.basket_controller import get_basket_items, add_item_to_basket, remove_item_from_basket

basket = Blueprint('basket', __name__)

@basket.route('/basket')
def get_basket_items():
    return {"message": "Basket endpoint"}

@basket.route('/basket/<id>', methods=['GET'])
def show_basket(id):
    """Visar en specifik användare."""
    basket = get_basket_items(id)
    if basket is None:
        return jsonify({"error": "Tom varukorg"}), 404
    return jsonify(basket)

@basket.route('/basket/<id>', methods=['DELETE'])
def del_item(id):
    """Ta bort en bok ur korgen."""
    basket = remove_item_from_basket(id)
    if basket is None:
        return jsonify({"error": "Boken hittades inte"}), 404
    return jsonify(basket)

@basket.route('/', methods=['POST'])
def new_item(user_id, book_id, quantity):
    """Addera bok i korgen."""
    basket = add_item_to_basket(user_id, book_id, quantity)
    if basket is None:
        return jsonify({"error": "Något gick fel"}), 404
    print(f'basket: {basket}')
    return jsonify(basket), 200