from flask import Blueprint, render_template, session, redirect, request

ui_bp = Blueprint("ui_bp", __name__, url_prefix="/ui")

# =========================
# LOGIN PAGE (PUBLIC)
# =========================
@ui_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


# =========================
# PROTECT ALL /ui ROUTES
# =========================
@ui_bp.before_request
def protect_ui():
    # allow login page without session
    if "/login" in str(request.path):
        return

    if "user_id" not in session:
        return redirect("/ui/login")


# =========================
# DASHBOARD
# =========================
@ui_bp.route("")
def dashboard():
    return render_template(
        "index.html",
        user_name=session.get("name"),
        role=session.get("role")
    )


@ui_bp.route("/add-project")
def add_project():
    return render_template("add_project.html", role=session.get("role"))


@ui_bp.route("/add-material")
def add_material():
    return render_template("add_material.html", role=session.get("role"))


@ui_bp.route("/add-labour")
def add_labour():
    return render_template("add_labour.html", role=session.get("role"))


@ui_bp.route("/summary/<project_id>")
def summary(project_id):
    return render_template("summary.html", project_id=project_id)
