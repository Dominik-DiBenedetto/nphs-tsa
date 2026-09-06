from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser

class Member(AbstractUser):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=7, unique=True) # nNumber
    role = models.CharField(max_length=20, default="Member")
    email = models.EmailField(unique=True)
    strikesNum = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Strike(models.Model):
    reason = models.CharField(max_length=100)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="strikes")

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name', 'username', 'role', 'email'] 