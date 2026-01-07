from database.db import db

class Labour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, nullable=False)
    worker_name = db.Column(db.String(100))
    wage = db.Column(db.Float)
    date = db.Column(db.String(20))
