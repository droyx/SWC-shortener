from .models import ShortenedURL
from .shortener import generate_code
from .errors import CreateShortException

from django.db.utils import IntegrityError


class Shortener:
    def __init__(self, shorted_code_length: int = 8):
        self.shorted_code_length = shorted_code_length

    def create_shorted_url(self, url: str) -> ShortenedURL:

        code = generate_code(self.shorted_code_length)
        try:
            shorten, _ = ShortenedURL.objects.get_or_create(
                url=url, defaults={"code": code}
            )
        except IntegrityError:
            raise CreateShortException()
        return shorten
