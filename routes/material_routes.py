from flask import Blueprint, request, jsonify
from database.mongo import materials_collection, projects_collection
from models.material import material_schema
from bson import ObjectId
from utils.auth import role_required

material_bp = Blueprint("material_bp", __name__, url_prefix="/materials")

# =========================
# ADD MATERIAL (ADMIN + MANAGER) ✅ 8.8
# =========================
@material_bp.route("", methods=["POST"])
@role_required("admin", "manager")
def add_material():
    data = request.get_json()

    required = ["project_id", "name", "quantity", "cost", "date"]
    if not data or not all(data.get(f) for f in required):
        return jsonify({"message": "All fields required"}), 400

    if not ObjectId.is_valid(data["project_id"]):
        return jsonify({"message": "Invalid project ID"}), 400

    if not projects_collection.find_one(
        {"_id": ObjectId(data["project_id"])}
    ):
        return jsonify({"message": "Project not found"}), 404

    material = material_schema(data)
    materials_collection.insert_one(material)

    return jsonify({"message": "Material added successfully"}), 201


# =========================
# DELETE MATERIAL (ADMIN ONLY)
# =========================
@material_bp.route("/<material_id>", methods=["DELETE"])
@role_required("admin")
def delete_material(material_id):
    if not ObjectId.is_valid(material_id):
        return jsonify({"message": "Invalid material ID"}), 400

    materials_collection.delete_one(
        {"_id": ObjectId(material_id)}
    )

    return jsonify({"message": "Material deleted"}), 200
