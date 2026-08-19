import json
from django.db import models
from authentication.models import Member

# Create your models here.
class Team(models.Model):
    number = models.IntegerField(default=1)
    competitors = models.ManyToManyField(Member, through="TeamMember", related_name="teams")

    def __str__(self):
        formatted = "TEAM\n"
        for competitor in self.competitors:
            if competitor and competitor.name:
                formatted = f"\t{formatted}\n{competitor.name}"
        return formatted

class TeamMember(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    is_captain = models.BooleanField(default=False)

    def __str__(self):
        role = "Captain" if self.is_captain else "Member"
        return f"{self.user.name} ({role})"

class Event(models.Model):
    name = models.CharField(max_length=100)
    desc = models.TextField()
    prompt = models.TextField(blank=True, null=True)

    CEG = models.FileField(blank=True, null=True)
    teams = models.ManyToManyField(Team, related_name="teams")

    def __str__(self):
        return self.name