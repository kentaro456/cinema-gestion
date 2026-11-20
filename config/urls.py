"""
Routage principal du projet.

Chaque application fournit son propre fichier `urls.py` ; ici on les rattache
à un préfixe. Pour ajouter un module, il suffit de décommenter / ajouter une
ligne `path(...)` ci-dessous.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),              # accueil, connexion, déconnexion
    path("films/", include("films.urls")),       # tâche 4.2
    path("salles/", include("salles.urls")),     # module salles
    path("seances/", include("seances.urls")),   # tâche 4.2
    path("billetterie/", include("billetterie.urls")),  # module billetterie
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
