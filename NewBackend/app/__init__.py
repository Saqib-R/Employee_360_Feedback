from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)

    with app.app_context():
        from . import routes
        routes.register_routes(app)

    return app
