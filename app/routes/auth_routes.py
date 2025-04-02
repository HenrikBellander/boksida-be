import jwt
import datetime
import os
import sqlite3
from flask import Blueprint, jsonify, make_response, request
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from config import Config
import time
print(f"System time: {time.time()}")
print(f"UTC now: {datetime.datetime.utcnow()}")

load_dotenv()

auth = Blueprint("auth", __name__, url_prefix='/auth')

SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables")


def get_db_connection():
    return sqlite3.connect(Config.DB_PATH)


def generate_jwt(user_id, username):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    print(f"UTC now: {datetime.datetime.utcnow()}")
    print(f"Expires at: {expiration_time}")
    
    payload = {
        "id": user_id,
        "username": username,
        "exp": expiration_time,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    print(f"Token generated at: {datetime.datetime.utcnow()}")
    return token

def authenticate_user(username, password):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT user_id, username, password FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        
        if not user:
            return None, "User not found"
            
        if not check_password_hash(user[2], password):  # user[2] = password_hash
            return None, "Incorrect password"
            
        token = generate_jwt(user[0], user[1])  # user[0] = id, user[1] = username
        return token, None
        
    except Exception as e:
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()

def verify_jwt():
    token = request.cookies.get("token")
    if not token:
        return None, "Missing token"
    
    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=["HS256"],
            options={'require_exp': True}  # Tvingar verifiering av exp
        )
        print(f"Current UTC: {datetime.datetime.utcnow()}")
        print(f"Token expires at: {datetime.datetime.fromtimestamp(payload['exp'])}")
        return {"id": payload["id"], "username": payload["username"]}, None
    except jwt.ExpiredSignatureError as e:
        print(f"Token expired at: {e.expired_at}")
        return None, "Token expired"
    except Exception as e:
        print(f"JWT Error: {str(e)}")
        return None, f"Token error: {str(e)}"



@auth.route('/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({
            "status": "error",
            "message": "Content-Type must be application/json"
        }), 415

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({
            "status": "error",
            "message": "Both username and password are required"
        }), 400

    token, error = authenticate_user(username, password)
    if error:
        return jsonify({
            "status": "error",
            "message": error
        }), 401

    response_data = {
        "status": "success",
        "message": "Login successful",
        "data": {
            "token": token,
            "user": {
                "username": username
            }
        }
    }

    response = jsonify(response_data)
    
    response.set_cookie(
        key='token',
        value=token,
        httponly=True,
        secure=False,  
        samesite='Strict',
        max_age=3600 
    )
    
    return response

@auth.route('/verify', methods=['GET'])
def verify():
    user_data, error = verify_jwt()
    if error:
        return jsonify({"error": error}), 401
    return jsonify({
        "status": "success",
        "data": {"user": user_data}
    })

@auth.route("/logout", methods=["POST"])
def logout():
    response = make_response(jsonify({
        "status": "success",
        "message": "Logged out"
    }))
    response.delete_cookie('token')
    return response

@auth.route('/me', methods=['GET'])
def get_current_user():
    token = request.cookies.get('token')
    if not token:
        return jsonify({"error": "Unauthorized"}), 401
    
    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT user_id, username FROM users WHERE user_id = ?", (data['id'],))
        user = cursor.fetchone()
        conn.close()
        
        if not user:
            return jsonify({"error": "User not found"}), 404
            
        return jsonify({
            "user": {
                "id": user[0],
                "username": user[1]
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 401

