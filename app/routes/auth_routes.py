from flask import Blueprint, jsonify, request, make_response
from ..controllers.auth_controller import authenticate_user, get_db_connection, verify_jwt
from functools import wraps

auth = Blueprint("auth", __name__)

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Username and password required",
            "data": None
        }), 400
    
    token, error = authenticate_user(username, password)
    if error:
        return jsonify({
            "status": "error",
            "message": error,
            "data": None
        }), 401
    
    # Get complete user data from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT user_id, username, email FROM users WHERE username = ?", 
        (username,)
    )
    user = cursor.fetchone()
    conn.close()
    
    response = jsonify({
        "status": "success",
        "message": "Login successful",
        "data": {
            "user": {
                "id": user[0],
                "username": user[1],
                "email": user[2] if len(user) > 2 else None
            }
        }
    })
    
    response.set_cookie(
        'token',
        token,
        httponly=True,
        secure=False,  # True in production (HTTPS)
        samesite='Lax',
        max_age=86400,  # 24h
        path='/',
        domain=None  # Current domain only
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
        return jsonify({"status": "error", "message": error}), 401
        
    return jsonify({
        "status": "success",
        "message": "Authenticated",
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
        secure=True,    # True in production
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

# Example protected route
# @app.route('/protected')
# @token_required
# def protected_route(current_user):
#     return jsonify({'message': f'Hello {current_user.username}'})


# Is this needed for the ProtectedRoute.jsx to function???
# from functools import wraps

# def protected_route(fn):
#     @wraps(fn)
#     def wrapper(*args, **kwargs):
#         try:
#             verify_jwt_in_request()  # Verifierar JWT
#             current_user = get_jwt_identity()
#             return fn(current_user, *args, **kwargs)
#         except:
#             return jsonify({"msg": "Ogiltig token"}), 401
#     return wrapper

# @app.route('/api/me', methods=['GET'])
# @protected_route
# def get_current_user(current_user):
#     user_data = users.get(current_user, None)
#     if not user_data:
#         return jsonify({"msg": "Användare hittades inte"}), 404
#     return jsonify({
#         "username": current_user,
#         "role": user_data['role']
#     })