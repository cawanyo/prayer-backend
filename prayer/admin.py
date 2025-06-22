from django.contrib import admin
from .models import Prayer, PrayerCategory, Comment
# Register your models here.
admin.site.register(PrayerCategory)
admin.site.register(Prayer)
admin.site.register(Comment)