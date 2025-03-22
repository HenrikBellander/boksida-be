from flask import Flask
from .routes import books

def create_app():
    app = Flask(__name__)
    app.register_blueprint(books)
    return app

