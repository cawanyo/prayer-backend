from django.db import models
from django.conf import settings

class Program(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    person = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='assigned_programs',
        help_text='The person responsible for this program',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_programs'
    )

    def __str__(self):
        return f"{self.name} - {self.date} ({self.start_time} to {self.end_time}) by {self.person.username}"
