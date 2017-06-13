# coding=utf-8
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from django.db.models import Q

from tasking.apps.tasks.models import Task
from tasking.apps.tasks.serializers import TaskListSerializer, TaskSerializer
from tasking.apps.tasks.permissions import TaskPermission


class TaskListPagination(PageNumberPagination):
    page_size = 18


class TaskListView(ListAPIView):
    pagination_class = TaskListPagination
    queryset = Task.objects.filter(status='recruit')
    permission_classes = (AllowAny,)
    serializer_class = TaskListSerializer


# CRUD
class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (TaskPermission,)
    serializer_class = TaskSerializer

    def get_queryset(self):
        from django.contrib.auth.models import User
        user = User.objects.get(username='root')
        queryset = super(TaskViewSet, self).get_queryset()
        role = self.request.query_params.get('role', '')
        if role == 'author':
            query = Q(author=user)
        elif role == 'member':
            query = Q(members__in=[user])
        else:
            query = Q(author=user) | Q(members__in=[user])
        queryset = queryset.filter(query).order_by('-id')
        # 去重返回
        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
