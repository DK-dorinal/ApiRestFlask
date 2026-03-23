# ApiRestFlask

API REST pour gérer des articles de blog, développée avec Flask et SQLite.

Dépôt GitHub : https://github.com/DK-dorinal/ApiRestFlask

---

## Table des matières

1. [Description du projet](#1-description-du-projet)
2. [Technologies utilisées](#2-technologies-utilisées)
3. [Structure des fichiers](#3-structure-des-fichiers)
4. [Installation](#4-installation)
5. [Configuration](#5-configuration)
6. [Lancement](#6-lancement)
7. [Documentation Swagger](#7-documentation-swagger)
8. [Modèle de données — Article](#8-modèle-de-données--article)
9. [Endpoints de l'API](#9-endpoints-de-lapi)
10. [Formats de réponse](#10-formats-de-réponse)
11. [Codes HTTP utilisés](#11-codes-http-utilisés)
12. [Bonnes pratiques appliquées](#12-bonnes-pratiques-appliquées)
13. [Tester avec Postman](#13-tester-avec-postman)
14. [Variables d'environnement](#14-variables-denvironnement)

---

## 1. Description du projet

Ce projet est une API REST permettant de gérer des articles de blog. Elle couvre l'ensemble des opérations CRUD (créer, lire, modifier, supprimer) ainsi qu'une fonctionnalité de recherche par titre ou contenu.

Chaque article possède un titre, un contenu, un auteur, une date de création, une catégorie et des tags. Les données sont stockées dans une base SQLite locale. L'API est entièrement documentée via Swagger UI, accessible directement au lancement.

---

## 2. Technologies utilisées

| Outil | Rôle |
|---|---|
| Python 3.10+ | Langage principal |
| Flask | Framework web |
| Flask-SQLAlchemy | ORM et gestion de la base de données |
| Flasgger | Génération automatique de la documentation Swagger |
| SQLite | Base de données locale (fichier `blog.db`) |

---

## 3. Structure des fichiers

```
ApiRestFlask/
├── app.py            # Point d'entrée, factory Flask, Swagger, error handlers
├── config.py         # Configurations Development / Testing / Production
├── extensions.py     # Instance SQLAlchemy partagée
├── models.py         # Modèle ORM Article
├── routes.py         # Blueprint avec tous les endpoints /api/articles
├── requirements.txt  # Dépendances Python
└── blog.db           # Base de données SQLite (générée au premier lancement)
```

**`app.py`** — crée l'application Flask via `create_app()`, charge la configuration, initialise la base de données, enregistre le blueprint des routes, configure Swagger, et définit les gestionnaires d'erreur globaux (404, 405, 500). L'accès à `/` redirige automatiquement vers `/apidocs`.

**`config.py`** — contient trois classes de configuration (`DevelopmentConfig`, `TestingConfig`, `ProductionConfig`) héritant d'une base commune. La configuration active est choisie via la variable d'environnement `APP_ENV`.

**`extensions.py`** — contient uniquement l'instance `db = SQLAlchemy()`, partagée entre `models.py` et `routes.py` pour éviter les imports circulaires.

**`models.py`** — définit la table `articles` avec ses colonnes. La méthode `mise_dictonnaire()` sérialise un article en dictionnaire Python pour les réponses JSON.

**`routes.py`** — blueprint Flask contenant les 6 endpoints du projet. Inclut les helpers `ok()` / `err()` pour des réponses JSON uniformes et la fonction `valider_champs()` pour la validation des entrées.

---

## 4. Installation

Cloner le dépôt :

```bash
git clone https://github.com/DK-dorinal/ApiRestFlask
cd ApiRestFlask
```

Créer et activer un environnement virtuel (recommandé) :

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

## 5. Configuration

Trois environnements sont disponibles dans `config.py` :

| Environnement | Classe | Base de données |
|---|---|---|
| `development` (défaut) | `DevelopmentConfig` | `blog.db` (fichier local) |
| `testing` | `TestingConfig` | SQLite en mémoire |
| `production` | `ProductionConfig` | Variable `DATABASE_URL` |

Pour changer d'environnement :

```bash
# Linux / macOS
export APP_ENV=production

# Windows (PowerShell)
$env:APP_ENV = "production"
```

---

## 6. Lancement

```bash
python app.py
```

La console affiche :

```
  Blog API  ->  http://127.0.0.1:5000
  Swagger UI ->  http://127.0.0.1:5000/apidocs
```

La base de données `blog.db` est créée automatiquement au premier lancement. Ouvrir `http://127.0.0.1:5000` dans un navigateur redirige directement vers la documentation Swagger.

---

## 7. Documentation Swagger

L'interface Swagger UI est accessible à :

```
http://127.0.0.1:5000/apidocs
```

Elle liste tous les endpoints avec leurs paramètres, les formats JSON attendus et les codes de réponse. Il est possible d'envoyer des requêtes directement depuis cette interface sans avoir besoin de Postman.

---

## 8. Modèle de données — Article

Chaque article stocké en base contient les champs suivants :

| Champ | Type | Obligatoire | Description |
|---|---|---|---|
| `id` | entier | — | Identifiant unique, généré automatiquement |
| `titre` | chaîne (255) | oui | Titre de l'article |
| `contenu` | texte | oui | Corps de l'article |
| `auteur` | chaîne (100) | oui | Nom de l'auteur |
| `date` | datetime | — | Date de création, définie automatiquement |
| `categorie` | chaîne (100) | oui | Catégorie (ex. : Technologie, Sport) |
| `tags` | chaîne (500) | non | Tags séparés par des virgules (ex. : `"flask, python, api"`) |

Exemple de représentation JSON d'un article :

```json
{
    "id": 1,
    "titre": "Introduction à Flask",
    "contenu": "Flask est un micro-framework Python...",
    "auteur": "DK-dorinal",
    "date": "2024-06-15T14:30:00",
    "categorie": "Technologie",
    "tags": ["flask", "python", "api"]
}
```

Les tags sont stockés en base sous forme de chaîne CSV (`"flask, python, api"`) et retournés sous forme de tableau JSON dans toutes les réponses.

---

## 9. Endpoints de l'API

### Résumé

| Méthode | URL | Action |
|---|---|---|
| `POST` | `/api/articles` | Créer un article |
| `GET` | `/api/articles` | Lire tous les articles (filtrables) |
| `GET` | `/api/articles/<id>` | Lire un article par ID |
| `PUT` | `/api/articles/<id>` | Modifier un article |
| `DELETE` | `/api/articles/<id>` | Supprimer un article |
| `GET` | `/api/articles/search?query=texte` | Rechercher par titre ou contenu |
| `GET` | `/api/health` | Vérifier que l'API est active |

---

### POST /api/articles — Créer un article

Crée un nouvel article et le stocke en base de données. Retourne une confirmation avec l'ID généré.

**Corps de la requête (JSON) :**

| Champ | Type | Obligatoire |
|---|---|---|
| `titre` | string | oui |
| `contenu` | string | oui |
| `auteur` | string | oui |
| `categorie` | string | oui |
| `tags` | string | non |

**Exemple de requête :**

```json
{
    "titre": "Introduction à Flask",
    "contenu": "Flask est un micro-framework Python léger et extensible.",
    "auteur": "DK-dorinal",
    "categorie": "Technologie",
    "tags": "flask, python, api"
}
```

**Réponse (201) :**

```json
{
    "success": true,
    "message": "article cree avec success",
    "data": {
        "id": 1,
        "titre": "Introduction à Flask",
        "contenu": "Flask est un micro-framework Python léger et extensible.",
        "auteur": "DK-dorinal",
        "date": "2024-06-15T14:30:00",
        "categorie": "Technologie",
        "tags": ["flask", "python", "api"]
    }
}
```

**Erreurs possibles :** 400 (JSON invalide), 422 (champ obligatoire manquant ou vide).

---

### GET /api/articles — Lire tous les articles

Retourne la liste complète des articles, triés du plus récent au plus ancien. Accepte des filtres optionnels en paramètres de requête.

**Paramètres disponibles :**

| Paramètre | Type | Description |
|---|---|---|
| `categorie` | string | Filtre par catégorie (insensible à la casse, partiel) |
| `auteur` | string | Filtre par auteur (insensible à la casse, partiel) |
| `date` | string | Filtre par date au format `YYYY-MM-DD` |

**Exemples :**

```
GET /api/articles
GET /api/articles?categorie=Technologie
GET /api/articles?auteur=dorinal
GET /api/articles?categorie=Tech&date=2024-06-15
```

**Réponse (200) :**

```json
{
    "success": true,
    "message": "2 article(s) recupere(s).",
    "count": 2,
    "data": [
        {
            "id": 2,
            "titre": "Deuxième article",
            "auteur": "DK-dorinal",
            "date": "2024-06-16T10:00:00",
            "categorie": "Technologie",
            "tags": []
        },
        {
            "id": 1,
            "titre": "Introduction à Flask",
            "auteur": "DK-dorinal",
            "date": "2024-06-15T14:30:00",
            "categorie": "Technologie",
            "tags": ["flask", "python"]
        }
    ]
}
```

---

### GET /api/articles/\<id\> — Lire un article

Retourne toutes les informations d'un article identifié par son ID.

**Exemple :**

```
GET /api/articles/1
```

**Réponse (200) :**

```json
{
    "success": true,
    "message": "article recupere avec success",
    "data": {
        "id": 1,
        "titre": "Introduction à Flask",
        "contenu": "Flask est un micro-framework Python léger et extensible.",
        "auteur": "DK-dorinal",
        "date": "2024-06-15T14:30:00",
        "categorie": "Technologie",
        "tags": ["flask", "python", "api"]
    }
}
```

**Erreurs possibles :** 404 si l'article n'existe pas.

---

### PUT /api/articles/\<id\> — Modifier un article

Met à jour un article existant. Permet de modifier le titre, le contenu, la catégorie, les tags et l'auteur. Les quatre champs `titre`, `contenu`, `auteur` et `categorie` sont obligatoires. Le champ `tags` est optionnel.

**Exemple :**

```
PUT /api/articles/1
```

**Corps de la requête :**

```json
{
    "titre": "Introduction à Flask — mis à jour",
    "contenu": "Contenu révisé et enrichi.",
    "auteur": "DK-dorinal",
    "categorie": "Technologie",
    "tags": "flask, python, mise-a-jour"
}
```

**Réponse (200) :**

```json
{
    "success": true,
    "message": "article modifie avec success",
    "data": {
        "id": 1,
        "titre": "Introduction à Flask — mis à jour",
        "contenu": "Contenu révisé et enrichi.",
        "auteur": "DK-dorinal",
        "date": "2024-06-15T14:30:00",
        "categorie": "Technologie",
        "tags": ["flask", "python", "mise-a-jour"]
    }
}
```

**Erreurs possibles :** 404 (article introuvable), 400 (JSON invalide), 422 (validation échouée).

---

### DELETE /api/articles/\<id\> — Supprimer un article

Supprime l'article correspondant à l'ID fourni. Retourne les données de l'article supprimé en confirmation.

**Exemple :**

```
DELETE /api/articles/1
```

**Réponse (200) :**

```json
{
    "success": true,
    "message": "article supprime avec success",
    "data": {
        "id": 1,
        "titre": "Introduction à Flask",
        "contenu": "Flask est un micro-framework Python léger et extensible.",
        "auteur": "DK-dorinal",
        "date": "2024-06-15T14:30:00",
        "categorie": "Technologie",
        "tags": ["flask", "python", "api"]
    }
}
```

**Erreurs possibles :** 404 si l'article n'existe pas.

---

### GET /api/articles/search — Rechercher

Recherche des articles dont le **titre ou le contenu** contient le texte fourni. La recherche est insensible à la casse.

**Paramètre obligatoire :**

| Paramètre | Type | Description |
|---|---|---|
| `query` | string | Texte à rechercher dans le titre ou le contenu |

**Exemples :**

```
GET /api/articles/search?query=flask
GET /api/articles/search?query=micro-framework
```

**Réponse (200) :**

```json
{
    "success": true,
    "message": "1 article(s) trouve(s).",
    "data": [
        {
            "id": 1,
            "titre": "Introduction à Flask",
            "contenu": "Flask est un micro-framework Python léger et extensible.",
            "auteur": "DK-dorinal",
            "date": "2024-06-15T14:30:00",
            "categorie": "Technologie",
            "tags": ["flask", "python", "api"]
        }
    ]
}
```

**Erreurs possibles :** 400 si le paramètre `query` est absent.

---

### GET /api/health — Santé de l'API

Vérifie que l'API est en ligne. Utile pour les outils de monitoring.

**Réponse (200) :**

```json
{
    "status": "healthy",
    "app": "ApiRestFlask – Blog API"
}
```

---

## 10. Formats de réponse

Toutes les réponses de l'API suivent une structure JSON uniforme.

**Succès :**

```json
{
    "success": true,
    "message": "description de l'opération",
    "data": { ... }
}
```

**Erreur simple :**

```json
{
    "success": false,
    "message": "description de l'erreur"
}
```

**Erreur de validation (422) :**

```json
{
    "success": false,
    "message": "le titre, le contenu et l'auteur sont obligatoire",
    "errors": [
        "'categorie' est obligatoire."
    ]
}
```

Le champ `errors` est présent uniquement sur les erreurs de validation. Il liste chaque champ problématique séparément.

---

## 11. Codes HTTP utilisés

| Code | Signification | Cas d'utilisation dans ce projet |
|---|---|---|
| 200 | OK | Lecture, modification, suppression réussies |
| 201 | Created | Article créé avec succès |
| 400 | Bad Request | JSON invalide, paramètre de requête absent, format de date incorrect |
| 404 | Not Found | Article introuvable par ID |
| 405 | Method Not Allowed | Méthode HTTP non supportée sur la route |
| 422 | Unprocessable Entity | Champ obligatoire manquant ou vide |
| 500 | Internal Server Error | Erreur interne non prévue |

---

## 12. Bonnes pratiques appliquées

**Validation des entrées** — la fonction `valider_champs()` dans `routes.py` vérifie que tous les champs obligatoires sont présents et non vides avant toute écriture en base. Les erreurs de validation retournent le détail de chaque champ problématique dans un tableau `errors`.

**Codes HTTP corrects** — chaque réponse utilise le code HTTP approprié à la situation, conformément aux standards REST (voir section 11).

**Séparation des responsabilités** — le projet est découpé en couches distinctes : `models.py` pour la définition des données, `routes.py` pour la logique des endpoints, `config.py` pour la configuration, `extensions.py` pour les dépendances partagées, et `app.py` pour l'assemblage de l'application.

**Réponses JSON uniformes** — les helpers `ok()` et `err()` garantissent que toutes les réponses ont la même structure, qu'il s'agisse d'un succès ou d'une erreur.

**Gestionnaires d'erreur globaux** — les erreurs 404, 405 et 500 sont interceptées au niveau de l'application et retournent du JSON structuré, jamais du HTML.

**Insensibilité à la casse sur les filtres** — les filtres par `auteur` et `categorie` ainsi que la recherche par `query` utilisent `ilike`, ce qui évite de manquer des résultats à cause des majuscules.

---

## 13. Tester avec Postman

**Créer un article**

- Méthode : `POST`
- URL : `http://127.0.0.1:5000/api/articles`
- Headers : `Content-Type: application/json`
- Body (raw JSON) :

```json
{
    "titre": "Mon premier article",
    "contenu": "Ceci est le texte de l'article.",
    "auteur": "DK-dorinal",
    "categorie": "Technologie",
    "tags": "flask, python"
}
```

**Voir tous les articles**

- Méthode : `GET`
- URL : `http://127.0.0.1:5000/api/articles`

**Filtrer par catégorie et date**

- Méthode : `GET`
- URL : `http://127.0.0.1:5000/api/articles?categorie=Technologie&date=2024-06-15`

**Voir un article précis**

- Méthode : `GET`
- URL : `http://127.0.0.1:5000/api/articles/1`

**Modifier un article**

- Méthode : `PUT`
- URL : `http://127.0.0.1:5000/api/articles/1`
- Body (raw JSON) :

```json
{
    "titre": "Titre modifié",
    "contenu": "Contenu mis à jour.",
    "auteur": "DK-dorinal",
    "categorie": "Technologie"
}
```

**Supprimer un article**

- Méthode : `DELETE`
- URL : `http://127.0.0.1:5000/api/articles/1`

**Rechercher par titre ou contenu**

- Méthode : `GET`
- URL : `http://127.0.0.1:5000/api/articles/search?query=flask`

---

## 14. Variables d'environnement

| Variable | Valeur par défaut | Description |
|---|---|---|
| `APP_ENV` | `development` | Environnement actif : `development`, `testing` ou `production` |
| `SECRET_KEY` | `dev-secret-key-change-in-prod` | Clé secrète Flask. À remplacer obligatoirement en production. |
| `DATABASE_URL` | `sqlite:///blog.db` | URI de la base de données. En production, pointer vers PostgreSQL ou autre. |

---

Développé par DK-dorinal — https://github.com/DK-dorinal/ApiRestFlask
