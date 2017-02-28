# coding=utf-8
from rest_framework import serializers
from tasking.apps.accounts.models import UserProfile


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = UserProfile
        fields = ('username', 'email')
        read_only_fields = ('username', 'email')
