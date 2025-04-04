from flask import Flask
from .routes.basket_routes import basket # the file where your basket endpoint is defined
from .routes.auth_routes import auth
from .routes.book_routes import books
from .routes.user_routes import users
from .routes.team_routes import team_bp
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app, 
    resources={r"/*": {"origins": "http://localhost:5173"}},
    supports_credentials=True,
    expose_headers=["Set-Cookie"])

    app.register_blueprint(team_bp)
    app.register_blueprint(auth)
    app.register_blueprint(books) 
    app.register_blueprint(users)
    app.register_blueprint(basket)
    
    return app