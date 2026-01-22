from flask import Blueprint, render_template, session, redirect

ui_bp = Blueprint("ui_bp", __name__, url_prefix="/ui")

def login_required():
    return "user_id" in session

@ui_bp.before_request
def protect_ui():
    if not login_required():
        return redirect("/login")

@ui_bp.route("")
def dashboard():
    return render_template("index.html")

@ui_bp.route("/add-project")
def add_project():
    return render_template("add_project.html")

@ui_bp.route("/add-material")
def add_material():
    return render_template("add_material.html")

@ui_bp.route("/add-labour")
def add_labour():
    return render_template("add_labour.html")

@ui_bp.route("/summary/<project_id>")
def summary(project_id):
    return render_template("summary.html", project_id=project_id)
