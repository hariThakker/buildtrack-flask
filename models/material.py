def material_schema(data):
    return {
        "project_id": data["project_id"],  # string ObjectId
        "name": data["name"],
        "quantity": int(data["quantity"]),
        "cost": float(data["cost"]),
        "date": data["date"]
    }
