from flask import Flask, jsonify
from .basket_routes import basket # the file where your basket endpoint is defined
from .routes.auth_routes import auth
from .routes.book_routes import books
from .routes.user_routes import users
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, 
    resources={r"/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True,
    expose_headers=["Set-Cookie"])

    app.register_blueprint(auth)
    app.register_blueprint(books) 
    app.register_blueprint(users)
    app.register_blueprint(basket)  # registers the basket endpoint
    
    return app