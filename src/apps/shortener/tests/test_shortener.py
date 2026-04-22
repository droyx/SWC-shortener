from django.test import TestCase
from ..shortener import generate_code


class TestGenerateCode(TestCase):
    def test_generate_code_correct_code(self):
        # When
        result = generate_code(n=10)

        # Then
        self.assertIsInstance(result, str)
        self.assertEqual(len(result), 10)

    def test_multiple_generated_codes_are_random(self):
        # When
        code1 = generate_code(n=10)
        code2 = generate_code(n=10)
        code3 = generate_code(n=10)

        # Then
        self.assertEqual(len({code1, code2, code3}), 3)
