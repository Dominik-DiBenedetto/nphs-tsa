from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Member(AbstractUser):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=7, unique=True) # nNumber
    role = models.CharField(max_length=20)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.user.n_number