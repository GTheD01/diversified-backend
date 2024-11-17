from django.db import models
from django.conf import settings

class Expense(models.Model):
    label = models.CharField(max_length=205)
    price = models.DecimalField(max_digits=19, decimal_places=4)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.label
