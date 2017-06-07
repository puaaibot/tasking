# coding=utf-8
from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.author == request.user


class TaskPermission(permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly):
    """
    登录后才能创建任务,
    任务所有者才能修改和删除任务
    """

    pass
