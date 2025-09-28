from app.blueprints.authenticator import bp
from app.models.user import User
from flask_jwt_extended import create_access_token, get_jwt_identity, current_user, get_jwt, jwt_required, create_refresh_token
from flask import jsonify, request, render_template, make_response

@bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    
    if data.get("username", "") == "":
        return jsonify({"message": "Username not specified"}), 403
    if len(data.get("password", "")) < 12:
        return jsonify({"message": f"Password is not long enough ({len(data.get("password", ""))} characters instead of 12)"}), 403
    
    user = User.get_by_username(username = data.get("username"))


    if user is not None:
        return jsonify({"message": "User with that username already exists"}), 401
    
    new_user = User(
        username = data.get("username", ""),
    )

    new_user.change_password(data.get("password", ""))
    new_user.add()

    return jsonify({"message": "User registered succesfully"}), 201


@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if data.get("username", "") == "":
        return jsonify({"message": "Username not specified"}), 403

    user = User.get_by_username(data.get("username"))
    if user is None or not user.check_password(data.get("password", "")):
        return jsonify({"message": "Invalid username or password"}), 404

    access_token = create_access_token(identity=user.username)
    refresh_token = create_refresh_token(identity=user.username)

    resp = make_response(jsonify({"message": "Logged in successfully"}))
    resp.set_cookie(
        "access_token", access_token,
        httponly=True,
        secure=True,      # Only over HTTPS
        samesite='Strict', # CSRF protection
        max_age=15*60     # 15 minutes
    )
    resp.set_cookie(
        "refresh_token", refresh_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=7*24*60*60 # 7 days
    )

    return resp, 200

@bp.route("/identity", methods=["GET"])
@jwt_required(locations=["cookies"])
def identity():
    return jsonify({"username": get_jwt_identity()}), 200


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True, locations=["cookies"])
def refresh():
    identity = get_jwt_identity()
    new_access_token = create_access_token(identity=identity)
    new_refresh_token = create_refresh_token(identity=identity)

    resp = make_response(jsonify({"message": "Token refreshed successfully"}))
    resp.set_cookie(
        "access_token", new_access_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=15*60
    )
    resp.set_cookie(
        "refresh_token", new_refresh_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=7*24*60*60
    )
    return resp, 200