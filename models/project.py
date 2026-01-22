def project_schema(data):
    return {
        "name": data["name"],
        "client": data["client"],
        "location": data["location"],
        "start_date": data["start_date"],
        "is_active": True
    }