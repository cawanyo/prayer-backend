from django.db import models
from django.conf import settings

class Availability(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='availabilities')
    date = models.DateField()
    state = models.BooleanField(default=True)  # True = available

    class Meta:
        unique_together = ('user', 'date')  # one availability per user per day

    def __str__(self):
        return f"{self.user.username} - {self.date} - {'Available' if self.state else 'Unavailable'}"
