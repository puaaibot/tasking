from django.conf.urls import url
from rest_framework.routers import SimpleRouter
from tasking.apps.tasks import views

urlpatterns = [
    url(r'all/^$', views.TaskListView.as_view(), name='task-list'),
]

router = SimpleRouter()
router.register(r'', views.TaskViewSet)

urlpatterns += router.urls
