import json
from django.db import models

# Create your models here.
class Event(models.Model):
    name = models.CharField(max_length=35)
    desc = models.TextField()
    prompt = models.CharField(max_length=200, blank=True, null=True)

    CEG = models.FileField(blank=True, null=True)
    competitors = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_teams(self):
        teams = json.loads(self.competitors)
        if teams and teams != {}:
            return teams.keys()
        return None