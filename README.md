# Cinéma – Gestion (socle technique)

Application interne de gestion de cinéma : films, salles, séances, billetterie et consultation des ventes.
Projet de groupe – Master 2 CPI, Université Paris 8.

Ce dépôt contient le **socle technique** (tâche 4.1) : il fournit la structure commune sur laquelle chaque membre de l'équipe branche son module.

---

## 1. Stack technique

| Élément | Choix |
|---|---|
| Backend | Python 3.13 (3.11+ compatible) · Django 5.2 LTS |
| Frontend | Django Templates · HTML · CSS · Bootstrap 5.3 |
| Base de données | SQLite (par défaut), PostgreSQL possible |
| Langue de l'interface | Français |

Aucun framework JavaScript (pas de React ni Vue).

## 2. Arborescence

```
cinema-gestion/
├── manage.py                 # point d'entrée des commandes Django
├── requirements.txt          # dépendances Python figées
├── .env.example              # modèle de configuration (sans secret)
├── .gitignore
├── README.md
├── config/                   # réglages globaux du projet
│   ├── settings.py           # configuration (lit le fichier .env)
│   ├── urls.py               # routage principal
│   ├── wsgi.py / asgi.py
├── core/                     # socle : accueil, connexion, navigation, admin
│   ├── views.py              # tableau de bord
│   ├── urls.py               # /, /connexion/, /deconnexion/
│   ├── admin.py              # titre de l'administration
│   └── tests.py              # tests du socle
├── films/                    # module films (tâche 4.2)
├── salles/                   # module salles (autre membre)
├── seances/                  # module séances (tâche 4.2)
├── billetterie/              # module billetterie (autre membre)
├── templates/                # templates communs
│   ├── base.html             # gabarit de base (Bootstrap)
│   ├── includes/navbar.html  # barre de navigation
│   ├── core/home.html        # tableau de bord
│   └── registration/login.html
└── static/                   # fichiers statiques communs
    └── css/style.css
```

**Règle d'intégration :** chaque module vit dans sa propre application Django. Il ajoute ses modèles dans `models.py`, ses vues dans `views.py`, ses routes dans `urls.py` (déjà branchées dans `config/urls.py`) et ses templates dans `templates/<app>/` (ou `<app>/templates/<app>/`). Il ne modifie pas le code des autres modules.

## 3. Installation

Depuis le dossier du projet, dans un terminal PowerShell (Windows) :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
copy .env.example .env
```

Sous macOS / Linux : `python3 -m venv .venv`, puis `source .venv/bin/activate`, puis `pip install -r requirements.txt` et `cp .env.example .env`.

Modifier ensuite `.env` si besoin (la clé secrète par défaut ne doit pas être utilisée en production).

## 4. Migrations et lancement

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Puis ouvrir <http://127.0.0.1:8000/>.

- Tableau de bord : <http://127.0.0.1:8000/> (après connexion)
- Connexion : <http://127.0.0.1:8000/connexion/>
- Administration : <http://127.0.0.1:8000/admin/>

## 5. Tests

```powershell
python manage.py check
python manage.py test
```

## 6. Passer à PostgreSQL (optionnel)

1. Installer PostgreSQL et créer la base `cinema` et l'utilisateur correspondant.
2. Décommenter `psycopg[binary]` dans `requirements.txt`, puis `pip install -r requirements.txt`.
3. Dans `.env` : `DJANGO_DB_ENGINE=postgresql` et renseigner les variables `POSTGRES_*`.
4. Relancer `python manage.py migrate`.

## 7. Mise en production (rappel)

- `DJANGO_DEBUG=false`, une vraie `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS` renseigné.
- `python manage.py collectstatic` pour générer `staticfiles/`.

## 8. Travailler en équipe avec Git

Ne jamais committer `.env`, `db.sqlite3` ni `.venv/` : ils sont exclus par `.gitignore`.
