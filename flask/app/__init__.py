from flask import Flask

from config import Config
from app.extensions import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)

    from app.blueprints.front import bp as frontend_bp
    app.register_blueprint(frontend_bp)

    return app