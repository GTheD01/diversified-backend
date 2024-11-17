from django.urls import path
from expense.views import expense, expenses

urlpatterns = [
    path('', expenses, name='expenses'),
    path('<int:id>', expense),

]