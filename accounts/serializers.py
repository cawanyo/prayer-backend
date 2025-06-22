from rest_framework import serializers
from .models import CustomUser, MemberDemand

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name','phone', 'password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone']
        extra_kwargs = {
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'phone': {'required': False},
        }

class MemberDemandSerializer(serializers.ModelSerializer):
    requester = CustomUserSerializer(read_only=True)
    validated_by = CustomUserSerializer(read_only=True)
    class Meta:
        model = MemberDemand
        fields = ['id', 'requester',  'validated_by', 'submitted_at', 'state']
        read_only_fields = ['requester', 'validated_by', 'submitted_at']
        
        