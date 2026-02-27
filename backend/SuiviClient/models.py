from django.db import models
from django.contrib.auth.models import BaseUserManager,AbstractBaseUser
import  uuid
# Create your models here.

class UserManager(BaseUserManager):
    def create_user( self,email,password=None,**extra_fields ):
        if not email :
            raise ValueError('Email est obligatoire')
        email = self.normalize_email(email)
        user = self.model(email=email,**extra_fields )
        user.set_password(password)
        user.save(using = self._db)

        
        return user
    
    def create_superuser( self, email, password=None,**extra_fields ):
        extra_fields.setdefault("role","admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(email, password,**extra_fields)
    
       
    
class User(AbstractBaseUser):
    username = models.CharField(max_length=50, blank=True, default='')
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    email      = models.EmailField(unique=True)
    role       = models.CharField(max_length=20, default='user')  

    is_active    = models.BooleanField(default=True)
    is_staff     = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    
    
class Clients(models.Model):
    id =  models.UUIDField(primary_key=True, default=uuid.uuid4)
    nom = models.CharField(max_length=50)
    prenom = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    motDePasse = models.CharField(max_length=50)
    