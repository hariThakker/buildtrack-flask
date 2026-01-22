def labour_schema(data):
    return {
        "project_id": data["project_id"],  # string ObjectId
        "worker_name": data["worker_name"],
        "wage": float(data["wage"]),
        "date": data["date"]
    }
