from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
from .models import Specialite, CustomUser, Specialite_User, Planning, RendezVous, Consultation
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.mail import send_mail
from campay.sdk import Client as campayClient # pour le mode de paiement
import random


def indexAccueil(request):
    name = {
        'firstname': ["TFOA2", "Junior", "Arnold", "Arthur", "Alfred"],
        'note':{
            'math':15,
            'Physique':14
            }
        }
    
    return render(request,'index.html')


def consultationDetail(request,id):
    consultation = Consultation.objects.get(id=id)
    specialiste_id = consultation.rendezVous.specialiste_id
    print(specialiste_id)
    
    specialite = Specialite_User.objects.get(specialiste_id=specialiste_id)
    print(specialite)
    print(specialite.specialite.titre)
    specialite_title = specialite.specialite.titre
    
    context = {
        'consultation':consultation,
        'specialite_title':specialite_title
    }
    return render(request,'detailConsultation.html',context)

def rendezVousDetail(request,id):
    rendezvous = RendezVous.objects.get(id=id)
    specialiste_id = rendezvous.specialiste_id
    print(specialiste_id)
    
    specialite = Specialite_User.objects.get(specialiste_id=specialiste_id)
    print(specialite)
    print(specialite.specialite.titre)
    specialite_title = specialite.specialite.titre
    
    context = {
        'rendezVous':rendezvous,
        'specialite_title':specialite_title
    }
    return render(request,'detailRendezvous.html',context)

def search(request):
    query = request.GET.get('q', '').strip()  # Récupère le terme de recherche

    if query:
        specialites = Specialite.objects.filter(
            Q(titre__icontains=query)
        ).distinct()  # Rechercher par spécialité
        
        medecins = CustomUser.objects.filter( 
            Q(name__icontains=query) & 
            Q(role_id=1)
        ).distinct()  # Rechercher par nom specialiste
        
        print(len(medecins),'taille de la recherche')
        
        specialistes = []
        
        if len(specialites) != 0:
            for specialite in specialites:
                spe = Specialite_User.objects.filter(specialite_id=specialite.id)
            
                print(spe,'ok')
            
                for medecin in spe:
                    specialistes.append(medecin)
                    
        else:
            print('in else')
            for specialite in medecins:
                spe = Specialite_User.objects.filter(specialiste_id=specialite.id)
            
                print(spe,'ok')
            
                for medecin in spe:
                    specialistes.append(medecin)
        
        print(specialistes)
        context = {
            'specialistes':specialistes
        }
        
        return render(request, 'patient/index.html',context)

    else:
        medecins = Specialite_User.objects.all()  # Si aucune recherche, afficher tous les médecins
        specialites = Specialite.objects.all()
        
    
        context = {
            'specialistes': medecins, 
            'specialites':specialites,
            'query': query
        }

        return render(request, 'patient/index.html',context)
    
    

# Function patient

@login_required
def dashboardPatient(request):
    print(request.user)
    specialistes = Specialite_User.objects.all()
    specialites = Specialite.objects.all()
    print(specialistes)
    
    context = {
        'specialistes':specialistes,
        'specialites':specialites
    }
    return render(request,'patient/index.html',context)

