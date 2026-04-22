from rest_framework import serializers
from .service import Shortener
from django.urls import reverse

from .errors import CreateShortAPIException, CreateShortException


class ShortenerSerializer(serializers.Serializer):
    url = serializers.URLField(max_length=2000)

    def save(self, **kwargs):
        url = self.validated_data["url"]
        try:
            self.instance = Shortener().create_shorted_url(url)
        except CreateShortException:
            raise CreateShortAPIException()
        return self.instance

    def to_representation(self, instance):
        request = self._context["request"]
        url = request.build_absolute_uri(
            reverse("shorten-detail", args=[self.instance.code])
        )
        response = {"url": url}
        return response
