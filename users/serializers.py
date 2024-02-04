from rest_framework.serializers import ModelSerializer
from .models import Task, Expense, ShortUrl

class TaskSerializer(ModelSerializer):
  class Meta:
    model = Task
    fields = "__all__"

class ExpenseSerializer(ModelSerializer):
  class Meta:
    model = Expense
    fields = "__all__"

class ShortUrlSerializer(ModelSerializer):
  class Meta:
    model = ShortUrl
    fields = "__all__"