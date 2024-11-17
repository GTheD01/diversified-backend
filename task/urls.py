from django.urls import path

from task.views import task, tasks

urlpatterns=[
    path('', tasks, name='tasks'),
    path('<int:id>', task),
]