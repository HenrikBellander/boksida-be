from flask import Flask

from .routes.auth_routes import auth
from .routes.book_routes import books
from .routes.user_routes import users
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    #CORS(app)
    #CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})
    CORS(app, 
     origins=["http://localhost:5173"], 
     supports_credentials=True,
     allow_headers=["Content-Type", "Authorization"]),
     
    

    app.register_blueprint(auth)
    app.register_blueprint(books) 
    app.register_blueprint(users)
    
    return app

