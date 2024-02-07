from rest_framework.serializers import ModelSerializer
from .models import Task, Expense, ShortUrl, UserAccount

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

class AvatarSerializer(ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['avatar']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.avatar:
            representation['avatar'] = self.context['request'].build_absolute_uri(instance.avatar.url)
        return representation