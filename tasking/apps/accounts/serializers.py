# coding=utf-8

from django.contrib.auth.models import User
from rest_framework import serializers
from oauth2_provider.models import Application

from tasking.apps.accounts.models import UserProfile
from tasking.common.fields import PhoneField


def validate_client(client_id, client_secret):
    application = Application.objects.filter(client_id=client_id, client_secret=client_secret).first()
    if not application:
        raise serializers.ValidationError({'client': ['客户端认证失败']})
    return application


class SignUpSerializer(serializers.Serializer):
    type = serializers.CharField(default='email', max_length=63)
    client_id = serializers.CharField(required=True, max_length=255)
    client_secret = serializers.CharField(required=True, max_length=255)
    email = serializers.EmailField(
        required=False,
        max_length=255,
        allow_blank=True,
        error_messages={
            'invalid': '邮箱格式不正确'
        }
    )
    mobile = PhoneField(required=False, max_length=63, allow_blank=True)
    password = serializers.CharField(required=True, max_length=255)
    redirect_uri = serializers.CharField(required=True, max_length=255)

    def validate(self, data):
        type = data.get('type', None)
        if type == 'email':
            email = data.get('email', None)
            if not email:
                raise serializers.ValidationError({'email': '请输入电子邮箱'})
            existing = User.objects.filter(email=email).exists()
            if existing:
                raise serializers.ValidationError({'email': '该邮箱已被注册'})
        else:
            mobile = data.get('mobile', None)
            if not mobile:
                raise serializers.ValidationError({'mobile': '请输入手机号码'})
            existing = UserProfile.objects.filter(mobile=mobile).exists()
            if existing:
                raise serializers.ValidationError({'mobile': '该号码已被注册'})

        return data


class SignInSerializer(serializers.Serializer):
    client_id = serializers.CharField(required=True, max_length=255)
    client_secret = serializers.CharField(required=True, max_length=255)
    account = serializers.CharField(required=True, max_length=255)
    password = serializers.CharField(required=True, max_length=255)
    redirect_uri = serializers.CharField(required=True, max_length=255)

#
# class UserProfileSerializer(serializers.ModelSerializer):
#     email = serializers.ReadOnlyField(source='user.email')
#
#     class Meta:
#         model = UserProfile
#         fields = ('id', 'mobile', 'email')
#         read_only_fields = ('id', 'mobile', 'email')
