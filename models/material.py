from database.db import db

class Material(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100))
    quantity = db.Column(db.Float)
    cost = db.Column(db.Float)
    date = db.Column(db.String(20))
