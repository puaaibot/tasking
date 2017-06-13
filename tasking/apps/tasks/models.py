# coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import time


class Task(models.Model):
    STATUS_CHOICES = (
        ('recruit', '招募中'),
        ('processing', '进行中'),
        ('finished', '结束'),
    )

    title = models.CharField(max_length=63, null=False)
    content = models.TextField(null=False)
    bounty = models.PositiveIntegerField(verbose_name='报酬', default=0)
    author = models.ForeignKey(User, related_name='published_tasks')
    members = models.ManyToManyField(User, related_name='participated_tasks', blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='recruit')
    created_at = models.FloatField(default=time.time)
    cycle = models.FloatField(verbose_name='任务周期', default=0)

    def __unicode__(self):
        return self.title
