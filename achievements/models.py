from django.db import models
from events.models import Event

# Create your models here.

class Conference(models.Model):
    name = models.CharField(max_length=35)
    location = models.CharField(max_length=35, null=True, blank=True)
    month = models.CharField(max_length=10, null=True, blank=True)
    year = models.IntegerField()
    overall_placement = models.CharField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.name

class EventAchievement(models.Model):
    event = models.CharField(max_length=35)
    competitors = models.TextField(null=True, blank=True)
    placement = models.CharField(max_length=3)

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)
    eventRef = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name