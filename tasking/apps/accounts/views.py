# coding=utf-8
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_201_CREATED

from tasking.apps.accounts.serializers import SignUpSerializer, UserProfileSerializer
from tasking.apps.accounts.models import UserProfile


class SignUpView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        resp_data = {
            'code': 0
        }
        status = HTTP_400_BAD_REQUEST

        if serializer.is_valid():
            username = serializer.data.get('username', '')
            password = serializer.data.get('password', '')

            if User.objects.filter(username=username).exists():
                error_messages = '用户名已存在'
                resp_data = {
                    'code': 0,
                    'error_messages': error_messages
                }
            else:
                password = make_password(password)
                User.objects.create(
                    username=username,
                    password=password
                )
                resp_data = {
                    'code': 1
                }
                status = HTTP_201_CREATED
                return Response(resp_data, status=status)

        return Response(resp_data, status=status)


class UserProfileView(APIView):

    def get(self, request):
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        serializer = UserProfileSerializer(instance=user_profile)
        return Response(serializer.data, status=HTTP_200_OK)


# class SignInView(APIView):
#
#     def post(self, request):
#         serializer = SignInSerializer(data=request.data)
#         resp_data = {
#             'code': 0
#         }
#         status = HTTP_400_BAD_REQUEST
#
#         if serializer.is_valid():
#             username = serializer.data.get('username', '')
#             password = serializer.data.get('password', '')
#             user = authenticate(username=username, password=password)
#
#             if user is not None:
#                 Token.objects.filter(user=user).delete()
#                 token = Token.objects.create(user=user)
#                 user_profile = UserProfile.objects.get_or_create(user=user)
#                 user_profile_serializer = UserProfileSerializer(data=user_profile)
#                 user_profile_data = user_profile_serializer.data # fuck
#                 resp_data = {
#                     'code': 1,
#                     'user_profile': user_profile_data,
#                     'token': token.key
#                 }
#                 status = HTTP_201_CREATED
#             else:
#                 error_messages = '密码错误' if User.objects.filter(username=username).exists() else '用户不存在'
#                 resp_data = {
#                     'code': 0,
#                     'error_messages': error_messages
#                 }
#
#         return Response(resp_data, status=status)
