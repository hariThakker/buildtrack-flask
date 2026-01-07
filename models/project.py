from database.db import db

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    client = db.Column(db.String(100))
    location = db.Column(db.String(100))
    start_date = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
