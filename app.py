from flask import Flask, jsonify, redirect
from flasgger import Swagger

from config import active_config
from extensions import db
from routes import articlees_bp


def create_app(config=None):
    app = Flask(__name__)

    app.config.from_object(config or active_config)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(articlees_bp)

    Swagger(app)

    @app.route("/")
    def index():
        return redirect("/apidocs")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "healthy", "app": "ApiRestFlask – Blog API"}), 200

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"success": False, "message": "Route introuvable."}), 404

    @app.errorhandler(405)
    def method_not_allowed(e):
        return jsonify({"success": False, "message": "Methode non autorisee."}), 405

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"success": False, "message": "Erreur interne du serveur."}), 500

    return app


if __name__ == '__main__':
    application = create_app()
    print("\n  Blog API  ->  http://127.0.0.1:5000")
    print("  Swagger UI ->  http://127.0.0.1:5000/apidocs\n")
    application.run(debug=True)
