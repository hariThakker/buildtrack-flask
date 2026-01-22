from flask import Flask
from routes.project_routes import project_bp
from routes.material_routes import material_bp
from routes.labour_routes import labour_bp
from routes.ui_routes import ui_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)

# 🔐 Session secret
app.secret_key = "buildtrack-secret-key"

app.register_blueprint(project_bp)
app.register_blueprint(material_bp)
app.register_blueprint(labour_bp)
app.register_blueprint(ui_bp)
app.register_blueprint(auth_bp)

@app.route("/")
def home():
    return {"message": "BuildTrack API running (MongoDB + Auth)"}

if __name__ == "__main__":
    app.run(debug=True)
