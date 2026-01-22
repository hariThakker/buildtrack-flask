from flask import Blueprint, request, jsonify, session
from database.mongo import users_collection
from models.user import user_schema, verify_password

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/auth")

# ======================
# REGISTER USER (ADMIN ONLY LATER)
# ======================
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    required = ["name", "email", "password"]
    if not data or not all(data.get(f) for f in required):
        return jsonify({"message": "All fields required"}), 400

    if users_collection.find_one({"email": data["email"]}):
        return jsonify({"message": "User already exists"}), 409

    user = user_schema(data)
    users_collection.insert_one(user)

    return jsonify({"message": "User registered successfully"}), 201


# ======================
# LOGIN
# ======================
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    if not data or not data.get("email") or not data.get("password"):
        return jsonify({"message": "Email & password required"}), 400

    user = users_collection.find_one({"email": data["email"]})
    if not user or not verify_password(user, data["password"]):
        return jsonify({"message": "Invalid credentials"}), 401

    session["user_id"] = str(user["_id"])
    session["role"] = user["role"]
    session["name"] = user["name"]

    return jsonify({
        "message": "Login successful",
        "role": user["role"]
    }), 200


# ======================
# LOGOUT
# ======================
@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"}), 200
