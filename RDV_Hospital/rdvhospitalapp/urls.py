from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexAccueil,name="accueil"),
    path('dashboard/patient',views.dashboardPatient,name="dashboardpatient"),
    path('dashboard/specialiste',views.dashboardSpecialiste,name="dashboardspecialiste"),
    path('choixUtilisateur/',views.choixUtilisateur),
    path('connexion/',views.connexion,name="connexion"),
    path('inscription/<str:user>/',views.inscription,name="inscription"),
    path('deconnexion/',views.deconnexion,name='deconnexion'),
    path('prendre_rendez-vous/',views.ajoutPrendreRendezVous,name="store"),
    path('consultation/',views.consultation),
    path('urgence/',views.urgence),
    path('profil/',views.profil),
    
]
