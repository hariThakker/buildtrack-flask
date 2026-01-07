from flask import Flask
from config import SQLALCHEMY_DATABASE_URI
from database.db import db
from flask import render_template
from routes.project_routes import project_bp
from routes.material_routes import material_bp
from routes.labour_routes import labour_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

app.register_blueprint(project_bp)
app.register_blueprint(material_bp)
app.register_blueprint(labour_bp)

with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return {"message": "Construction Management API running"}

@app.route("/ui")
def dashboard():
    return render_template("index.html")

@app.route("/ui/add-project")
def add_project_ui():
    return render_template("add_project.html")

@app.route("/ui/add-material")
def add_material_ui():
    return render_template("add_material.html")

@app.route("/ui/add-labour")
def add_labour_ui():
    return render_template("add_labour.html")

@app.route("/ui/summary/<int:project_id>")
def summary_ui(project_id):
    return render_template("summary.html", project_id=project_id)


if __name__ == "__main__":
    app.run(debug=True)
