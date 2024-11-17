from rest_framework.serializers import ModelSerializer
from .models import UserAccount


class AvatarSerializer(ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['avatar']
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if instance.avatar:
            representation['avatar'] = self.context['request'].build_absolute_uri(instance.avatar.url)
        return representation