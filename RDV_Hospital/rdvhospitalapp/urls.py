from django.urls import path
from . import views

urlpatterns = [
    path('',views.indexAccueil,name="accueil"),
    path('detail_consultation/<int:id>/',views.consultationDetail,name="detail_consultation"),
    path('detail_rendezvous/<int:id>/',views.rendezVousDetail,name="detail_rendezvous"),
    path('search/', views.search, name='search'),
    
    # route patient
    path('dashboard/patient',views.dashboardPatient,name="dashboardpatient"),
    path('prendre_rendez-vous/',views.ajoutPrendreRendezVous,name="store"),
    path('consultation/',views.consultation,name="consultaion"),
    path('rendez-vous/',views.rendezVous,name="rendezVousPatient"),
    path('urgence/',views.urgence),
    path('profil/',views.profil),
    path('join/',views.join_room, name='join_room'),
    # end route patient
    
    # route professionnel sante
    path('dashboard/specialiste',views.dashboardSpecialiste,name="dashboardspecialiste"),
    path('planning/',views.planning, name="planning"),
    path('delete/<str:table>/<int:id>/',views.delete, name="delete"),
    path("get-disponibilites/<int:specialiste_id>/", views.get_disponibilites, name="get_disponibilites"),
    path('rendez-vous specialiste/',views.rendezVousSpecialiste,name="rendezVousSpecialiste"),
    path('consultation specialiste/',views.consultationSpecialiste,name="consultationspecialaite"),
    path('meeting/', views.videocall, name='meeting'),
    # end route professionnel sante
    
    # route authentification
    path('choixUtilisateur/',views.choixUtilisateur),
    path('connexion/',views.connexion,name="connexion"),
    path('inscription/<str:user>/',views.inscription,name="inscription"),
    path('deconnexion/',views.deconnexion,name='deconnexion'),
    # end route authentification
    
    
    
    
]
