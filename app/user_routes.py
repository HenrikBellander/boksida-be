from flask import Blueprint, jsonify, request
from .controllers.user_controller import get_users, get_single_user, delete_user, add_user, update_user

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['GET'])
def get_all_users():
    """Hämtar alla användare från databasen och returnerar som JSON."""
    users = get_users()
    return jsonify(users)

@users.route('/user/<id>', methods=['GET'])
def show_user(id):
    """Visar en specifik användare."""
    user = get_single_user(id)
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

@users.route('/user/<id>', methods=['DELETE'])
def del_user(id):
    """Ta bort en användare."""
    user = delete_user(id)
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

@users.route('/user/<id>', methods=['PUT'])
def update_user_route(id, username, password):
    """Uppdatera en användare."""
    user = update_user(id, username, password)
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

@users.route('/', methods=['POST'])
def new_user(username, password):
    """Skapa en ny användare."""
    user = add_user(username, password)
    if user is None:
        return jsonify({"error": "Något gick fel"}), 404
    return jsonify(user)



