from flask import Blueprint, request, jsonify
from database.db import db
from models.material import Material

material_bp = Blueprint("material_bp", __name__, url_prefix="/materials")

# ADD material expense
@material_bp.route("", methods=["POST"])
def add_material():
    data = request.json

    material = Material(
        project_id=data.get("project_id"),
        name=data.get("name"),
        quantity=data.get("quantity"),
        cost=data.get("cost"),
        date=data.get("date")
    )
    
@material_bp.route("/<int:material_id>", methods=["DELETE"])
def delete_material(material_id):
    material = Material.query.get(material_id)
    if not material:
        return {"message": "Material not found"}, 404

    db.session.delete(material)
    db.session.commit()
    return {"message": "Material deleted successfully"}, 200


    db.session.add(material)
    db.session.commit()

    return jsonify({"message": "Material expense added"}), 201
