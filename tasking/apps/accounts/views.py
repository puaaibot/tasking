# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from oauth2_provider.models import Grant

from tasking.apps.accounts.serializers import (
    SignUpSerializer,
    SignInSerializer,
    # UserProfileSerializer,
    validate_client
)
from tasking.apps.accounts.models import UserProfile

from uuid import uuid4


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        status = HTTP_400_BAD_REQUEST
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            client_id = serializer.data.get('client_id', '')
            client_secret = serializer.data.get('client_secret', '')
            application = validate_client(client_id=client_id, client_secret=client_secret)

            password = serializer.data.get('password', '')
            hash_password = make_password(password)
            username = uuid4().hex[:30]
            email = serializer.data.get('email', '')
            mobile = serializer.data.get('mobile', '')
            redirect_uri = serializer.data.get('redirect_uri', '')
            grant_type = 'authorization_code'
            user = User.objects.create(
                username=username,
                email=email,
                password=hash_password,
                last_login=timezone.now(),
                is_active=True
            )
            UserProfile.objects.create(
                user=user,
                mobile=mobile
            )

            authorization_code = uuid4().hex[:30]
            expires = timezone.now() + timezone.timedelta(minutes=10)
            Grant.objects.create(
                user=user,
                code=authorization_code,
                application=application,
                expires=expires,
                redirect_uri=redirect_uri
            )
            resp_data = {
                'authorization_code': authorization_code,
                'grant_type': grant_type,
                'redirect_uri': redirect_uri
            }
            status = HTTP_201_CREATED
            return Response(resp_data, status=status)

        return Response(serializer.errors, status=status)


class SignInView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        status = HTTP_400_BAD_REQUEST
        serializer = SignInSerializer(data=request.data)

        if serializer.is_valid():
            client_id = serializer.data.get('client_id', '')
            client_secret = serializer.data.get('client_secret', '')
            application = validate_client(client_id=client_id, client_secret=client_secret)

            account = serializer.data.get('account', '')
            password = serializer.data.get('password', '')
            user = authenticate(account=account, password=password)
            if not user:
                raise serializers.ValidationError({'password': ['账户或密码错误']})

            redirect_uri = serializer.data.get('redirect_uri', '')
            grant_type = 'authorization_code'
            authorization_code = uuid4().hex[:30]
            expires = timezone.now() + timezone.timedelta(minutes=10)
            Grant.objects.create(
                user=user,
                code=authorization_code,
                application=application,
                expires=expires,
                redirect_uri=redirect_uri
            )
            resp_data = {
                'authorization_code': authorization_code,
                'grant_type': grant_type,
                'redirect_uri': redirect_uri
            }
            status = HTTP_201_CREATED
            return Response(resp_data, status=status)

        return Response(serializer.errors, status=status)


# class UserProfileView(APIView):
#
#     def get(self, request):
#         user_profile, created = UserProfile.objects.get_or_create(user=request.user)
#         serializer = UserProfileSerializer(instance=user_profile)
#         return Response(serializer.data, status=HTTP_200_OK)
