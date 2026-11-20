from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration de l'application « Core (accueil, navigation, connexion) »."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Core (accueil, navigation, connexion)"
