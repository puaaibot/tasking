from django.conf.urls import url
from tasking.apps.accounts import views

urlpatterns = [
    url(r'^sign-up/$', views.SignUpView.as_view(), name='sign-up'),
    url(r'^user-info/$', views.UserInfoView.as_view(), name='user-info'),
]
