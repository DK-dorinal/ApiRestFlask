from flask import Blueprint, jsonify, request
from extensions import db
from models import Article
from datetime import datetime

articlees_bp = Blueprint('articles', __name__)


def ok(data=None, message="Succès", status=200, **extra):
    body = {"success": True, "message": message}
    if data is not None:
        body["data"] = data
    body.update(extra)
    return jsonify(body), status


def err(message="Erreur", status=400, errors=None):
    body = {"success": False, "message": message}
    if errors:
        body["errors"] = errors
    return jsonify(body), status


def valider_champs(data, partial=False):
    problems = []
    required = ["titre", "contenu", "auteur"]
    for field in required:
        if not partial and field not in data:
            problems.append(f"'{field}' est obligatoire.")
        elif field in data and not str(data[field]).strip():
            problems.append(f"'{field}' ne peut pas etre vide.")
    return problems


@articlees_bp.route('/api/articles/search', methods=['GET'])
def rechercher_articles():
    """
    Rechercher des articles par titre.
    ---
    tags:
      - Articles
    parameters:
      - name: titre
        in: query
        type: string
        required: true
        description: Titre a rechercher
    responses:
      200:
        description: Liste des articles trouves
      400:
        description: Parametre manquant
    """
    titre = request.args.get('titre', '').strip()
    if not titre:
        return err('parametre de la requet obligatoire', 400)

    articles = Article.query.filter(Article.titre.ilike(f'%{titre}%')).all()
    return ok([a.mise_dictonnaire() for a in articles],
              f"{len(articles)} article(s) trouve(s).")


@articlees_bp.route('/api/articles', methods=['POST'])
def creer_articles():
    """
    Creer un nouvel article.
    ---
    tags:
      - Articles
    parameters:
      - in: body
        name: body
        required: true
        schema:
          required: [titre, contenu, auteur]
          properties:
            titre:
              type: string
              example: "Mon premier article"
            contenu:
              type: string
              example: "Ceci est le texte de l'article"
            auteur:
              type: string
              example: "DK-dorinal"
    responses:
      201:
        description: Article cree
      400:
        description: Champs manquants
      422:
        description: Erreur de validation
    """
    data = request.get_json(silent=True)
    if data is None:
        return err("Le corps de la requete doit etre du JSON valide.", 400)

    errors = valider_champs(data)
    if errors:
        return err("le titre, le contenu et l'auteur sont obligatoire", 422, errors=errors)

    a = Article(
        titre=data['titre'].strip(),
        contenu=data['contenu'].strip(),
        auteur=data['auteur'].strip(),
        date=datetime.now(),
    )
    db.session.add(a)
    db.session.commit()
    return ok(a.mise_dictonnaire(), 'article cree avec success', 201)


@articlees_bp.route('/api/articles', methods=['GET'])
def recuperer_articles():
    """
    Recuperer tous les articles (filtrables).
    ---
    tags:
      - Articles
    parameters:
      - name: auteur
        in: query
        type: string
      - name: date
        in: query
        type: string
        description: Format YYYY-MM-DD
    responses:
      200:
        description: Liste des articles
    """
    auteur   = request.args.get('auteur')
    date_str = request.args.get('date')

    query = Article.query
    if auteur:
        query = query.filter(Article.auteur.ilike(f'%{auteur}%'))
    if date_str:
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
            query = query.filter(db.func.date(Article.date) == date_obj)
        except ValueError:
            return err("Format de date invalide. Utilisez YYYY-MM-DD.", 400)

    articles = query.order_by(Article.date.desc()).all()
    return ok([a.mise_dictonnaire() for a in articles],
              f"{len(articles)} article(s) recupere(s).",
              count=len(articles))


@articlees_bp.route('/api/articles/<int:id>', methods=['GET'])
def recuperer_article(id):
    """
    Recuperer un article par son ID.
    ---
    tags:
      - Articles
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Article trouve
      404:
        description: Article non trouve
    """
    a = db.session.get(Article, id)
    if not a:
        return err('article non trouve', 404)
    return ok(a.mise_dictonnaire(), 'article recupere avec success')


@articlees_bp.route('/api/articles/<int:id>', methods=['PUT'])
def modifier_article(id):
    """
    Modifier un article (remplacement complet).
    ---
    tags:
      - Articles
    parameters:
      - name: id
        in: path
        type: integer
        required: true
      - in: body
        name: body
        required: true
        schema:
          required: [titre, contenu, auteur]
          properties:
            titre:
              type: string
            contenu:
              type: string
            auteur:
              type: string
    responses:
      200:
        description: Article modifie
      404:
        description: Article non trouve
      422:
        description: Erreur de validation
    """
    a = db.session.get(Article, id)
    if not a:
        return err('article non trouve', 404)

    data = request.get_json(silent=True)
    if data is None:
        return err("Le corps de la requete doit etre du JSON valide.", 400)

    errors = valider_champs(data)
    if errors:
        return err("le titre, le contenu et l'auteur sont obligatoire", 422, errors=errors)

    a.titre   = data['titre'].strip()
    a.contenu = data['contenu'].strip()
    a.auteur  = data['auteur'].strip()
    db.session.commit()
    return ok(a.mise_dictonnaire(), 'article modifie avec success')


@articlees_bp.route('/api/articles/<int:id>', methods=['DELETE'])
def supprimer_article(id):
    """
    Supprimer un article.
    ---
    tags:
      - Articles
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Article supprime
      404:
        description: Article non trouve
    """
    a = db.session.get(Article, id)
    if not a:
        return err('article non trouve', 404)

    deleted = a.mise_dictonnaire()
    db.session.delete(a)
    db.session.commit()
    return ok(deleted, 'article supprime avec success')
