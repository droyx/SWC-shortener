from django.test import TestCase
from rest_framework.exceptions import ValidationError
from unittest.mock import patch
from ..serializers import ShortenerSerializer
from ..errors import CreateShortException, CreateShortAPIException
from django.test import RequestFactory


class TestShortenerSerializer(TestCase):
    def test_serializer_correct_url_field(self):
        # Given
        serializer = ShortenerSerializer(data={"url": "http://test.com"})

        # When
        serializer.is_valid(raise_exception=True)

        # Then
        self.assertEqual(serializer.validated_data["url"], "http://test.com")

    def test_serializer_incorrect_url(self):
        # Given
        serializer = ShortenerSerializer(data={"url": "noturl"})

        # When & Then
        self.assertRaises(ValidationError, serializer.is_valid, raise_exception=True)

    def test_serializer_success_create_short_url(self):
        # Given
        serializer = ShortenerSerializer(data={"url": "http://test.com"})
        serializer.is_valid(raise_exception=True)

        # When
        instance = serializer.save()

        # Then
        self.assertEqual(instance.url, "http://test.com")

    def test_serializer_raise_error_when_cannot_create_short_url(self):
        # Given
        serializer = ShortenerSerializer(data={"url": "http://test.com"})
        serializer.is_valid(raise_exception=True)

        # When & Then
        with patch(
            "apps.shortener.serializers.Shortener.create_shorted_url",
            side_effect=CreateShortException(),
        ):
            self.assertRaises(CreateShortAPIException, serializer.save)

    def test_serializer_to_representation(self):
        # Given
        request = RequestFactory().get("/short/", HTTP_HOST="testserver")
        serializer = ShortenerSerializer(
            data={"url": "http://test.com"}, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # When
        result = serializer.to_representation(serializer.instance)

        # Then
        self.assertEqual(
            result["url"], f"http://testserver/short/{serializer.instance.code}/"
        )
