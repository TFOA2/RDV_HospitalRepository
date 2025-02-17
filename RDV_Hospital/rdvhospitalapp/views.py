from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def indexAccueil(request):
    template = loader.get_template("index.html")
    name = {
        'firstname': ["TFOA2", "Junior", "Arnold", "Arthur", "Alfred"],
        'note':{
            'math':15,
            'Physique':14
            }
        }
    
    return HttpResponse(template.render(name,request))

def dashboard(request):
    
    return render(request,'patient/index.html')

def choixUtilisateur(request):
    
    return render(request,'userChoice.html')

def connexion(request):
    
    return render(request, "connexion.html")

def inscription(request,type):
    context = {
        'type':type
    }
    
    return render(request, "inscription.html",context)
    
def ajoutPrendreRendezVous(request):
    
    return render(request, "patient/ajout.html")

def consultation(request):
    
    return render(request,"patient/consultation.html")

def urgence(request):
    
    return render(request,"patient/urgence.html")

def profil(request):
    
    return render(request,"patient/profil.html")