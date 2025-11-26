# app/utils/jwt_utils.py
from flask import request, jsonify, current_app
import jwt
from functools import wraps

# app/utils/jwt_utils.py
from flask import request, jsonify, current_app, g
import jwt
from functools import wraps

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"error": "Token is missing"}), 401
        
        token = auth_header[7:] if auth_header.startswith("Bearer ") else auth_header
        
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

            g.current_user = {
                "username": data.get("username"),
                "role": data.get("role")
            }
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token is invalid"}), 401
        
        return f(*args, **kwargs)
    return decorated

def requires_role(*roles):
    def wrapper(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            user = getattr(g, "current_user", None)
            print(user["role"])
            if not user:
                return jsonify({"error": "Unauthorized"}), 401
            if user["role"] not in roles:
                return jsonify({"error": "Forbidden: insufficient permissions"}), 403
            return f(*args, **kwargs)
        return decorated
    return wrapper