@login_required  
def ajoutPrendreRendezVous(request):
    specialistes = Specialite_User.objects.all()   
    
    specialiste_id = request.GET.get('specialiste_id', '')
    specialiste_name = request.GET.get('specialiste_name', '')
    specialiste_titre = request.GET.get('specialiste_titre', '')
    context = {
        'specialistes':specialistes,
        'selected_specialiste_id': specialiste_id,
        'selected_specialiste_name': specialiste_name,
        'selected_specialiste_titre': specialiste_titre,
    }
    
    if request.method == 'POST':
        specialiste = request.POST.get('specialiste',None)
        date = request.POST.get('date',None)
        heure = request.POST.get('heure',None)
        motif = request.POST.get('motif',None)
        type = request.POST.get('type',None)
        
        heureDebut,heureFin = heure.split('-')
        print('=='*4,date,'=='*4)
        print('=='*4,heure,'=='*4)
        print('=='*4,heureDebut,'=='*4)
        print('=='*4,heureFin,'=='*4)
        print('=='*4,request.user.name,'=='*4)
        print('=='*4,request.user.email,'=='*4)
        print('=='*4,request.user.phone,'=='*4)
        
        rendezVous = RendezVous(patient_id=request.user.id,specialiste_id=specialiste,date=date,heureDebut=heureDebut,heureFin=heureFin ,motif=motif,type=type,status=0)
        rendezVous.save()
        
        
        planning = get_object_or_404(Planning,specialiste_id=specialiste,date=date,heure_debut=heureDebut,heure_fin=heureFin)
        print(planning)
        planning.status = 1
        planning.save()
        
        specialisteName = CustomUser.objects.get(id=specialiste)
        message = f"""
        Bonjour {request.user.name},
        
        Votre rendez-vous avec le spécialiste a bien été confirmé.
        Motif: {motif}
        
        📅 Date : {date}
        ⏰ Heure : {heure}
        🏥 Spécialiste : Dr. {specialisteName.name}
        
        Merci de votre confiance !
        """
        
        send_mail(
            'Confirmation de rendez-vous', # subject
            message, #message
            'fokouongsirus11@gmail.com', # expediteur
            ['tfoarnold@gmail.com'] # desitinataire
            
        )
        return redirect('store')
       
        
    return render(request, "patient/ajout.html", context)

def get_disponibilites(request, specialiste_id):
    disponibilites = Planning.objects.filter(specialiste_id=specialiste_id, status=0).values("date", "heure_debut","heure_fin")
    print(disponibilites)
    return JsonResponse(list(disponibilites), safe=False)

@login_required
def consultation(request):
    consultations = Consultation.objects.filter(rendezVous__patient_id=request.user.id)
    context = {
        'consultations':consultations
    }
    return render(request,"patient/consultation.html",context)

def rendezVous(request):
    
    rendezvous = RendezVous.objects.filter(patient_id=request.user.id)
    context = {
        'rendezVous':rendezvous
    }
    
    return render(request,'patient/rendez-vous.html',context)

@login_required
def urgence(request):
    
    return render(request,"patient/urgence.html")

@login_required
def profil(request):
    
    return render(request,"patient/profil.html")

@login_required
def join_room(request):
    if request.method == 'POST':
        roomID = request.POST['roomID']
        return redirect("/meeting?roomID=" + roomID)
    return render(request, 'patient/joinRoom.html')
# end function patient



# Funtcion professionnel sante

@login_required
def dashboardSpecialiste(request):
    plannings = Planning.objects.all()
    context = {
        'plannings':plannings,
    }
    return render(request,'proSante/index.html',context)
    
@login_required
def planning(request):
    if request.method == 'POST':
        
        date = request.POST.get('date',None)
        heureDebut = request.POST.get('heureDebut', None)
        heureFin = request.POST.get('heureFin', None)
        
        planning = Planning(specialiste_id=request.user.id,date=date, heure_debut=heureDebut, heure_fin=heureFin)
        planning.save()
        
        return redirect('planning')
    
    plannings = Planning.objects.all()
    context = {
        'plannings': plannings
    }
    
    return render(request,'proSante/planning.html',context)

def rendezVousSpecialiste(request):
    
    rendezvous = RendezVous.objects.filter(specialiste_id=request.user.id)
    context = {
        'rendezVous':rendezvous
    }
    
    return render(request,'proSante/rendez-vous.html',context)

def consultationSpecialiste(request):
    if request.method == 'POST':
        rdv = request.POST.get('rendezvous')
        ordonance = request.POST.get('ordonance')
        diagnostic = request.POST.get('diagnostic')
        
        print(f"=="*4,"New User",rdv,ordonance,diagnostic,"=="*4)
        
        consultation = Consultation(rendezVous_id=rdv,diagnostique=diagnostic, ordonance=ordonance)
        consultation.save()
        
        rendezvous = RendezVous.objects.get(id=rdv)
        rendezvous.status = 1
        rendezvous.save()
        
        return redirect('consultationspecialaite')
    
    rdv = RendezVous.objects.filter(Q(specialiste_id=request.user.id) & Q(status=0))
    consultations = Consultation.objects.filter(rendezVous__specialiste_id=request.user.id)
    print(consultations)
    
    context ={
        'rendezvous':rdv,
        'consultations':consultations
    }
    return render(request,'proSante/consultation.html',context)

