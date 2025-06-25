from unittest import TestCase
from lambda_function import lambda_handler

class Tests(TestCase):
    def test_lambda_handler(self):
        response = lambda_handler()
        self.assertTrue(response)