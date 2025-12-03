from flask import Blueprint, current_app, request, jsonify
import jwt, datetime
from app.data.sample_data import users

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Log in a user
    This endpoint authenticates a user based on username and password.
    ---
    tags:
      - Authentication
    summary: Authenticate a user
    description: Receives a username and password, validates them against stored users, and returns a JWT token if successful.
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: body
        required: true
        description: User credentials needed for login.
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
              example: "admin"
            password:
              type: string
              format: password
              example: "adminpass"
    responses:
      200:
        description: Login successful. A JWT token is returned.
        schema:
          type: object
          properties:
            token:
              type: string
              example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2Vybm..."
      400:
        description: Bad Request. Username or password was not provided.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Username and password required"
      401:
        description: Unauthorized. Invalid credentials.
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Invalid credentials"
    """
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if any(u.username == username and u.password == password for u in users):
        pass
    else:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode({
        'username': username,
        'role': next(u.role for u in users if u.username == username),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }, current_app.config['SECRET_KEY'], algorithm="HS256")
    return jsonify({"token": token})