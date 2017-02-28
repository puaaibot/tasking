from django.conf.urls import url
from tasking.apps.accounts import views

urlpatterns = [
    url(r'^signup/$', views.SignUpView.as_view(), name='sign-up'),
    url(r'^user/$', views.UserProfileView.as_view(), name='user-profile'),
    # url(r'^signin/$', views.SignInView.as_view(), name='sign-in'),
]
