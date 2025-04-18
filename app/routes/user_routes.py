from flask import Blueprint, jsonify, request
from ..controllers.user_controller import (
    get_all_users,
    create_user,
    get_user_by_id_or_username,
    delete_user,
    update_user,
    delete_user_name,
    update_user_username
)

users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['GET'])
def get_all_userss():
    users = get_all_users()
    return jsonify(users)

@users.route('/user/<identifier>', methods=['GET'])
def show_user(identifier):
    if identifier.isdigit():
        user, error = get_user_by_id_or_username(user_id=identifier)
    else:
        user, error = get_user_by_id_or_username(username=identifier)
    
    if error:
        return jsonify({"error": error}), 404
    return jsonify(user)


@users.route('/user/<id>', methods=['DELETE'])
def del_user(id):
    user = delete_user(id)
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

@users.route('/username/<name>', methods=['DELETE'])
def del_user_name(name):
    user = delete_user_name(name)
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

@users.route('/user/<id>', methods=['PUT'])
def update_user_route(id):
    data = request.json
    user = update_user(id, {'username': data.get('username'), 'password': data.get('password'), 'email': data.get('email')})
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)


@users.route('/username/<name>', methods=['PUT'])
def update_user_username_route(name):
    data = request.json
    user = update_user_username(name, {'username': data.get('username'), 'password': data.get('password'), 'email': data.get('email')})
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

@users.route('/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    user, error = create_user(username, password, email)
    if error:
        return jsonify({"error": error}), 400
    
    return jsonify({"message": "User created", "user": user}), 201