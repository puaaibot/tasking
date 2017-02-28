# coding=utf-8
from django.core.cache import cache
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from rest_framework import HTTP_HEADER_ENCODING
from rest_framework.authtoken.models import Token
import datetime


def get_authorization_header_token(request):
    token = request.META.get('HTTP_AUTHORIZATION', b'') or request.COOKIES.get('auth_token', b'')
    if isinstance(token, type('')):
        token = token.encode(HTTP_HEADER_ENCODING)
    return token


class ExpiringTokenAuthentication(BaseAuthentication):
    model = Token

    def authenticate(self, request):
        token = get_authorization_header_token(request=request)

        if not token:
            return None
        try:
            token = token.decode()
        except UnicodeError:
            raise exceptions.AuthenticationFailed('认证失败')
        return self.authenticate_credentials(token)

    def authenticate_credentials(self, key):
        token_cache = 'token_' + key
        cache_user = cache.get(token_cache)

        if cache_user:
            return cache_user

        try:
            token = self.model.objects.get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed('认证失败')

        utc_now = datetime.datetime.utcnow()
        if token.created < utc_now - datetime.timedelta(days=14):
            raise exceptions.AuthenticationFailed('认证信息过期')

        if token:
            cache.set(token_cache, token.user, 7 * 24 * 60 * 60)

        return (token.user, token)

    def authenticate_header(self, request):
        return 'Token'
