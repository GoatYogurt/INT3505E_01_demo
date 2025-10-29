# app/utils/jwt_utils.py
from flask import request, jsonify
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token is missing"}), 401
        if token.startswith("Bearer "):
            token = token[7:]
        try:
            data = jwt.decode(token, 'your_secret_key_here', algorithms=["HS256"])
            current_user = data['username']
        except:
            return jsonify({"error": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)
    return decorated