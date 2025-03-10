from django.db import models
from django.conf import settings
# Create your models here.


from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    """Manager personnalisé pour le modèle CustomUser"""

    def create_user(self, email, password=None, **extra_fields):
        """Créer un utilisateur normal"""
        if not email:
            raise ValueError("L'email est obligatoire")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Créer un superutilisateur"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    titre = models.CharField(max_length=50)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Modèle utilisateur personnalisé avec email comme identifiant principal"""

    email = models.EmailField(unique=True)  # Champ unique pour l'authentification
    name = models.CharField(max_length=50)
    phone = models.IntegerField()
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # Permet l'accès à l'admin

    objects = CustomUserManager()  # Associe le manager personnalisé

    USERNAME_FIELD = 'email'  # Définit l'email comme identifiant principal
    REQUIRED_FIELDS = []  # Pas besoin d'un username, donc cette liste reste vide

    def __str__(self):
        return self.email




    
class Specialite(models.Model):
    titre = models.CharField(max_length=50)
    
class Specialite_User(models.Model):
    specialite = models.ForeignKey(Specialite, on_delete=models.CASCADE)
    specialiste = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class Planning(models.Model):
    specialiste = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField( auto_now=False, auto_now_add=False)
    heure_debut = models.TimeField( auto_now=False, auto_now_add=False)
    heure_fin = models.TimeField( auto_now=False, auto_now_add=False)
    status = models.IntegerField(default=0)
    
class Paiement(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    montant = models.IntegerField()
    mode_paiement = models.CharField(max_length=50)
    
class Urgence(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='urgence_patient')
    specialiste = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='urgence_specialiste')
    motif = models.CharField(max_length=150)
    description = models.CharField(max_length=250)
    
class RendezVous(models.Model):
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rendezvous_patient')
    specialiste = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='rendezvous_specialiste')
    motif = models.CharField(max_length=150)
    date = models.DateField()
    heureDebut = models.TimeField()
    heureFin = models.TimeField()
    type = models.BooleanField()
    status = models.IntegerField(default=0)
    
class Consultation(models.Model):
    rendezVous = models.ForeignKey(RendezVous, on_delete=models.CASCADE)
    diagnostique = models.CharField(max_length=250)
    ordonance = models.CharField(max_length=50)
    
