from flask import Blueprint, jsonify, request, make_response
from ..controllers.user_controller import verify_user
from ..controllers.auth_controller import authenticate_user, verify_jwt, generate_jwt
from datetime import datetime, timedelta
from functools import wraps

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    token, error = authenticate_user(username, password)
    if error:
        return jsonify({"error": error}), 401
    
    #response = jsonify({"message": "Login successful"})
    response = jsonify({
        "status": "success",
        "message": "Login successful",
        "data": None
    })
    # response.set_cookie('token', token, httponly=True, secure=True)
    response.set_cookie(
        'token',
        token,
        httponly=True,
        secure=True,
        samesite='Lax',
        max_age=86400,  # 24h
        path='/'
    )
    return response

# @auth.route('/verify', methods=['GET'])
# def verify():
#     user_data, error = verify_jwt()
#     if error:
#         return jsonify({"error": error}), 401
#     #return jsonify({"user": user_data})
#     return jsonify({
#         "status": "success",
#         "data": {"user": user_data}
#     })
@auth.route('/verify', methods=['GET'])
def verify():
    user_data, error = verify_jwt()
    if error:
        return jsonify({
            "status": "error",
            "message": error
        }), 401
        
    return jsonify({
        "status": "success",
        "data": {
            "user": {
                "id": user_data["id"],
                "username": user_data["username"]
            }
        }
    })

# @auth.route("/logout", methods=["POST"])
# def logout():
#     response = make_response(jsonify({"message": "Logged out"}))
#     response.set_cookie(
#         "token",
#         "",
#         expires=datetime.utcnow() - timedelta(seconds=3600),
#         httponly=True,
#         secure=False,
#         path="/",
#     )
#     return response, 200

@auth.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({
        "status": "success",
        "message": "Logged out"
    }))
    response.set_cookie(
        "token",
        "",
        expires=0,
        httponly=True,
        secure=True,
        samesite='Lax',
        path='/'
    )
    return response

@auth.route("/me", methods=["GET"])
def get_current_user():
    user, error = verify_jwt()
    if error:
        return jsonify({"error": error}), 401
    #return jsonify({"user": user}), 200
    return jsonify({
        "status": "success",
        "data": {"user": user}
    })

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
            
        try:
            user = verify_jwt(token)
            if not user:
                return jsonify({'message': 'Token is invalid'}), 401
        except Exception as e:
            return jsonify({'message': str(e)}), 401
            
        return f(user, *args, **kwargs)
    return decorated

