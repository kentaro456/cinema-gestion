"""
Enregistrement des modèles de « Séances » dans l'interface d'administration.

Exemple (à décommenter quand un modèle existe) :
    from django.contrib import admin
    from .models import MonModele

    @admin.register(MonModele)
    class MonModeleAdmin(admin.ModelAdmin):
        list_display = ("id",)
"""
from django.contrib import admin  # noqa: F401
