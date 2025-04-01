from flask import Flask, jsonify
from .routes import books
from .user_routes import users
from .basket_routes import basket # the file where your basket endpoint is defined
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)    
    
    # Registrera blueprints med eventuella URL-prefix
    app.register_blueprint(books, url_prefix='/api')
    app.register_blueprint(users, url_prefix='/api/users')
    app.register_blueprint(basket)  # registers the basket endpoint

    
    # Definiera en route för rot-URL ("/")
    @app.route('/')
    def index():
        return jsonify({"message": "Välkommen till API!"})
    
    return app
