import jwt
import datetime
import os
import sqlite3
from flask import request, jsonify, make_response
from werkzeug.security import check_password_hash
from dotenv import load_dotenv
from config import Config

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')

if not SECRET_KEY:
    raise ValueError("No SECRET_KEY set in environment variables")

def get_db_connection():
    return sqlite3.connect(Config.DB_PATH)


def generate_token_response(user_id, username):
    token = generate_jwt(user_id, username)
    
    response = make_response(jsonify({
        'message': 'Login successful',
        'user': {
            'id': user_id,
            'username': username
        }
    }))
    
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

def verify_jwt():
    token = request.cookies.get('token')
    if not token:
        return None, "Missing token"
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return {
            'id': payload['id'],
            'username': payload['username'],
            'exp': payload['exp']
        }, None
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"
    
def generate_jwt(user_id, username):
    payload = {
        "id": user_id,
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
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
            
        if not check_password_hash(user[2], password):
            return None, "Incorrect password"
            
        token = generate_jwt(user[0], user[1])
        return token, None
        
    except Exception as e:
        return None, f"Database error: {str(e)}"
    finally:
        conn.close()