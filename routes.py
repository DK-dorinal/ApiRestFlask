from flask import Blueprint, jsonify, request
from app import db
from models import Article
from datetime import datetime

articlees_bp = Blueprint('articles', __name__)


#route pour creer des artciles
@articlees_bp.route('/api/articles', methods=['POST'])
def creer_articles():
    data = request.get_json()
    
    #validation des champs
    if not data.get('titre') or not data.get('contenu') or not data.get('auteur'):
        return jsonify({'message': 'le titre, le contenu et l\'auteur sont obligatoire'}), 400
    
    a = Article(
        titre=data['titre'],
        contenu=data['contenu'],
        auteur=data['auteur'],
        date=datetime.now()
    )
    
    db.session.add(a)
    db.session.commit()
    return jsonify({'message': 'article cree avec success','article':a.mise_dictonnaire()}), 201

#route pour recuperer tous les articles
@articlees_bp.route('/api/articles', methods=['GET'])
def recuperer_articles():
    auteur = request.args.get('auteur')
    date = request.args.get('date')
    
    query = Article.query
    if auteur:
        query = query.filter_by(auteur=auteur)
    if date:
        query = query.filter_by(date=date)
    
    articles = query.all()
    return jsonify({'articles': [a.mise_dictonnaire() for a in articles]}), 200

#recuperer les articles par id
@articlees_bp.route('/api/articles/<int:id>', methods=['GET'])
def recuperer_article(id):
    a = Article.query.get_or_404(id)
    if not a:
        return jsonify({'message': 'article non trouve'}), 404
    return jsonify({'article': a.mise_dictonnaire()}), 200

#route pour modifier un article
@articlees_bp.route('/api/articles/<int:id>', methods=['PUT'])
def modifier_article(id):
    a = Article.query.get(id)
    
    if not a:
        return jsonify({'message' : 'article non trouve'}), 404
    
    data = request.get_json()
    if not data.get('titre') or not data.get('contenu') or not data.get('auteur'):
        return jsonify({'message': 'le titre, le contenu et l\'auteur sont obligatoire'}), 400
    
    a.titre = data['titre']
    a.contenu = data['contenu']
    a.auteur = data['auteur']
    db.session.commit()
    return jsonify({'message': 'article modifie avec success', 'article': a.mise_dictonnaire()}), 200

#route pour supprimer un article
@articlees_bp.route('/api/articles/<int:id>', methods=['DELETE'])
def supprimer_article(id):
    a = Article.query.get_or_404(id)
    if not a:
        return jsonify({'message': 'article non trouve'}), 404
    db.session.delete(a)
    db.session.commit()
    return jsonify({'message': 'article supprime avec success'}), 200

#rechercher articles
@articlees_bp.route('/api/articles/search', methods=['GET'])
def rechercher_articles():
    titre = request.args.get('titre')
    if not titre:
        return jsonify({'message': 'parametre de la requet obligatoire'}), 400
    
    articles = Article.query.filter(Article.titre.contains(titre)).all()
    return jsonify({'articles': [a.mise_dictonnaire() for a in articles]}), 200