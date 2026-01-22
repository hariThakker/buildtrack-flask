from flask import Blueprint, request, jsonify
from database.mongo import (
    projects_collection,
    materials_collection,
    labour_collection
)
from bson import ObjectId
from models.project import project_schema
from utils.auth import role_required

project_bp = Blueprint("project_bp", __name__, url_prefix="/projects")

# =========================
# CREATE PROJECT (ADMIN + MANAGER)
# =========================
@project_bp.route("", methods=["POST"])
@role_required("admin", "manager")
def create_project():
    data = request.get_json()

    required = ["name", "client", "location", "start_date"]
    if not data or not all(data.get(f) for f in required):
        return jsonify({"message": "All fields are required"}), 400

    project = project_schema(data)
    result = projects_collection.insert_one(project)

    return jsonify({
        "message": "Project created",
        "project_id": str(result.inserted_id)
    }), 201


# =========================
# GET ALL PROJECTS (ALL ROLES)
# =========================
@project_bp.route("", methods=["GET"])
def get_projects():
    projects = []

    for p in projects_collection.find():
        p["_id"] = str(p["_id"])
        projects.append(p)

    return jsonify(projects), 200


# =========================
# PROJECT SUMMARY (ALL ROLES)
# =========================
@project_bp.route("/<project_id>/summary", methods=["GET"])
def project_summary(project_id):
    if not ObjectId.is_valid(project_id):
        return jsonify({"message": "Invalid project ID"}), 400

    material_cursor = materials_collection.aggregate([
        {"$match": {"project_id": project_id}},
        {"$group": {"_id": None, "total": {"$sum": "$cost"}}}
    ])

    labour_cursor = labour_collection.aggregate([
        {"$match": {"project_id": project_id}},
        {"$group": {"_id": None, "total": {"$sum": "$wage"}}}
    ])

    material_cost = next(material_cursor, {}).get("total", 0)
    labour_cost = next(labour_cursor, {}).get("total", 0)

    return jsonify({
        "material_cost": material_cost,
        "labour_cost": labour_cost,
        "total_expense": material_cost + labour_cost
    }), 200


# =========================
# DELETE PROJECT (ADMIN ONLY) ✅ 8.7
# =========================
@project_bp.route("/<project_id>", methods=["DELETE"])
@role_required("admin")
def delete_project(project_id):
    if not ObjectId.is_valid(project_id):
        return jsonify({"message": "Invalid project ID"}), 400

    result = projects_collection.delete_one(
        {"_id": ObjectId(project_id)}
    )

    if result.deleted_count == 0:
        return jsonify({"message": "Project not found"}), 404

    materials_collection.delete_many({"project_id": project_id})
    labour_collection.delete_many({"project_id": project_id})

    return jsonify({"message": "Project deleted successfully"}), 200
