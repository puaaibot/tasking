from django.conf.urls import url
from tasking.apps.accounts import views

urlpatterns = [
    url(r'^sign-up/$', views.SignUpView.as_view(), name='sign-up'),
    url(r'^sign-in/$', views.SignInView.as_view(), name='sign-in'),
    # url(r'^user-profile/$', views.UserProfileView.as_view(), name='user-profile'),
]
