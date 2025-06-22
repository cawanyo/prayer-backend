# Register your models here.
from django.contrib import admin
from django.contrib.auth.models import Group
from .models import CustomUser, MemberDemand
# Register your models here.
membre = Group.objects.get_or_create(name='membre')
intercesseur = Group.objects.get_or_create(name='intercesseur')
responsable = Group.objects.get_or_create(name='responsable')


admin.site.register(CustomUser)
admin.site.register(MemberDemand)
