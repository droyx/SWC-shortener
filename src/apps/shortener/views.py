from django.http.response import HttpResponsePermanentRedirect
from rest_framework import mixins, viewsets
from .models import ShortenedURL
from .serializers import ShortenerSerializer


class ShortenerView(
    mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet
):
    lookup_field = "code"
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenerSerializer

    def retrieve(self, request, *args, **kwargs):
        shorten = self.get_object()
        return HttpResponsePermanentRedirect(redirect_to=shorten.url)
