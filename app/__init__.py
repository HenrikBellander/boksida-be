from flask import Flask
from .routes import books
from .user_routes import users
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(books) 
    app.register_blueprint(users) 
    return app

