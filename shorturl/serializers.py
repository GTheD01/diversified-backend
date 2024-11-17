from rest_framework.serializers import ModelSerializer
from shorturl.models import ShortUrl


class ShortUrlSerializer(ModelSerializer):
  class Meta:
    model = ShortUrl
    fields = "__all__"