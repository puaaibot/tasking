from django.contrib import admin

from tasking.apps.tasks.models import Task


admin.site.register(Task)