def delete(request,id,table):
    if table == 'planning':
        planning = Planning.objects.get(id=id)
        if planning.status == 1:
            raison = request.GET.get('raison', '')
            
            message = f"""
            Bonjour {request.user.name},
        
            Le crenau que vous avez reservez date: {planning.date}, heure: {planning.heure_debut} - {planning.heure_fin}  a été annuler.
            Pour la raison suivante: {raison}
            
        
            Merci de votre confiance !
            """
        
            send_mail(
            'Annulation du planning', # subject
            message, #message
            'fokouongsirus11@gmail.com', # expediteur
            ['tfoarnold@gmail.com'] # desitinataire
            
            )
            print(planning,raison)
            planning.delete()
            
        else:
            planning.delete()
        return redirect('planning')
    
    elif table == 'rendezvous':
        rendezvous = RendezVous.objects.get(id=id)
        if rendezvous.status == 0:
            raison = request.GET.get('raison', '')
            message = f"""
            Bonjour,
        
            Le rendez-vous ayant comme Motif: {rendezvous.motif} a été annuler.
            Pour la raison suivante: {raison}
            
        
            Merci de votre confiance !
            """
        
            send_mail(
            'Annulation de rendez-vous', # subject
            message, #message
            'fokouongsirus11@gmail.com', # expediteur
            ['tfoarnold@gmail.com'] # desitinataire
            
            )
            print(rendezvous,raison)
            rendezvous.delete()
        else:
            rendezvous.delete()
        
        if request.user.role.titre == 'specialiste':
            return redirect('rendezVousSpecialiste')
        if request.user.role.titre == 'patient':
            return redirect('rendezVousPatient')
    


@login_required
def videocall(request):
    room_id = str(random.randint(1000, 9999))
    
    message = f"""
    Bonjour,
    
    Votre rendez-vous en ligne est confirmé !

    📌 Identifiant de la consultation en ligne : {room_id}

    Merci de votre confiance !
    """
        
    send_mail(
        'Teleconsultation', # subject
        message, #message
        'fokouongsirus11@gmail.com', # expediteur
        ['tfoarnold@gmail.com'] # desitinataire
        
    )
    context={
        'name':request.user.name,
        'roomId':room_id,
    }
    return render(request,'proSante/videocall.html',context)
   
# end function professionnel sante

# Function authentification
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
        print(f"=="*4,"New User",name,email,specialite,password,repassword,"=="*4)
        
        newUser.save()
        
        if user == 'specialiste':
            specialiteUser = Specialite_User(specialite_id=specialite, specialiste_id=newUser.id)
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

@login_required
def deconnexion(request):
    print(request.user)
    print(request.user.is_authenticated)
    logout(request)
    
    return redirect('connexion')
# end function authentification  
  

# function de paiement
def initPaiement(request):
    from campay.sdk import Client as CamPayClient

    campay = CamPayClient({
        "app_username" : "uJ_cD0nMLoowI3IzKij-dBovM4TK5kz_wd2DHRd1O0YXXAyrCU5MzF7BtMaUDMwRtJwpDybDddRpBdtZOE4Hmg",
        "app_password" : "6VnkEbim9P37fI1eGhbWyoFCRnys1ntOdbd9KHwNvRtnxZRccvBGtX3ba2kWy0AmrTlXU7uTsX2fcEslI4XbaA",
        "environment" : "DEV" #use "DEV" for demo mode or "PROD" for live mode
    })
    
    collect = campay.collect({
        "amount": "5", #The amount you want to collect
        "currency": "XAF",
        "from": "2376xxxxxxxx", #Phone number to request amount from. Must include country code
        "description": "some description",
        "external_reference": "", #Reference from the system initiating the transaction.
      })

    print(collect)
    #{"reference": "bcedde9b-62a7-4421-96ac-2e6179552a1a", "external_reference":"12345678",

