import factory
from factory.django import DjangoModelFactory

from django.db.models.signals import post_save

from ..models import ShortenedURL


@factory.django.mute_signals(post_save)
class ShortenedURLFactory(DjangoModelFactory):
    class Meta:
        model = ShortenedURL

    url = factory.Sequence(lambda n: f"http://test{n}.com")
    code = factory.Sequence(lambda n: f"code{n}")
