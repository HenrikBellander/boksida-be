from flask import Blueprint, jsonify, request
from app.controllers.basket_controller import (
    get_basket_items,
    add_item_to_basket,
    remove_item_from_basket
)

basket = Blueprint('basket', __name__)

@basket.route('/api/basket', methods=['POST'])
def new_item():
    data = request.get_json()
    user_id = data.get('user_id')
    book_id = data.get('book_id')
    quantity = data.get('quantity', 1)
    new_basket_id = add_item_to_basket(user_id, book_id, quantity)
    if new_basket_id:
        return jsonify({"basket_id": new_basket_id}), 200
    return jsonify({"error": "Something went wrong"}), 400

@basket.route('/api/basket/<int:book_id>', methods=['DELETE'])
def del_item(book_id):
    # Retrieve the user_id from the query parameters.
    user_id = request.args.get('user_id', type=int)
    if user_id is None:
        return jsonify({"error": "User id is required"}), 400
    result = remove_item_from_basket(user_id, book_id)
    if result:
        return jsonify({"message": "Book removed from basket"}), 200
    return jsonify({"error": "Book not found in basket"}), 404

@basket.route('/api/basket/<int:user_id>', methods=['GET'])
def show_basket(user_id):
    basket_items = get_basket_items(user_id)
    if not basket_items:
        return jsonify({"error": "Empty basket"}), 404
    total = sum(float(item['book_price']) for item in basket_items)
    return jsonify({"basket_items": basket_items, "total": total})