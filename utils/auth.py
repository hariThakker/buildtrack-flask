from flask import session, jsonify
from functools import wraps

def role_required(*roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            if "user_id" not in session:
                return jsonify({"message": "Authentication required"}), 401

            if session.get("role") not in roles:
                return jsonify({"message": "Access denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
