from django.db import models
from django.conf import settings
# Create your models here.


# from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
# from django.db import models

# class CustomUserManager(BaseUserManager):
#     """Manager personnalisé pour le modèle CustomUser"""

#     def create_user(self, email, password=None, **extra_fields):
#         """Créer un utilisateur normal"""
#         if not email:
#             raise ValueError("L'email est obligatoire")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         """Créer un superutilisateur"""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         return self.create_user(email, password, **extra_fields)


# class CustomUser(AbstractBaseUser, PermissionsMixin):
#     """Modèle utilisateur personnalisé avec email comme identifiant principal"""

#     email = models.EmailField(unique=True)  # Champ unique pour l'authentification
#     first_name = models.CharField(max_length=50, blank=True)
#     last_name = models.CharField(max_length=50, blank=True)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)  # Permet l'accès à l'admin

#     objects = CustomUserManager()  # Associe le manager personnalisé

#     USERNAME_FIELD = 'email'  # Définit l'email comme identifiant principal
#     REQUIRED_FIELDS = []  # Pas besoin d'un username, donc cette liste reste vide

#     def __str__(self):
#         return self.email




class Role(models.Model):
    title = models.CharField(max_length=50)
    
class Specialite(models.Model):
    titre = models.CharField(max_length=50)
    
class Specialite_User(models.Model):
    spacialite_id = models.ForeignKey(Specialite, on_delete=models.CASCADE)
    specialiste_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
class Planning(models.Model):
    id_specialiste = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    disponibilite = models.DateTimeField()
    
class Consultation(models.Model):
    patient_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultation_patient')
    specialiste_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='consultation_specialiste')
    diagnostique = models.CharField(max_length=250)
    ordonance = models.CharField(max_length=50)
    
class Paiement(models.Model):
    patient_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    montant = models.IntegerField()
    mode_paiement = models.CharField(max_length=50)
    
class Urgence(models.Model):
    patient_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='urgence_patient')
    specialiste_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='urgence_specialiste')
    motif = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    
