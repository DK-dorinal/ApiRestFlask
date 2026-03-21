# ApiRestFlask
creation d'une api rest flask grace a l'aide de clee route comme tuteur
===================================================
          PROJET : API REST FLASK (BLOG)
===================================================

1. DESCRIPTION DU PROJET
------------------------
Ce projet est une API REST simple permettant de gérer des articles de blog. 
Il permet de créer, lire, modifier, supprimer et rechercher des articles 
stockés dans une base de données SQLite.

Technologies utilisées :
- Python
- Flask (Framework Web)
- Flask-SQLAlchemy (Gestion de la base de données)
- SQLite (Base de données légère)

2. INSTALLATION ET LANCEMENT
----------------------------
Pour faire fonctionner le projet sur votre machine :

A. Cloner le dépôt :
   Lien : https://github.com/DK-dorinal/ApiRestFlask

B. Installer les outils nécessaires :
   Ouvrez votre terminal dans le dossier du projet et tapez :
   pip install flask flask-sqlalchemy

C. Lancer l'application :
   Tapez la commande suivante :
   python app.py

L'API sera active à l'adresse : http://127.0.0.1:5000

3. UTILISATION AVEC POSTMAN
---------------------------
Pour tester les fonctionnalités, utilisez l'outil Postman en configurant 
les requêtes comme suit :

--- GÉRER LES ARTICLES ---

• CRÉER UN ARTICLE :
  - Méthode : POST
  - URL : http://127.0.0.1:5000/api/articles
  - Body (sélectionnez 'raw' et 'JSON') :
    {
        "titre": "Mon premier article",
        "contenu": "Ceci est le texte de l'article",
        "auteur": "Ton Nom"
    }

• VOIR TOUS LES ARTICLES :
  - Méthode : GET
  - URL : http://127.0.0.1:5000/api/articles

• VOIR UN ARTICLE PRÉCIS :
  - Méthode : GET
  - URL : http://127.0.0.1:5000/api/articles/1  (remplacez 1 par l'ID voulu)

• MODIFIER UN ARTICLE :
  - Méthode : PUT
  - URL : http://127.0.0.1:5000/api/articles/1
  - Body (JSON) : Envoyez les nouvelles données (titre, contenu, auteur).

• SUPPRIMER UN ARTICLE :
  - Méthode : DELETE
  - URL : http://127.0.0.1:5000/api/articles/1

--- RECHERCHE ET FILTRES ---

• RECHERCHER PAR TITRE :
  - Méthode : GET
  - URL : http://127.0.0.1:5000/api/articles/search?titre=MonTitre

• FILTRER PAR AUTEUR :
  - Méthode : GET
  - URL : http://127.0.0.1:5000/api/articles?auteur=NomDeLAuteur

4. STRUCTURE DES FICHIERS
-------------------------
- app.py : Point d'entrée, configure la base de données blog.db.
- models.py : Définit ce qu'est un "Article" (ID, Titre, Contenu, Date, Auteur).
- routes.py : Contient toute l'intelligence de l'API (les liens et les actions).

---------------------------------------------------
Développé par : DK-dorinal
Lien GitHub : https://github.com/DK-dorinal/ApiRestFlask