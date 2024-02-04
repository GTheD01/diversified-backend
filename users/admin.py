from django.contrib import admin
from .models import UserAccount, Task, Expense, ShortUrl

# Register your models here.

admin.site.register(UserAccount)
admin.site.register(Task)
admin.site.register(Expense)
admin.site.register(ShortUrl)
