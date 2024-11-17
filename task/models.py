from django.db import models
from django.conf import settings


class Task(models.Model):
    label = models.CharField(max_length=200)
    description = models.CharField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.label
