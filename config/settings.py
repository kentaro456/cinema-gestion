"""
Réglages Django du projet de gestion de cinéma.

Les valeurs sensibles (clé secrète, mode debug, base de données...) sont lues
dans les variables d'environnement, éventuellement chargées depuis un fichier
`.env` placé à la racine du projet (voir `.env.example`).
"""

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Charge le fichier .env s'il existe (sans écraser les variables déjà définies).
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    """Lit une variable d'environnement booléenne (true/false, 1/0, yes/no, on/off)."""
    value = os.environ.get(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(name, default=""):
    """Lit une liste séparée par des virgules dans une variable d'environnement."""
    raw = os.environ.get(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# --------------------------------------------------------------------------
# Sécurité
# --------------------------------------------------------------------------

# En production, DJANGO_SECRET_KEY doit être définie. La valeur ci-dessous
# ne sert que pour le développement local.
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "dev-only-insecure-key-a-remplacer-avant-la-production",
)

DEBUG = env_bool("DJANGO_DEBUG", default=True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", default="localhost,127.0.0.1")


# --------------------------------------------------------------------------
# Applications
# --------------------------------------------------------------------------

INSTALLED_APPS = [
    # Applications Django natives
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Applications métier du projet (une par domaine fonctionnel)
    "core",          # accueil, templates communs, navigation, connexion
    "films",         # gestion des films (tâche 4.2)
    "salles",        # gestion des salles (module attribué à un autre membre)
    "seances",       # programmation des séances (tâche 4.2)
    "billetterie",   # ventes et billets (module attribué à un autre membre)
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # Dossier global "templates/" à la racine (base.html, navigation...).
        # Les templates propres à chaque app sont dans <app>/templates/.
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# --------------------------------------------------------------------------
# Base de données
# --------------------------------------------------------------------------
# SQLite par défaut (aucune installation nécessaire).
# Pour passer à PostgreSQL : DJANGO_DB_ENGINE=postgresql + variables POSTGRES_*
# (voir README.md, section "Passer à PostgreSQL").

DB_ENGINE = os.environ.get("DJANGO_DB_ENGINE", "sqlite").lower()

if DB_ENGINE == "postgresql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.environ.get("POSTGRES_DB", "cinema"),
            "USER": os.environ.get("POSTGRES_USER", "cinema"),
            "PASSWORD": os.environ.get("POSTGRES_PASSWORD", ""),
            "HOST": os.environ.get("POSTGRES_HOST", "localhost"),
            "PORT": os.environ.get("POSTGRES_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# --------------------------------------------------------------------------
# Validation des mots de passe
# --------------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------------------------------
# Internationalisation : interface en français, heure de Paris
# --------------------------------------------------------------------------

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = "Europe/Paris"
USE_I18N = True
USE_TZ = True


# --------------------------------------------------------------------------
# Fichiers statiques (CSS, JavaScript, images)
# --------------------------------------------------------------------------

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"  # utilisé par `collectstatic` en production


# --------------------------------------------------------------------------
# Authentification
# --------------------------------------------------------------------------

LOGIN_URL = "login"                 # nom de l'URL de connexion (core)
LOGIN_REDIRECT_URL = "home"         # après connexion : tableau de bord
LOGOUT_REDIRECT_URL = "home"        # après déconnexion


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
