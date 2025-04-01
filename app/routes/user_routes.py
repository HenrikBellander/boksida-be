from flask import Blueprint, jsonify, request
from ..controllers.user_controller import (
    get_all_users,
    create_user,
    get_user_by_id_or_username,
    delete_user,
    update_user
)


users = Blueprint('users', __name__, url_prefix='/users')

@users.route('/', methods=['GET'])
def get_all_userss():
    users = get_all_users()
    return jsonify(users)

# @users.route('/user/<id>', methods=['GET'])
# def show_user(id):
#     user = get_user_by_id_or_username(id)
#     if user is None:
#         return jsonify({"error": "Användaren hittades inte"}), 404
#     return jsonify(user)

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

@users.route('/user/<id>', methods=['PUT'])
def update_user_route(id, username, password, email):
    user = update_user(id, username, password, email)
    if user is None:
        return jsonify({"error": "Användaren hittades inte"}), 404
    return jsonify(user)

# @users.route('/', methods=['POST'])
# def register_user():
#     data = request.get_json()
#     user = create_user(data.get('username'), data.get('password'), data.get('email'))
#     if user is None:
#         return jsonify({"error": "Något gick fel"}), 404
#     print(f'user: {user}')
#     return jsonify(), 200

@users.route('/', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    
    user, error = create_user(username, password, email)
    if error:
        return jsonify({"error": error}), 200
    
    #return jsonify({"message": "User created", "user": user}), 201
    return jsonify(user), 201