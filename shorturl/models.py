from django.db import models
from django.conf import settings


class ShortUrl(models.Model):
    original_url = models.URLField(max_length=600)
    short_url = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.original_url