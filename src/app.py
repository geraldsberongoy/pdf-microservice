from flask import Flask
from flask_cors import CORS
from src.config.firebase import init_firebase
from src.routes.api import api_bp
from src.extensions import limiter

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes
    
    # Initialize Extensions
    limiter.init_app(app)
    
    # Initialize Firebase
    init_firebase()
    
    # Register Blueprints
    app.register_blueprint(api_bp)
    
    return app
