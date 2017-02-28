from django.contrib import admin

from tasking.apps.accounts.models import UserProfile


admin.site.register(UserProfile)
