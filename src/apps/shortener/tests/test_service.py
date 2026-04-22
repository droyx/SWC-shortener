from unittest.mock import patch
from django.test import TestCase
from ..service import Shortener
from .factories import ShortenedURLFactory
from ..errors import CreateShortException


class TestShortener(TestCase):
    def test_success_create_shorted_url(self):
        # Given
        url = "http://test.com"

        # When
        result = Shortener(5).create_shorted_url(url)

        # Then
        self.assertEqual(result.url, url)
        self.assertEqual(len(result.code), 5)

    def test_create_shorted_url_when_code_not_unique(self):
        # Given
        url = "http://test.com"
        code = "12345678"
        ShortenedURLFactory.create(code=code)

        with patch("apps.shortener.service.generate_code") as mock_generate_code:
            mock_generate_code.side_effect = [code, "87654321"]

            # When
            result = Shortener().create_shorted_url(url)

            # Then
            self.assertEqual(mock_generate_code.call_count, 2)
            self.assertEqual(result.code, "87654321")
            self.assertEqual(result.url, url)

    def test_cannot_create_shorted_url(self):
        # Given
        url = "http://test.com"
        code = "12345678"
        ShortenedURLFactory.create(code=code)

        with patch("apps.shortener.service.generate_code") as mock_generate_code:
            mock_generate_code.return_value = code

            # When
            self.assertRaises(CreateShortException, Shortener().create_shorted_url, url)

    def test_create_shorted_url_not_create_new_object_when_existed_url(self):

        # Given
        url = "http://test.com"
        code = "12345678"
        shorten = ShortenedURLFactory.create(code=code, url=url)

        # When
        result = Shortener().create_shorted_url(url)

        # Then
        self.assertEqual(shorten.id, result.id)
        self.assertEqual(shorten.code, result.code)
        self.assertEqual(shorten.url, result.url)
