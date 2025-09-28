from flask import Flask, jsonify
from config import Config
from app.extensions import db, jwt

from app.models.job import Job
from app.models.user import User

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    app.config['JWT_COOKIE_SECURE'] = True  # Only True if you're using HTTPS
    app.config['JWT_ACCESS_COOKIE_NAME'] = 'access_token'
    app.config['JWT_REFRESH_COOKIE_NAME'] = 'refresh_token'
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Or True if you're handling CSRF

    db.init_app(app)
    jwt.init_app(app)

    with app.app_context():
        from app.models.job import Job
        from app.models.user import User
        db.create_all()

    from app.blueprints.front import bp as frontend_bp
    app.register_blueprint(frontend_bp)

    from app.blueprints.authenticator import bp as authenticator_bp
    app.register_blueprint(authenticator_bp, url_prefix="/account/")

    @jwt.user_lookup_loader
    def user_lookup_callback(jwt_header, jwt_data):
        identity = jwt_data.get("sub")
        return User.query.filter_by(username=identity).one_or_none()

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_data):
        return jsonify({"message": "Token is expired", "error": "token_expired"}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Token is invalid", "error": "token_invalid"}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({"message": "Token is missing", "error": "authorization_header"}), 404
        
    return app