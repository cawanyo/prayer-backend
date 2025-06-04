from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.

membre = Group.objects.get_or_create(name='membre')
intercesseur = Group.objects.get_or_create(name='intercesseur')
responsable = Group.objects.get_or_create(name='responsable')

