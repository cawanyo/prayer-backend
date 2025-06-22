from django.db import models
from accounts.models import CustomUser
from django.utils import timezone


class PrayerCategory(models.Model):
    name = models.CharField(max_length=255)

class Prayer(models.Model):
    content = models.CharField(max_length=255)
    submiter_name = models.CharField(max_length=255, null=True, blank=True)
    submiter_phone = models.CharField(max_length=255, null=True, blank=True)
    submiter_email = models.EmailField(max_length=255, default="", blank=True, null=True)
    submission_date = models.DateTimeField( auto_now_add=True,)
    STATE_CHOICES = [
        ('pending', 'Pending'),
        ('answered', 'Answered'),
        ('failed', 'Failed'),
    ]
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='pending')

    # Make user optional
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,      # Database can store NULL
        blank=True,     # Forms can leave this field blank
    )

    category = models.ForeignKey(
        PrayerCategory,
        on_delete=models.SET_DEFAULT,
        default=None,   # You might want to define a default category object
        null=True,      # Allow NULL in DB
        blank=True      # Allow blank in forms
    )


class Comment(models.Model):
    content = models.TextField()
    prayer = models.ForeignKey(Prayer, on_delete=models.CASCADE, related_name='comments')
    submiter_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.submiter_name} on Prayer {self.prayer.id}'
