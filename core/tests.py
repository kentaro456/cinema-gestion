"""
Tests du socle technique.

Ils vérifient que le projet démarre, que les applications sont bien
déclarées, que l'accueil est protégé, et que la connexion / déconnexion
fonctionne avec l'authentification native de Django.
"""
from django.apps import apps
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

EXPECTED_APPS = ["core", "films", "salles", "seances", "billetterie"]


class SocleStructureTests(TestCase):
    """Le projet et ses applications métier sont correctement déclarés."""

    def test_applications_metier_installees(self):
        for nom in EXPECTED_APPS:
            with self.subTest(app=nom):
                self.assertTrue(apps.is_installed(nom))

    def test_routes_nommees_disponibles(self):
        self.assertEqual(reverse("home"), "/")
        self.assertEqual(reverse("login"), "/connexion/")
        self.assertEqual(reverse("logout"), "/deconnexion/")

    def test_administration_accessible(self):
        response = self.client.get("/admin/login/")
        self.assertEqual(response.status_code, 200)


class AccueilTests(TestCase):
    """Le tableau de bord n'est visible qu'après connexion."""

    @classmethod
    def setUpTestData(cls):
        cls.utilisateur = get_user_model().objects.create_user(
            username="test_gerant",
            password="Mot-de-passe-test-42!",
        )

    def test_accueil_redirige_vers_connexion_si_anonyme(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_accueil_accessible_une_fois_connecte(self):
        self.client.force_login(self.utilisateur)
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/home.html")
        self.assertTemplateUsed(response, "base.html")
        self.assertContains(response, "Tableau de bord")


class ConnexionTests(TestCase):
    """Connexion et déconnexion avec l'authentification native de Django."""

    @classmethod
    def setUpTestData(cls):
        cls.mot_de_passe = "Mot-de-passe-test-42!"
        cls.utilisateur = get_user_model().objects.create_user(
            username="test_caissier",
            password=cls.mot_de_passe,
        )

    def test_page_connexion_affichee(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

    def test_connexion_valide_redirige_vers_accueil(self):
        response = self.client.post(
            reverse("login"),
            {"username": "test_caissier", "password": self.mot_de_passe},
        )
        self.assertRedirects(response, reverse("home"))

    def test_connexion_invalide_reste_sur_la_page(self):
        response = self.client.post(
            reverse("login"),
            {"username": "test_caissier", "password": "mauvais"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_deconnexion_par_post_redirige_vers_accueil(self):
        self.client.force_login(self.utilisateur)
        response = self.client.post(reverse("logout"))
        self.assertRedirects(response, reverse("home"), fetch_redirect_response=False)
        # Après déconnexion, l'accueil redemande la connexion.
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 302)
