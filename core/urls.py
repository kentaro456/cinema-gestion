"""
Routes du socle : accueil, connexion et déconnexion.

L'authentification repose entièrement sur les vues natives de Django
(django.contrib.auth.views) : aucune logique de mot de passe n'est recodée.
"""
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("connexion/", auth_views.LoginView.as_view(template_name="registration/login.html"), name="login"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
]
