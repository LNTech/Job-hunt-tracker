from flask import Blueprint

bp = Blueprint('jobs', __name__)

from app.blueprints.jobs import routes