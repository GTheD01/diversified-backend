from django.urls import path, re_path
from .views import (
    CustomProviderAuthView,
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    LogoutView,
    tasks,
    task,
    expenses,
    expense,
    shortUrl,
    shortUrlDel
)

urlpatterns = [
    re_path(
        r'^o/(?P<provider>\S+)/$',
        CustomProviderAuthView.as_view(),
        name='provider-auth'
    ),
    path('jwt/create/', CustomTokenObtainPairView.as_view()),
    path('jwt/refresh/', CustomTokenRefreshView.as_view()),
    path('jwt/verify/', CustomTokenVerifyView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('tasks/', tasks, name='tasks'),
    path('tasks/<int:id>', task),
    path('expenses/', expenses, name='expenses'),
    path('expenses/<int:id>', expense),
    path('shorturls/', shortUrl, name='shorturls'),
    path('<str:id>/', shortUrlDel),
]