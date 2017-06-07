# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from tasking.apps.accounts.serializers import (
    SignUpSerializer,
    UserSerializer
)
from tasking.apps.accounts.models import UserProfile

from uuid import uuid4


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        status = HTTP_400_BAD_REQUEST
        serializer = SignUpSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.data.get('password', '')
            hash_password = make_password(password)
            username = uuid4().hex[:30]
            email = serializer.data.get('email', '')
            mobile = serializer.data.get('mobile', '')
            redirect_uri = serializer.data.get('redirect_uri', '')
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

            resp_data = {
                'redirect_uri': redirect_uri
            }
            status = HTTP_201_CREATED
            return Response(resp_data, status=status)

        return Response(serializer.errors, status=status)


class UserInfoView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        serializer = UserSerializer(instance=request.user)
        return Response(serializer.data, status=HTTP_200_OK)
