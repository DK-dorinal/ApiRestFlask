from flask import Flask, render_template
from flask_sqlachemy import SQLAlchemy
import os

app = Flask(__name__) #creeation de l'application

DB_URL = os.path.abspath(os.path.dirname(__file__)) #creation du chemin vers la bd

app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+os.path.join(DB_URL,'test')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

#creation des routes
@app.route('/')#route de lancement du projet
def index():
    return render_template('create.html') #templates ou page html retourne

#lancement du projet
if __name__ == '__main__':
    app.run(debug=True)