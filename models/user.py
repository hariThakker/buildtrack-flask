from werkzeug.security import generate_password_hash, check_password_hash

def user_schema(data):
    return {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "role": data.get("role", "manager")  # default role
    }

def verify_password(user, password):
    return check_password_hash(user["password"], password)
