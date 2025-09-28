from app.blueprints.front import bp
from flask import render_template
from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, get_jwt, jwt_required, create_refresh_token

@bp.route('/')
def index():
    return render_template("index.html")

@bp.route("/register")
def register():
    return render_template("register.html")

@bp.route("/login")
def login():
    return render_template("login.html")

@bp.route("/jobs")
@jwt_required(locations=["cookies"])
def jobs():
    identity = get_jwt_identity()
    return render_template("jobs.html", username=identity)
