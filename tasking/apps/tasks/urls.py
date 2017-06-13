from django.conf.urls import url
from tasking.apps.tasks import views

urlpatterns = [
    url(r'^all/$', views.TaskListView.as_view(), name='task-all'),
]
