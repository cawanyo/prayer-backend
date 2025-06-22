from rest_framework import serializers
from accounts.models import CustomUser
from .models import Prayer, PrayerCategory, Comment

class PrayerCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrayerCategory
        fields = ['id', 'name']

class PrayerSerializer(serializers.ModelSerializer):
    # Optional: nested representation of user and category
    user = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.all(),
        required=False,
        allow_null=True
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=PrayerCategory.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Prayer
        fields = [
            'id', 'content', 'submiter_name', 'submiter_phone', 'submiter_email',
            'user', 'category', 'submission_date', 'state'
        ]
        read_only_fields = ['submission_date']




class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'prayer', 'submiter_name', 'created_at']
        read_only_fields = ['prayer']