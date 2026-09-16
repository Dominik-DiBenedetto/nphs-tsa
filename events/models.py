import json
from django.db import models
from authentication.models import Member

# Create your models here.
class Team(models.Model):
    number = models.IntegerField(default=1)
    competitors = models.ManyToManyField(Member, through="TeamMember", related_name="teams")

    def __str__(self):
        if not self.competitors.exists():
            return f"Team {self.number} (No competitors)"

        competitor_list = "\n".join(f"\t{competitor}" for competitor in self.teammember_set.all())
        return f"TEAM {self.number}:\n{competitor_list}"

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
    teams = models.ManyToManyField(Team, related_name="event")

    def __str__(self):
        return self.name