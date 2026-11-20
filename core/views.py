from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    """
    Tableau de bord simple : accueil après connexion.

    Les compteurs réels (films, salles, séances, ventes) seront branchés
    par les modules correspondants. Pour l'instant, la page présente
    l'état de chaque module du projet.
    """
    modules = [
        {"nom": "Films", "description": "Titres et durées des films", "statut": "À venir (tâche 4.2)", "url_name": None},
        {"nom": "Salles", "description": "Salles et capacités", "statut": "Structure prête", "url_name": None},
        {"nom": "Séances", "description": "Programmation et conflits d'horaires", "statut": "À venir (tâche 4.2)", "url_name": None},
        {"nom": "Billetterie", "description": "Ventes, règlements et billets", "statut": "Structure prête", "url_name": None},
    ]
    context = {
        "modules": modules,
        "titre_page": "Tableau de bord",
    }
    return render(request, "core/home.html", context)
