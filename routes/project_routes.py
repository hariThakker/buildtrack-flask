from flask import Blueprint, request, jsonify
from database.db import db
from models.project import Project
from models.material import Material
from models.labour import Labour
from sqlalchemy import func 

project_bp = Blueprint("project_bp", __name__, url_prefix="/projects")

# CREATE project
@project_bp.route("", methods=["POST"])
def create_project():
    data = request.json

    project = Project(
        name=data.get("name"),
        client=data.get("client"),
        location=data.get("location"),
        start_date=data.get("start_date")
    )

    db.session.add(project)
    db.session.commit()

    return jsonify({"message": "Project created", "project_id": project.id}), 201

# PROJECT EXPENSE SUMMARY
@project_bp.route("/<int:project_id>/summary", methods=["GET"])
def project_summary(project_id):
    material_total = db.session.query(
        func.sum(Material.cost)
    ).filter(Material.project_id == project_id).scalar() or 0

    labour_total = db.session.query(
        func.sum(Labour.wage)
    ).filter(Labour.project_id == project_id).scalar() or 0

    return jsonify({
        "project_id": project_id,
        "material_cost": material_total,
        "labour_cost": labour_total,
        "total_expense": material_total + labour_total
    })

@project_bp.route("/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if not project:
        return {"message": "Project not found"}, 404

    db.session.delete(project)
    db.session.commit()
    return {"message": "Project deleted successfully"}, 200


# GET all projects
@project_bp.route("", methods=["GET"])
def get_projects():
    projects = Project.query.all()

    result = []
    for p in projects:
        result.append({
            "id": p.id,
            "name": p.name,
            "client": p.client,
            "location": p.location,
            "start_date": p.start_date,
            "is_active": p.is_active
        })

    return jsonify(result)
