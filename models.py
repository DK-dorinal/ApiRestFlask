from app import db
from datetime import datetime

class Article(db.Model):
    __tablename__ = "articles"
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    auteur = db.Column(db.String(100), nullable=False)
    
    def mise_dictonnaire(self):
        return {
            "id": self.id,
            "titre": self.titre,
            "contenu": self.contenu,
            "date": self.date,
            "auteur": self.auteur
        }