# app/routes/auth.py
from flask import Blueprint, current_app, request, jsonify
import jwt, datetime
from app.utils.jwt_utils import token_required
from app.data.sample_data import users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    if users.get(username) != password:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        'username': username,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token})