from django.db import models
from events.models import Event

# Create your models here.

class Conference(models.Model):
    name = models.CharField(max_length=35)
    location = models.CharField(max_length=35)
    date = models.DateField()
    year = models.IntegerField()

    def __str__(self):
        return self.name

class EventAchievement(models.Model):
    event = models.CharField(max_length=35)
    competitors = models.TextField()
    placement = models.CharField(max_length=3)

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    eventRef = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name