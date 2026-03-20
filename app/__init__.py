from flask import Flask

def create_app():
    app = Flask(__name__)

    app.config ['SECRET_KEY'] ="dev-secret-key-change-in-production"

    from app.routes.dashboard import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app