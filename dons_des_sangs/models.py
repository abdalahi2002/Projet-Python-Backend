from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
import uuid
from django.utils import timezone

# Create your models here.
# la model Wilaya
def validate_mauritanian_wilaya_name(value):
    allowed_wilayas = [
        "Adrar", "Assaba", "Brakna", "Dakhlet Nouadhibou", "Gorgol",
        "Guidimaka", "Hodh Ech Chargui", "Hodh El Gharbi", "Inchiri", 
        "Nouakchott-Nord", "Nouakchott-Ouest", "Nouakchott-Sud", 
        "Tagant", "Tiris Zemmour", "Trarza"
    ]
    if value.capitalize() not in map(str.capitalize, allowed_wilayas):
        raise ValidationError(f"Le nom de la wilaya doit être l'un des suivants : {', '.join(allowed_wilayas)}")


class Wilaya(models.Model):
    nom = models.CharField(max_length=100, primary_key=True, validators=[validate_mauritanian_wilaya_name])  # Utilisation du nom comme clé primaire
    id = None  # Désactivation de l'attribut id
    def __str__(self):
        return self.nom


#la model Type de Sang
def validate_type_sang(value):
    allowed_type_sang = ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]
    if value.upper() not in allowed_type_sang:
        raise ValidationError(f"Le type de sang doit être l'un des suivants : {', '.join(allowed_type_sang)}")

class Type_Sang(models.Model):
    nom = models.CharField(max_length=3, primary_key=True, validators=[validate_type_sang])
    def __str__(self):
        return self.nom
    
    
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone

class UserManager(BaseUserManager):
    def create_user(self, tel, email, first_name=None, last_name=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given tel, email, and optional first name, last name, and password.
        """
        if not email:
            raise ValueError('The email field must be set')

        user = self.model(
            tel=tel,
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, tel, email, first_name=None, last_name=None, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given tel, email, and optional first name, last name, and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(tel, email, first_name, last_name, password, **extra_fields)
    

class DonateurManager(UserManager):
    def create_donateur(self, tel, email, date_naissance=None, wilaya=None, type_sang=None, password=None, **extra_fields):
        """
        Creates and saves a Donateur with the given tel, email, and optional date of birth, wilaya, type_sang, and extra fields.
        """
        if not tel:
            raise ValueError('The Tel field must be set')

        donateur = self.model(
            tel=tel,
            email=self.normalize_email(email),
            date_naissance=date_naissance,
            wilaya=wilaya,
            type_sang=type_sang,
            password=password,
            **extra_fields
        )
        donateur.save(using=self._db)
        return donateur

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)  # Champ d'ID propre
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100, null=True,blank=True)
    tel = models.CharField(max_length=8, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    email = models.EmailField(max_length=70, unique=True)
    password = models.CharField(max_length=128, null=True, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['tel', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.tel}"

class Donateur(User):
    id_d = models.AutoField(primary_key=True)  # Champ d'ID propre pour Donateur
    date_naissance = models.DateField(blank=True, null=True)
    wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True, blank=True)
    type_sang = models.ForeignKey(Type_Sang, on_delete=models.CASCADE, null=True, blank=True)
    test = models.BooleanField(default=False)
    a_fait_don = models.BooleanField(default=False)
    date_don = models.DateField(blank = True,null=True)
    date_don_active = models.DateField(blank = True,null=True)
    objects = DonateurManager()

    USERNAME_FIELD = 'tel'

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.tel} {self.wilaya} {self.type_sang}"

    
class Administrateur(User):
    id_A = models.AutoField(primary_key=True)
    
    

    
# class DonateurManager(BaseUserManager):
#     def create_user(self,  first_name, last_name, username, tel,password, email=None, wilaya=None, type_sang=None, **extra_fields):
#         if not tel and not username:
#             raise ValueError('Le champ "tel" est obligatoire.')
#         email = self.normalize_email(email)

#         # Assurez-vous que wilaya est une instance de Wilaya ou un entier (ID)
#         if wilaya:
#             if isinstance(wilaya, str):  # Si c'est un nom de wilaya
#                 try:
#                     wilaya = Wilaya.objects.get(nom=wilaya)
#                 except Wilaya.DoesNotExist:
#                     raise ValueError(f"Wilaya avec le nom {wilaya} n'existe pas.")
#             elif isinstance(wilaya, int):  # Si c'est un ID de wilaya
#                 try:
#                     wilaya = Wilaya.objects.get(id=wilaya)
#                 except Wilaya.DoesNotExist:
#                     raise ValueError(f"Wilaya avec l'ID {wilaya} n'existe pas.")

#         # Assurez-vous que type_sang est une instance de Type_Sang ou un entier (ID)
#         if type_sang:
#             if isinstance(type_sang, str):  # Si c'est un nom de type_sang
#                 try:
#                     type_sang = Type_Sang.objects.get(nom=type_sang)
#                 except Type_Sang.DoesNotExist:
#                     raise ValueError(f"Type de sang avec le nom {type_sang} n'existe pas.")
#             elif isinstance(type_sang, int):  # Si c'est un ID de type_sang
#                 try:
#                     type_sang = Type_Sang.objects.get(id=type_sang)
#                 except Type_Sang.DoesNotExist:
#                     raise ValueError(f"Type de sang avec l'ID {type_sang} n'existe pas.")

#         user = self.model( first_name=first_name, last_name=last_name,username=username, tel=tel,email=email, wilaya=wilaya, type_sang=type_sang, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self,first_name, last_name,username, tel,password,email=None, wilaya=None, type_sang=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         # Utilisez des IDs pour wilaya et type_sang pour le super utilisateur
#         return self.create_user( first_name, last_name, username, tel, password,email, wilaya, type_sang, **extra_fields)

# class Donateur(models.Model):
#     first_name = models.CharField(max_length=100,null=True,blank=True)
#     last_name = models.CharField(max_length=100, null=True,blank=True)
#     tel = models.CharField(max_length=8, unique=True)
#     username = models.CharField(max_length=150, unique=True,null=True,blank=True)
#     wilaya = models.ForeignKey(Wilaya, on_delete=models.CASCADE, null=True, blank=True)
#     type_sang = models.ForeignKey(Type_Sang, on_delete=models.CASCADE, null=True, blank=True)
#     email = models.EmailField(max_length=70, unique=True, null=True, blank=True)

#     # Utilisez 'email' comme champ de connexion
#     USERNAME_FIELD = 'username'
    
#     # Incluez 'email' dans les champs requis
#     REQUIRED_FIELDS = ['first_name', 'last_name','tel','email']

#     objects = DonateurManager()

    

