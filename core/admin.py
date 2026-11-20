"""
Configuration de l'interface d'administration Django du projet.

Chaque application enregistre ses propres modèles dans son fichier admin.py.
Ce fichier-ci ne règle que le titre général de l'administration.
"""
from django.contrib import admin

admin.site.site_header = "Administration – Gestion de cinéma"
admin.site.site_title = "Cinéma – Administration"
admin.site.index_title = "Tableau de bord de l'administration"
