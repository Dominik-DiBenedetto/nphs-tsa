import json
from django.db import models
from authentication.models import Member

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    prompt = models.TextField(blank=True, null=True)

    CEG = models.FileField(blank=True, null=True)
    competitors = models.JSONField(blank=True, null=True)
    captain = models.OneToOneField(Member, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name