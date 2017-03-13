# coding=utf-8

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db import OperationalError, ProgrammingError

from tasking.apps.accounts.models import UserProfile


class ModelEmailMobileBackend(ModelBackend):

    def authenticate(self, account=None, password=None, **kwargs):
        UserModel = get_user_model()
        if account is None:
            account = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username=account)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        try:
            user = UserModel._default_manager.get(email=account)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            pass

        try:
            user_profile = UserProfile.objects.get(mobile=account)
            user = user_profile.user
            if user.check_password(password):
                return user
        # OperationalError处理UserProfile表在admin后台未同步的异常
        except (UserProfile.DoesNotExist, OperationalError, ProgrammingError):
            return None
