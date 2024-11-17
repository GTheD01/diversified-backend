from django.urls import path, re_path
from shorturl.views import shortUrl, shortUrlDel


urlpatterns=[
    path('', shortUrl, name='shorturls'),
    path('<str:id>/', shortUrlDel),
]