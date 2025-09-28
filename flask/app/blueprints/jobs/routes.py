from app.blueprints.jobs import bp
from flask import render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, get_jwt, jwt_required, create_refresh_token

@bp.route('/')
@jwt_required(locations=["cookies"])
def get_jobs():
    identity = ""
    