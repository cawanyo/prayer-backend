from django.db import models
from django.conf import settings

class RDVAvailability(models.Model):
    date = models.DateField()
    start_time = models.CharField(max_length=200)
    end_time = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.user.username} | {self.date} {self.start_time}-{self.end_time}"


class RDV(models.Model):
    STATE_CHOICES = [
        ('pending', 'Pending'),
        ('validated', 'Validated'),
        ('failed', 'Failed'),
    ]

    rdv_availabilities = models.ManyToManyField(RDVAvailability, related_name='rdvs')
    date = models.DateField(null=True)
    time = models.CharField(default='', max_length=200)
    informations = models.TextField(default='')
    selected_availability = models.ForeignKey(
        RDVAvailability,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='selected_for'
    )
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='pending')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rdvs_created'
    )
    validated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='rdvs_validated'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"RDV by {self.user.username} - {self.state}"
