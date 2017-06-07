# coding=utf-8

from django.contrib.auth.models import User
from rest_framework import serializers
from oauth2_provider.models import Application

from tasking.apps.accounts.models import UserProfile
from tasking.common.fields import PhoneField


# 暂时没用
def validate_client(client_id, client_secret):
    application = Application.objects.filter(client_id=client_id, client_secret=client_secret).first()
    if not application:
        raise serializers.ValidationError({'client': ['客户端认证失败']})
    return application


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        max_length=255,
        allow_blank=True,
        error_messages={
            'invalid': '邮箱格式不正确',
            'required': '请输入电子邮箱'
        }
    )
    mobile = PhoneField(required=False, max_length=63, allow_blank=True)
    password = serializers.CharField(required=True, max_length=255)
    redirect_uri = serializers.CharField(required=False, max_length=255)

    def validate(self, data):
        email = data.get('email', None)
        mobile = data.get('mobile', None)
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': '该邮箱已被注册'})
        if mobile and UserProfile.objects.filter(mobile=mobile).exists():
            raise serializers.ValidationError({'mobile': '该号码已被注册'})

        return data


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
        fields = ('mobile',)


class UserSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'user_profile', 'email',)
        read_only_fields = ('id', 'user_profile', 'email',)
