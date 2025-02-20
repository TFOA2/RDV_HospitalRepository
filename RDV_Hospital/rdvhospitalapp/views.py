from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.template import loader
from django.core.validators import validate_email


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

def inscription(request,user):
    
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name',None)
        email = request.POST.get('email',None)
        specialite = request.POST.get('specialite',None)
        password = request.POST.get('password',None)
        repassword = request.POST.get('repassword',None)
        
        if validate_email(email)==False or password != repassword:
            error = True
            message = "Erreur d'authentification verifier vos informations"
            
        print(f"=="*4,"New User",name,email,specialite,password,repassword,"=="*4)
        context = {
            'error':error,
            'message':message,
            'user':user if specialite else None
        }
        return render(request,'inscription.html',context)
    
        
    context = {
        'user':user
    }
    
    return render(request, "inscription.html",context)

# def register(request):
#     error = False
#     message = ""
#     if request.method == "POST":
#         name = request.POST.get('name',None)
#         email = request.POST.get('email',None)
#         specialite = request.POST.get('specialite',None)
#         password = request.POST.get('password',None)
#         repassword = request.POST.get('repassword',None)
        
#         if validate_email(email)==False or password != repassword:
#             error = True
#             message = "Erreur d'authentification verifier vos informations"
            
#         print(f"=="*4,"New User",name,email,specialite,password,repassword,"=="*4)
#         context = {
#             'error':error,
#             'message':message,
#         }
#         return render(request,'inscription.html',context)
    
def ajoutPrendreRendezVous(request):
    
    return render(request, "patient/ajout.html")

def consultation(request):
    
    return render(request,"patient/consultation.html")

def urgence(request):
    
    return render(request,"patient/urgence.html")

def profil(request):
    
    return render(request,"patient/profil.html")