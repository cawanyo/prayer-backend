from rest_framework import serializers
from .models import Program
from django.contrib.auth import get_user_model
from accounts.serializers import CustomUserSerializer
from accounts.permissions import ResponsableUpdatePermission


User = get_user_model()



class ProgramSerializer(serializers.ModelSerializer):
    person = CustomUserSerializer(read_only=True)
    person_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='person',
        write_only=True
    )

    created_by = CustomUserSerializer(read_only=True)

    class Meta:
        model = Program
        fields = ['id', 'name', 'date', 'start_time', 'end_time', 'person', 'person_id', 'created_by']
        read_only_fields = ['created_by']
