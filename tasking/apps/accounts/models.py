from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    mobile = models.CharField(max_length=63, null=True, blank=True)

    def __unicode__(self):
        return self.user.email or self.mobile
