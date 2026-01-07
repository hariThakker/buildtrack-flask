from flask import Blueprint, request, jsonify
from database.db import db
from models.labour import Labour

labour_bp = Blueprint("labour_bp", __name__, url_prefix="/labour")

# ADD labour payment
@labour_bp.route("", methods=["POST"])
def add_labour():
    data = request.json

    labour = Labour(
        project_id=data.get("project_id"),
        worker_name=data.get("worker_name"),
        wage=data.get("wage"),
        date=data.get("date")
    )
    
@labour_bp.route("/<int:labour_id>", methods=["DELETE"])
def delete_labour(labour_id):
    labour = Labour.query.get(labour_id)
    if not labour:
        return {"message": "Labour not found"}, 404

    db.session.delete(labour)
    db.session.commit()
    return {"message": "Labour deleted successfully"}, 200

    db.session.add(labour)
    db.session.commit()

    return jsonify({"message": "Labour payment added"}), 201
