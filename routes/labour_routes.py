from flask import Blueprint, request, jsonify
from database.mongo import labour_collection, projects_collection
from models.labour import labour_schema
from bson import ObjectId
from utils.auth import role_required

labour_bp = Blueprint("labour_bp", __name__, url_prefix="/labour")

# =========================
# ADD LABOUR (ADMIN + MANAGER) ✅ 8.8
# =========================
@labour_bp.route("", methods=["POST"])
@role_required("admin", "manager")
def add_labour():
    data = request.get_json()

    required = ["project_id", "worker_name", "wage", "date"]
    if not data or not all(data.get(f) for f in required):
        return jsonify({"message": "All fields required"}), 400

    if not ObjectId.is_valid(data["project_id"]):
        return jsonify({"message": "Invalid project ID"}), 400

    if not projects_collection.find_one(
        {"_id": ObjectId(data["project_id"])}
    ):
        return jsonify({"message": "Project not found"}), 404

    labour = labour_schema(data)
    labour_collection.insert_one(labour)

    return jsonify({"message": "Labour added successfully"}), 201


# =========================
# DELETE LABOUR (ADMIN ONLY)
# =========================
@labour_bp.route("/<labour_id>", methods=["DELETE"])
@role_required("admin")
def delete_labour(labour_id):
    if not ObjectId.is_valid(labour_id):
        return jsonify({"message": "Invalid labour ID"}), 400

    labour_collection.delete_one(
        {"_id": ObjectId(labour_id)}
    )

    return jsonify({"message": "Labour deleted"}), 200
