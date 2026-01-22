from pymongo import MongoClient

# Local MongoDB connection
client = MongoClient("mongodb://localhost:27017")

# Database
db = client["buildtrack_db"]

# Collections
projects_collection = db["projects"]
materials_collection = db["materials"]
labour_collection = db["labour"]
users_collection = db["users"]
