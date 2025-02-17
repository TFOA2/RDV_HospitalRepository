from django.urls import path
from .views import indexAccueil,dashboard,connexion,inscription,choixUtilisateur,ajoutPrendreRendezVous,consultation,urgence,profil

urlpatterns = [
    path('',indexAccueil,name="accueil"),
    path('dashboard/',dashboard,name="dashboard"),
    path('choixUtilisateur/',choixUtilisateur),
    path('connexion/',connexion,name="dashboardPatient"),
    path('inscription/<int:type>/',inscription,name="inscription"),
    path('prendre_rendez-vous/',ajoutPrendreRendezVous,name="store"),
    path('consultation/',consultation),
    path('urgence/',urgence),
    path('profil/',profil),
    
]
