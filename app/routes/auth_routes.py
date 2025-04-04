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
        secure=False,
        samesite='Lax',
        max_age=86400,
        path='/',
        domain=None
    )
    
    return response

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