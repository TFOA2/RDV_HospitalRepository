from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from .models import Specialite, CustomUser, Specialite_User
from django.contrib.auth.decorators import login_required


def indexAccueil(request):
    name = {
        'firstname': ["TFOA2", "Junior", "Arnold", "Arthur", "Alfred"],
        'note':{
            'math':15,
            'Physique':14
            }
        }
    
    return render(request,'index.html')

@login_required
def dashboardPatient(request):
    print(request.user)
    return render(request,'patient/index.html')

@login_required
def dashboardSpecialiste(request):
    
    return render(request,'proSante/index.html')

def choixUtilisateur(request):
    
    return render(request,'userChoice.html')

def connexion(request):
    if request.method == 'POST':
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        user = authenticate(request,email=email, password=password)
        # print(user.role.titre)
        print(request.user.is_authenticated)
        # 1 => specialiste et 2 => patient 
        if user is not None:
            print(user)
            login(request, user)
            if user.role.titre == 'specialiste':
                return redirect('dashboardspecialiste')
            elif user.role.titre == 'patient':
                return redirect('dashboardpatient')
        else:
           render(request, "connexion.html") 
    
    return render(request, "connexion.html")

def inscription(request,user):
    
    error = False
    message = ""
    if request.method == "POST":
        name = request.POST.get('name',None)
        email = request.POST.get('email',None)
        phone = request.POST.get('phone',None)
        specialite = request.POST.get('specialite',None)
        password = request.POST.get('password',None)
        repassword = request.POST.get('repassword',None)
        role = 1 if user == 'specialiste' else 2
        
        if validate_email(email)==False or password != repassword:
            error = True
            message = "Erreur d'authentification verifier vos informations"
            
            context = {
            'error':error,
            'message':message,
            'user':user if specialiste else None,
            }
            return render(request,'inscription.html',context)
            
        print(f"=="*4,"New User",name,email,specialite,password,repassword,"=="*4)
        
        newUser = CustomUser.objects.create_user(name=name, email=email, password=password, phone=phone, role_id=role)
        newUser.save()
        
        if user == 'specialiste':
            specialiteUser = Specialite_User(spacialite_id=specialite, specialiste_id=newUser.id)
            specialiteUser.save()
        
        context = {
            'user':user
        }
        return redirect('connexion')
        
    
    specialites = Specialite.objects.all() 
    context = {
        'user':user,
        'specialites':specialites
    }
    
    return render(request, "inscription.html",context)

# @login_required
def deconnexion(request):
    print(request.user)
    print(request.user.is_authenticated)
    logout(request)
    
    return redirect('connexion')
  
@login_required  
def ajoutPrendreRendezVous(request):
    specialistes = Specialite_User.objects.all()    
    context = {
        'specialistes':specialistes
    }
    return render(request, "patient/ajout.html", context)

@login_required
def consultation(request):
    
    return render(request,"patient/consultation.html")

@login_required
def urgence(request):
    
    return render(request,"patient/urgence.html")

@login_required
def profil(request):
    
    return render(request,"patient/profil.html")