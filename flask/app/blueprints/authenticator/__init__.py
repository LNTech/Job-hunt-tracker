from flask import Blueprint

bp = Blueprint('authenticator', __name__)

from app.blueprints.authenticator import routes