from django.db import models
from authentication.models import Member

class PushSubscription(models.Model):
    user = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)
    subscription_json = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Subscription {self.id} for {self.user or 'Anonymous'}"
