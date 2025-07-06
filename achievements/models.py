from django.db import models

# Create your models here.

class Conference(models.Model):
    name = models.CharField(max_length=35)
    location = models.CharField(max_length=35)
    year = models.IntegerField()
    competitors = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_teams(self):
        teams = json.loads(self.competitors)
        if teams and teams != {}:
            return teams.keys()
        return None

class EventAchievement(models.Model):
    name = models.CharField(max_length=35)
    competitors = models.TextField()
    placement = models.CharField(max_length=3)

    conference = models.ForeignKey(Conference, on_delete=models.CASCADE)

    def __str__(self):
        return self.name