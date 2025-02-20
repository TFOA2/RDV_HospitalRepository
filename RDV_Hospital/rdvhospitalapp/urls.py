from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexAccueil,name="accueil"),
    path('dashboard/',views.dashboard,name="dashboard"),
    path('choixUtilisateur/',views.choixUtilisateur),
    path('connexion/',views.connexion,name="dashboardPatient"),
    path('inscription/<str:user>/',views.inscription,name="inscription"),
    path('prendre_rendez-vous/',views.ajoutPrendreRendezVous,name="store"),
    path('consultation/',views.consultation),
    path('urgence/',views.urgence),
    path('profil/',views.profil),
    
]
