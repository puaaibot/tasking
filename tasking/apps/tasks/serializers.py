# coding=utf-8

from rest_framework import serializers

from tasking.apps.tasks.models import Task
from tasking.apps.accounts.serializers import UserSerializer


class TaskListSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='email')

    class Meta:
        model = Task
        fields = ('id','title', 'content', 'bounty', 'created_at', 'cycle', 'author', 'url')


class TaskSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='email')
    members = UserSerializer(read_only=True, many=True)

    class Meta:
        model = Task
        fields = ('id', 'title', 'content', 'bounty', 'created_at', 'cycle', 'author', 'members', 'status', 'url')
