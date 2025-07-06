from django.db import models
from authentication.models import Member


# Create your models here.
class AttendanceRecord(models.Model):
    date = models.DateField()
    n_number = models.CharField(max_length=7)
    user = models.ForeignKey(Member, on_delete=models.CASCADE, blank=True, null=True)
