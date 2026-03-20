================================================================================
                   PROJET API REST FLASK - GUIDE COMPLET
================================================================================

Ce fichier contient l'ensemble du projet avec des explications détaillées pour
chaque ligne de code. Vous allez comprendre comment fonctionne chaque partie.


/*******************************************************************/

STRUCTURE DU PROJET

Créez un dossier nommé "ApiRestFlask" avec cette structure :

ApiRestFlask/
│
├── app.py          # Fichier principal qui lance l'application
├── models.py       # Définit la structure de la base de données
├── routes.py       # Contient toutes les routes (URLs) de l'API
└── blog.db         # Base de données SQLite (créée automatiquement)


/*******************************************************************/

INSTALLATION DES OUTILS

Ouvrez un terminal (invite de commandes) dans le dossier ApiRestFlask et exécutez :

1. Créer un environnement virtuel (isole les dépendances) :
   python -m venv .venv

2. Activer l'environnement virtuel :
   - Sur Windows : .venv\Scripts\activate
   - Sur Mac/Linux : source .venv/bin/activate

3. Installer Flask et SQLAlchemy :
   pip install flask flask-sqlalchemy


/*******************************************************************/

FICHIER models.py (Structure des données)

Ce fichier définit comment les articles sont stockés dans la base de données.

python
from app import db                    # Importe la base de données depuis app.py
from datetime import datetime          # Pour gérer les dates

class Article(db.Model):               # Crée une table "articles"
    __tablename__ = "articles"         # Nom de la table dans la base de données
    
    # Définition des colonnes (champs) de la table
    id = db.Column(db.Integer, primary_key=True)        # Identifiant unique (auto-incrémenté)
    titre = db.Column(db.String(100), nullable=False)   # Titre (100 caractères max, obligatoire)
    contenu = db.Column(db.Text, nullable=False)        # Contenu (texte long, obligatoire)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Date auto-remplie
    auteur = db.Column(db.String(100), nullable=False)  # Auteur (100 caractères max, obligatoire)
    
    def mise_dictonnaire(self):        # Méthode pour convertir l'article en dictionnaire
        return {
            "id": self.id,              # L'ID de l'article
            "titre": self.titre,        # Le titre
            "contenu": self.contenu,    # Le contenu
            "date": self.date,          # La date
            "auteur": self.auteur       # L'auteur
        }