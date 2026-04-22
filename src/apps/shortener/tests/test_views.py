import json
from django.test import TestCase
from django.urls import reverse
from ..models import ShortenedURL
from .factories import ShortenedURLFactory


class TestShortenerView(TestCase):
    def test_success_create_shorted_url(self):
        # Given
        url = reverse("shorten-list")
        data = {"url": "http://test.com"}
        self.assertEqual(ShortenedURL.objects.count(), 0)

        # When
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        # Then
        self.assertEqual(response.status_code, 201)
        response_data = response.json()
        instance = ShortenedURL.objects.last()
        self.assertEqual(
            response_data, {"url": f"http://testserver/short/{instance.code}/"}
        )

    def test_wrong_url(self):
        # Given
        url = reverse("shorten-list")
        data = {"url": "wrongurl"}

        # When
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        # Then
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data, {"url": ["Enter a valid URL."]})

    def test_empty_url(self):
        # Given
        url = reverse("shorten-list")
        data = {"url": ""}

        # When
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        # Then
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data, {"url": ["This field may not be blank."]})

    def test_no_url(self):
        # Given
        url = reverse("shorten-list")
        data = {}

        # When
        response = self.client.post(
            url, data=json.dumps(data), content_type="application/json"
        )

        # Then
        self.assertEqual(response.status_code, 400)
        response_data = response.json()
        self.assertEqual(response_data, {"url": ["This field is required."]})

    def test_correct_code_redirects_to_url(self):
        # Given
        code = "12345678"
        redirect_url = "http://test.com"
        ShortenedURLFactory(code=code, url=redirect_url)
        url = reverse(
            "shorten-detail",
            args=[
                code,
            ],
        )

        # When
        response = self.client.get(url, content_type="application/json")

        # Then
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, redirect_url)

    def test_unexisted_code(self):
        # Given
        code = "12345678"
        url = reverse(
            "shorten-detail",
            args=[
                code,
            ],
        )

        # When
        response = self.client.get(url, content_type="application/json")

        # Then
        self.assertEqual(response.status_code, 404)
