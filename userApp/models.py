from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager


class UserModel(AbstractUser):
    userType  = models.CharField(default="personel", max_length=20, choices=[("personel","Personel"),("yönetici","Yönetici")])
    firstName = models.CharField(max_length=20)
    lastName  = models.CharField(max_length=30)
    email     = models.EmailField(unique=True)
    username  = None

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS =['firstName','lastName']

    objects = UserManager()

    def __str__(self):
        return self.email