from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__) #creeation de l'application

    DB_URL = os.path.abspath(os.path.dirname(__file__)) #creation du chemin vers la bd

    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+os.path.join(DB_URL,'blog.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes import articlees_bp
    app.register_blueprint(articlees_bp)

    return app

#lancement de l'app
if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all() 
    app.run(debug=True)